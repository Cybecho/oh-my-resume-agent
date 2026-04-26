#!/usr/bin/env python3
"""EN resume optional publish step helper.

This script centralizes step 8 behavior for both OpenAI/Codex skills and
Claude skills.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_TARGETS = {"docx", "figma"}


@dataclass
class Paths:
    session_dir: Path
    state_path: Path
    en_resume_dir: Path
    ats_path: Path
    review_path: Path
    publish_dir: Path
    report_path: Path
    manifest_path: Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str | None) -> datetime:
    if not value:
        return datetime.fromtimestamp(0, tz=timezone.utc)
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return datetime.fromtimestamp(0, tz=timezone.utc)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_targets(raw_targets: str | None, default_targets: list[str]) -> list[str]:
    if raw_targets:
        targets = [t.strip().lower() for t in raw_targets.split(",") if t.strip()]
    else:
        targets = [str(t).strip().lower() for t in default_targets if str(t).strip()]
    if not targets:
        raise ValueError("No publish targets resolved")
    unknown = sorted(set(targets) - ALLOWED_TARGETS)
    if unknown:
        raise ValueError(f"Unsupported targets: {unknown}. Allowed: {sorted(ALLOWED_TARGETS)}")
    # Keep stable order, remove duplicates
    deduped: list[str] = []
    for target in targets:
        if target not in deduped:
            deduped.append(target)
    return deduped


def ensure_step8(state: dict[str, Any]) -> None:
    steps = state.setdefault("steps", {})
    step8 = steps.setdefault(
        "8",
        {
            "status": "not_requested",
            "optional": True,
            "file": "en_resume/08_publish/08_publish_report.md",
            "targets": [],
            "completed_at": "",
            "blocked_reason": "",
        },
    )
    step8.setdefault("status", "not_requested")
    step8["optional"] = True
    step8.setdefault("file", "en_resume/08_publish/08_publish_report.md")
    step8.setdefault("targets", [])
    step8.setdefault("completed_at", "")
    step8.setdefault("blocked_reason", "")
    if state.get("state_version", 1) < 2:
        state["state_version"] = 2


def resolve_session_dir(root: Path, session_arg: str | None) -> Path:
    output_root = root / "output"
    if session_arg:
        candidate = Path(session_arg).expanduser()
        if not candidate.is_absolute():
            candidate = (root / candidate).resolve()
        if candidate.name == "state_en.json":
            candidate = candidate.parent
        if candidate.name == "en_resume":
            candidate = candidate.parent
        if (candidate / "state_en.json").exists():
            return candidate
        raise FileNotFoundError(f"Invalid session path: {session_arg}")

    candidates: list[tuple[datetime, Path]] = []
    if not output_root.exists():
        raise FileNotFoundError(f"Output directory not found: {output_root}")
    for state_path in output_root.glob("*/state_en.json"):
        try:
            state = read_json(state_path)
        except Exception:
            continue
        step7 = state.get("steps", {}).get("7", {})
        if step7.get("status") != "completed":
            continue
        rank = parse_iso(state.get("updated_at"))
        if rank == datetime.fromtimestamp(0, tz=timezone.utc):
            rank = datetime.fromtimestamp(state_path.stat().st_mtime, tz=timezone.utc)
        candidates.append((rank, state_path.parent))
    if not candidates:
        raise FileNotFoundError("No step-7-completed EN session found")
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def build_paths(session_dir: Path) -> Paths:
    en_resume_dir = session_dir / "en_resume"
    publish_dir = en_resume_dir / "08_publish"
    return Paths(
        session_dir=session_dir,
        state_path=session_dir / "state_en.json",
        en_resume_dir=en_resume_dir,
        ats_path=en_resume_dir / "06_ats_report.md",
        review_path=en_resume_dir / "07_review_report.md",
        publish_dir=publish_dir,
        report_path=publish_dir / "08_publish_report.md",
        manifest_path=publish_dir / "publish_manifest.json",
    )


def extract_field_bool(text: str, key: str) -> bool | None:
    match = re.search(rf"^\s*-\s*{re.escape(key)}\s*:\s*(true|false)\s*$", text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).lower() == "true"
    match = re.search(rf"^\s*{re.escape(key)}\s*:\s*(true|false)\s*$", text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).lower() == "true"
    return None


def extract_top_pick(review_text: str) -> str | None:
    match = re.search(r"^\s*-\s*top_pick\s*:\s*([ABC])\s*$", review_text, re.IGNORECASE | re.MULTILINE)
    if not match:
        match = re.search(r"top_pick\s*:\s*([ABC])", review_text, re.IGNORECASE)
    if not match:
        return None
    return match.group(1).upper()


def extract_section(markdown_text: str, section_name: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(section_name)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
        flags=re.MULTILINE,
    )
    match = pattern.search(markdown_text)
    return match.group(1).strip() if match else ""


def evaluate_mandatory_fixes_clear(review_text: str) -> bool:
    gate_value = extract_field_bool(review_text, "mandatory_fixes_clear")
    if gate_value is not None:
        return gate_value

    section = extract_section(review_text, "Mandatory Fixes")
    if not section:
        return True

    lines = [line.strip() for line in section.splitlines() if line.strip()]
    entries = []
    for line in lines:
        normalized = re.sub(r"^\s*(?:[-*]|\d+\.)\s*", "", line).strip().lower()
        if normalized:
            entries.append(normalized)
    if not entries:
        return True

    none_pattern = re.compile(r"^(none\b|n/?a\b|no mandatory fixes\b|no required fixes\b)")
    return all(bool(none_pattern.search(entry)) for entry in entries)


def evaluate_ats_pass(ats_text: str, review_text: str) -> bool:
    gate_value = extract_field_bool(review_text, "ats_pass")
    if gate_value is not None:
        return gate_value
    match = re.search(r"^\s*-\s*overall_status\s*:\s*(pass|fail)\s*$", ats_text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).lower() == "pass"
    return False


def sanitize_variant_markdown(raw_text: str) -> str:
    text = raw_text
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    text = re.sub(r"\n##\s+Provenance Notes[\s\S]*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def parse_variant_sections(clean_text: str) -> dict[str, Any]:
    lines = clean_text.splitlines()
    name = ""
    header_line = ""
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            name = line[2:].strip()
            for follow in lines[idx + 1 :]:
                if follow.strip():
                    header_line = follow.strip()
                    break
            break

    section_pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(section_pattern.finditer(clean_text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(clean_text)
        sections[title] = clean_text[start:end].strip()

    contact_parts = [part.strip() for part in header_line.split("|")] if header_line else []
    location = contact_parts[0] if len(contact_parts) > 0 else ""
    phone = contact_parts[1] if len(contact_parts) > 1 else ""
    email = contact_parts[2] if len(contact_parts) > 2 else ""
    linkedin = contact_parts[3] if len(contact_parts) > 3 else ""

    return {
        "name": name,
        "header_line": header_line,
        "location": location,
        "phone": phone,
        "email": email,
        "linkedin": linkedin,
        "summary": sections.get("Professional Summary", ""),
        "technical_skills": sections.get("Technical Skills", ""),
        "experience": sections.get("Experience", ""),
        "projects": sections.get("Projects", ""),
        "education": sections.get("Education", ""),
        "certifications": sections.get("Certifications / Community (Optional)", "")
        or sections.get("Certifications / Community", ""),
        "full_markdown": clean_text.strip(),
    }


def extract_company_date(session_dir: Path, state: dict[str, Any]) -> tuple[str, str]:
    company = str(state.get("company", "")).strip() or session_dir.name
    date_match = re.search(r"^(\\d{8})_", session_dir.name)
    if date_match is None:
        date_match = re.search(r"_(\d{8})$", session_dir.name)
    date_part = date_match.group(1) if date_match else datetime.now(timezone.utc).strftime("%Y%m%d")
    return company, date_part


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return slug or "resume"


def render_docx(
    root: Path,
    paths: Paths,
    state: dict[str, Any],
    config: dict[str, Any],
    source_variant: str,
    variant_payload: dict[str, Any],
) -> dict[str, Any]:
    docx_cfg = config.get("docx", {})
    template_path_raw = str(docx_cfg.get("template_path", "")).strip()
    output_pattern = str(docx_cfg.get("output_name_pattern", "{YYYYMMDD}_{company}_{variant}.docx")).strip()
    jinja_strict = bool(docx_cfg.get("jinja_strict", True))
    section_mapping = docx_cfg.get("section_mapping", {}) or {}

    result: dict[str, Any] = {
        "status": "failed",
        "artifact": "file",
        "identifier": "",
        "link": "",
        "path": "",
        "error": "",
    }

    if not template_path_raw:
        result["error"] = "missing_docx_template_path"
        return result

    template_path = Path(template_path_raw)
    if not template_path.is_absolute():
        template_path = (root / template_path).resolve()
    if not template_path.exists():
        result["error"] = f"missing_docx_template:{template_path}"
        return result

    try:
        from docxtpl import DocxTemplate
    except Exception as exc:
        result["error"] = f"missing_dependency_docxtpl:{exc}"
        return result

    context = dict(variant_payload)
    company, date_part = extract_company_date(paths.session_dir, state)
    context.update(
        {
            "company": company,
            "position": str(state.get("position", "")),
            "session": paths.session_dir.name,
            "date": date_part,
            "variant": source_variant,
            "generated_at": utc_now_iso(),
        }
    )
    if isinstance(section_mapping, dict):
        for template_var, source_key in section_mapping.items():
            context[str(template_var)] = context.get(str(source_key), "")

    file_name = output_pattern.format(
        company=safe_slug(company),
        date=date_part,
        variant=source_variant,
    )
    if not file_name.lower().endswith(".docx"):
        file_name += ".docx"
    output_path = paths.publish_dir / file_name
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        doc = DocxTemplate(str(template_path))
        if jinja_strict:
            from jinja2 import Environment, StrictUndefined

            env = Environment(undefined=StrictUndefined, autoescape=False)
            doc.render(context, jinja_env=env)
        else:
            doc.render(context)
        doc.save(str(output_path))
    except Exception as exc:
        result["error"] = f"docx_render_failed:{exc}"
        return result

    result.update(
        {
            "status": "success",
            "identifier": output_path.name,
            "path": str(output_path),
            "error": "",
        }
    )
    return result


def summarize_blocking_reasons(gate: dict[str, Any], targets: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for reason in gate.get("blocking_reasons", []):
        if reason and reason not in reasons:
            reasons.append(str(reason))
    for target_name, target_result in targets.items():
        if target_result.get("status") == "failed":
            error = str(target_result.get("error", "")).strip() or "unknown_error"
            reasons.append(f"{target_name}:{error}")
    return reasons


def build_publish_report(manifest: dict[str, Any], paths: Paths) -> str:
    gate = manifest.get("gate", {})
    state_summary = manifest.get("state", {})
    requested_targets = manifest.get("requested_targets", [])
    target_results = manifest.get("targets", {})
    state = manifest.get("state_en", {})
    company = state.get("company", paths.session_dir.name)
    role = state.get("position", "")

    rows: list[str] = []
    for target in requested_targets:
        item = target_results.get(target, {})
        rows.append(
            "| {target} | {status} | {artifact} | {identifier} | {link} | {error} |".format(
                target=target,
                status=item.get("status", "-"),
                artifact=item.get("artifact", "-"),
                identifier=item.get("identifier", "-") or "-",
                link=item.get("link", "-") or "-",
                error=item.get("error", "-") or "-",
            )
        )
    rows_text = "\n".join(rows) if rows else "| - | - | - | - | - | - |"

    gate_blocking = gate.get("blocking_reasons", [])
    gate_blocking_lines = "\n".join([f"  {idx}. {reason}" for idx, reason in enumerate(gate_blocking, 1)])
    if not gate_blocking_lines:
        gate_blocking_lines = "  1. None"

    report = f"""# Resume Publish Report: {company} - {role}

