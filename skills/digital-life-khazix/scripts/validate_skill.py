#!/usr/bin/env python3
"""Validate the digital-life-khazix skill structure and forward-test cases."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
OPENAI_YAML = ROOT / "agents" / "openai.yaml"
FORWARD_CASES = ROOT / "tests" / "forward_cases.yaml"
STYLE_REGRESSIONS = ROOT / "tests" / "style_regressions.yaml"
REQUIRED_REFERENCES = {
    "references/opening_playbook.md",
    "references/writing_modes.md",
    "references/zhihu_baokuan_playbook.md",
    "references/reader_engagement_playbook.md",
    "references/fact_boundary_and_variation.md",
    "references/human_texture_revision.md",
    "references/popular_science_texture.md",
    "references/anti_ai_revision.md",
    "references/style_examples.md",
    "references/content_methodology.md",
    "references/visual_delivery_playbook.md",
}
REQUIRED_CASE_CATEGORIES = {
    "workplace",
    "relationship",
    "social-event",
    "hot-topic",
    "ai-tool",
    "product-experience",
}


def fail(message: str) -> None:
    raise ValueError(message)


def read_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_skill_md() -> None:
    content = SKILL_MD.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        fail("SKILL.md frontmatter is missing or invalid")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        fail("SKILL.md frontmatter must be a mapping")
    if frontmatter.get("name") != "digital-life-khazix":
        fail("SKILL.md name must be digital-life-khazix")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        fail("SKILL.md description is missing")
    if len(description.strip()) > 1024:
        fail("SKILL.md description exceeds 1024 characters")

    referenced = set(re.findall(r"`(references/[^`]+\.md)`", content))
    missing_required = sorted(REQUIRED_REFERENCES - referenced)
    if missing_required:
        fail(f"SKILL.md does not reference required files: {missing_required}")
    missing_files = sorted(path for path in referenced if not (ROOT / path).exists())
    if missing_files:
        fail(f"Referenced files do not exist: {missing_files}")


def validate_openai_yaml() -> None:
    config = read_yaml(OPENAI_YAML)
    if not isinstance(config, dict) or not isinstance(config.get("interface"), dict):
        fail("agents/openai.yaml must contain an interface mapping")
    interface = config["interface"]
    if interface.get("display_name") != "数字生命卡兹克":
        fail("agents/openai.yaml display_name must preserve the Chinese UI name")
    prompt = interface.get("default_prompt", "")
    if "$digital-life-khazix" not in prompt:
        fail("agents/openai.yaml default_prompt must mention $digital-life-khazix")


def validate_forward_cases() -> None:
    config = read_yaml(FORWARD_CASES)
    if not isinstance(config, dict) or not isinstance(config.get("cases"), list):
        fail("tests/forward_cases.yaml must contain a cases list")
    delivery_contract = config.get("delivery_contract")
    if not isinstance(delivery_contract, dict):
        fail("tests/forward_cases.yaml must contain a delivery_contract mapping")
    if delivery_contract.get("minimum_images") != 0:
        fail("delivery_contract.minimum_images must be 0 for draft-only default delivery")
    if delivery_contract.get("insertion_anchor_required") != "only_when_images_requested":
        fail("delivery_contract.insertion_anchor_required must be only_when_images_requested")
    image_safety = delivery_contract.get("image_safety", "")
    if not isinstance(image_safety, str) or "血腥" not in image_safety:
        fail("delivery_contract.image_safety must mention non-graphic image handling")
    cases = config["cases"]
    categories = {case.get("category") for case in cases if isinstance(case, dict)}
    if categories != REQUIRED_CASE_CATEGORIES:
        fail(f"Forward-test categories mismatch: {sorted(categories)}")
    required_fields = {
        "id",
        "category",
        "prompt",
        "expected_mode",
        "comment_entry",
        "save_anchor",
        "must_avoid",
    }
    for case in cases:
        if not isinstance(case, dict):
            fail("Each forward-test case must be a mapping")
        missing = required_fields - set(case)
        if missing:
            fail(f"Forward-test case {case.get('id')} is missing fields: {sorted(missing)}")


def validate_style_regressions() -> None:
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT / "scripts"))
    from lint_draft_style import analyze_text

    config = read_yaml(STYLE_REGRESSIONS)
    if not isinstance(config, dict) or not isinstance(config.get("cases"), list):
        fail("tests/style_regressions.yaml must contain a cases list")
    if not config["cases"]:
        fail("tests/style_regressions.yaml must contain at least one case")
    for case in config["cases"]:
        if not isinstance(case, dict):
            fail("Each style-regression case must be a mapping")
        required = {"id", "expected_flags", "ai_like_excerpt", "humanized_excerpt"}
        missing = required - set(case)
        if missing:
            fail(f"Style-regression case {case.get('id')} is missing fields: {sorted(missing)}")
        actual_flags = set(analyze_text(case["ai_like_excerpt"]))
        expected_flags = set(case["expected_flags"])
        if not expected_flags <= actual_flags:
            fail(
                f"Style-regression case {case['id']} missed flags: "
                f"{sorted(expected_flags - actual_flags)}"
            )
        revised_flags = analyze_text(case["humanized_excerpt"])
        if revised_flags:
            fail(f"Humanized excerpt {case['id']} still triggers flags: {revised_flags}")


def main() -> int:
    try:
        validate_skill_md()
        validate_openai_yaml()
        validate_forward_cases()
        validate_style_regressions()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"[ERROR] {exc}")
        return 1
    print("[OK] skill structure, UI metadata, references, draft-only delivery contract, 6 forward-test cases, and style regressions are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