## Request
- session: {paths.session_dir}
- requested_targets: {requested_targets}
- source_variant: {manifest.get("source_variant")}
- force: {manifest.get("force", False)}

## Gate Check
- ats_pass: {gate.get("ats_pass")}
- has_top_pick: {gate.get("has_top_pick")}
- mandatory_fixes_clear: {gate.get("mandatory_fixes_clear")}
- gate_passed: {gate.get("gate_passed")}
- gate_blocking_reasons:
{gate_blocking_lines}

## Target Results
| Target | Status | Artifact | Identifier | Link | Error |
|--------|--------|----------|------------|------|-------|
{rows_text}

## Manifest
- path: {paths.manifest_path}

## State Update
- step_8_status: {state_summary.get("step_8_status")}
- blocked_reason: {state_summary.get("blocked_reason")}
- completed_at: {state_summary.get("completed_at")}
"""
    return report


def update_state_for_step8(
    state: dict[str, Any],
    targets: list[str],
    status: str,
    blocked_reason: str = "",
    completed: bool = False,
) -> None:
    ensure_step8(state)
    step8 = state["steps"]["8"]
    step8["status"] = status
    step8["targets"] = targets
    step8["blocked_reason"] = blocked_reason
    step8["completed_at"] = utc_now_iso() if completed else ""
    if completed:
        state["current_step"] = 9
    elif status == "in_progress":
        state["current_step"] = 8
    state["updated_at"] = utc_now_iso()


def prepare_command(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = read_json(root / "config" / "en_resume_publish.json")
    targets = parse_targets(args.targets, config.get("default_targets", ["docx", "figma"]))

    session_dir = resolve_session_dir(root, args.session)
    paths = build_paths(session_dir)
    state = read_json(paths.state_path)
    ensure_step8(state)

    ats_text = read_text(paths.ats_path) if paths.ats_path.exists() else ""
    review_text = read_text(paths.review_path) if paths.review_path.exists() else ""

    top_pick = extract_top_pick(review_text)
    has_top_pick = bool(top_pick)
    ats_pass = evaluate_ats_pass(ats_text, review_text)
    mandatory_fixes_clear = evaluate_mandatory_fixes_clear(review_text)

    blocking_reasons: list[str] = []
    gate_cfg = config.get("gate", {})
    if gate_cfg.get("require_ats_pass", True) and not ats_pass:
        blocking_reasons.append("ats_not_pass")
    if gate_cfg.get("require_top_pick", True) and not has_top_pick:
        blocking_reasons.append("missing_top_pick")
    if gate_cfg.get("require_no_mandatory_fixes", True) and not mandatory_fixes_clear:
        blocking_reasons.append("mandatory_fixes_not_clear")

    gate_passed = not blocking_reasons
    if args.force and not gate_passed:
        gate_passed = True
        blocking_reasons.append("gate_overridden_by_force")

    target_results: dict[str, Any] = {}
    for target in targets:
        target_results[target] = {
            "status": "skipped",
            "artifact": "file" if target == "docx" else "frame",
            "identifier": "",
            "link": "",
            "path": "",
            "error": "",
        }

    if not gate_passed:
        for target in targets:
            target_results[target]["status"] = "skipped"
            target_results[target]["error"] = "gate_blocked"
        final_status = "blocked"
        blocked_reason = ";".join(blocking_reasons)
        update_state_for_step8(state, targets, final_status, blocked_reason=blocked_reason, completed=False)
    else:
        variant_path = paths.en_resume_dir / "05_resume" / f"variant_{top_pick}.md"
        if not variant_path.exists():
            blocking_reasons.append(f"missing_variant_file:{variant_path}")
            gate_passed = False
            for target in targets:
                target_results[target]["status"] = "failed"
                target_results[target]["error"] = "missing_variant_file"
            final_status = "blocked"
            blocked_reason = ";".join(blocking_reasons)
            update_state_for_step8(state, targets, final_status, blocked_reason=blocked_reason, completed=False)
        else:
            variant_raw = read_text(variant_path)
            variant_clean = sanitize_variant_markdown(variant_raw)
            variant_payload = parse_variant_sections(variant_clean)

            if "docx" in targets:
                target_results["docx"] = render_docx(
                    root=root,
                    paths=paths,
                    state=state,
                    config=config,
                    source_variant=top_pick or "",
                    variant_payload=variant_payload,
                )
            if "figma" in targets:
                target_results["figma"] = {
                    "status": "pending",
                    "artifact": "frame",
                    "identifier": "",
                    "link": "",
                    "path": "",
                    "error": "",
                }

            if "figma" in targets:
                final_status = "in_progress"
                blocked_reason = ""
                update_state_for_step8(state, targets, final_status, blocked_reason=blocked_reason, completed=False)
            else:
                all_success = all(target_results[t]["status"] == "success" for t in targets)
                final_status = "completed" if all_success else "blocked"
                blocked_reason = "" if all_success else ";".join(summarize_blocking_reasons({"blocking_reasons": []}, target_results))
                update_state_for_step8(
                    state,
                    targets,
                    final_status,
                    blocked_reason=blocked_reason,
                    completed=all_success,
                )

    gate_summary = {
        "ats_pass": ats_pass,
        "has_top_pick": has_top_pick,
        "mandatory_fixes_clear": mandatory_fixes_clear,
        "gate_passed": gate_passed,
        "blocking_reasons": blocking_reasons,
    }
    step8_state = state.get("steps", {}).get("8", {})
    manifest = {
        "schema_version": 1,
        "generated_at": utc_now_iso(),
        "session": str(paths.session_dir),
        "source_variant": top_pick,
        "requested_targets": targets,
        "force": bool(args.force),
        "gate": gate_summary,
        "targets": target_results,
        "state": {
            "step_8_status": step8_state.get("status"),
            "blocked_reason": step8_state.get("blocked_reason", ""),
            "completed_at": step8_state.get("completed_at", ""),
        },
        "state_en": {
            "company": state.get("company", ""),
            "position": state.get("position", ""),
        },
    }

    write_json(paths.manifest_path, manifest)
    write_text(paths.report_path, build_publish_report(manifest, paths))
    write_json(paths.state_path, state)

    response = {
        "status": manifest["state"]["step_8_status"],
        "session": str(paths.session_dir),
        "manifest_path": str(paths.manifest_path),
        "report_path": str(paths.report_path),
        "requested_targets": targets,
        "source_variant": top_pick,
        "next_action": "finalize" if "figma" in targets and manifest["state"]["step_8_status"] == "in_progress" else "done",
    }
    print(json.dumps(response, ensure_ascii=False))
    return 0


def finalize_command(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    session_dir = resolve_session_dir(root, args.session)
    paths = build_paths(session_dir)

    state = read_json(paths.state_path)
    ensure_step8(state)

    if not paths.manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {paths.manifest_path}")
    manifest = read_json(paths.manifest_path)
    targets = manifest.get("requested_targets", [])
    target_results: dict[str, Any] = manifest.get("targets", {})

    if "figma" in targets:
        figma_status = args.figma_status.lower()
        if figma_status not in {"success", "failed", "skipped", "pending"}:
            raise ValueError("figma-status must be one of: success, failed, skipped, pending")
        target_results.setdefault("figma", {})
        target_results["figma"].update(
            {
                "status": figma_status,
                "artifact": "frame",
                "identifier": args.figma_node_id or "",
                "link": args.figma_url or "",
                "path": "",
                "error": args.figma_error or "",
            }
        )

    statuses = [str(target_results.get(target, {}).get("status", "failed")) for target in targets]
    if any(status == "pending" for status in statuses):
        step_status = "in_progress"
        completed = False
        blocked_reason = ""
    else:
        all_success = all(status == "success" for status in statuses)
        step_status = "completed" if all_success else "blocked"
        completed = all_success
        blocked_reason = "" if all_success else ";".join(summarize_blocking_reasons(manifest.get("gate", {}), target_results))

    update_state_for_step8(state, targets, step_status, blocked_reason=blocked_reason, completed=completed)

    manifest["generated_at"] = utc_now_iso()
    manifest["targets"] = target_results
    manifest["state"] = {
        "step_8_status": step_status,
        "blocked_reason": state.get("steps", {}).get("8", {}).get("blocked_reason", ""),
        "completed_at": state.get("steps", {}).get("8", {}).get("completed_at", ""),
    }
    manifest["state_en"] = {
        "company": state.get("company", ""),
        "position": state.get("position", ""),
    }

    write_json(paths.manifest_path, manifest)
    write_text(paths.report_path, build_publish_report(manifest, paths))
    write_json(paths.state_path, state)

    response = {
        "status": step_status,
        "session": str(paths.session_dir),
        "manifest_path": str(paths.manifest_path),
        "report_path": str(paths.report_path),
    }
    print(json.dumps(response, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EN resume publish helper")
    parser.add_argument("--root", default=".", help="Repository root path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Prepare publish (gate + docx + pending figma)")
    prepare.add_argument("--session", help="Session path (output/{YYYYMMDD}_{company})", default=None)
    prepare.add_argument("--targets", help="Comma-separated targets: docx,figma", default=None)
    prepare.add_argument("--force", action="store_true", help="Bypass gate failures (not recommended)")
    prepare.set_defaults(func=prepare_command)

    finalize = subparsers.add_parser("finalize", help="Finalize publish with figma result")
    finalize.add_argument("--session", help="Session path (output/{YYYYMMDD}_{company})", default=None)
    finalize.add_argument(
        "--figma-status",
        default="success",
        help="Figma status: success|failed|skipped|pending",
    )
    finalize.add_argument("--figma-node-id", default="", help="Figma frame/node id")
    finalize.add_argument("--figma-url", default="", help="Figma URL")
    finalize.add_argument("--figma-error", default="", help="Figma error message")
    finalize.set_defaults(func=finalize_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
