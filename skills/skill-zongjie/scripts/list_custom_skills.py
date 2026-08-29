from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


PLACEHOLDER_PREFIXES = ("[TODO", "TODO:")
TRIGGER_MARKERS = (
    " Use when ",
    " use when ",
    " Use this skill when ",
    " use this skill when ",
    " Trigger when ",
    " trigger when ",
    " When the user ",
    " when the user ",
)


def resolve_default_skills_root() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def load_builtin_names(reference_path: Path) -> set[str]:
    builtin_names: set[str] = set()
    for raw_line in reference_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        builtin_names.add(line)
    return builtin_names


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_frontmatter(skill_text: str) -> tuple[dict[str, str], str]:
    if not skill_text.startswith("---"):
        return {}, skill_text

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", skill_text, flags=re.DOTALL)
    if not match:
        return {}, skill_text

    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip("'\"")

    return frontmatter, skill_text[match.end() :]


def first_useful_paragraph(body: str) -> str:
    paragraphs = re.split(r"\n\s*\n", body)
    for paragraph in paragraphs:
        candidate = normalize_space(paragraph)
        if not candidate:
            continue
        if candidate.startswith("#"):
            continue
        if candidate.startswith(PLACEHOLDER_PREFIXES):
            continue
        return candidate
    return ""


def compress_summary(description: str, body: str) -> str:
    cleaned_description = normalize_space(description)
    paragraph = first_useful_paragraph(body)
    candidates: list[str] = []
    if cleaned_description and not cleaned_description.startswith(PLACEHOLDER_PREFIXES):
        candidates.append(cleaned_description)
    if paragraph:
        candidates.append(paragraph)

    for candidate in candidates:
        summary = candidate
        for marker in TRIGGER_MARKERS:
            index = summary.find(marker)
            if index > 0:
                summary = summary[:index].strip(" .;:-")
                break

        split_parts = re.split(r"(?<=[.!?。；;])\s+", summary, maxsplit=1)
        if split_parts:
            summary = split_parts[0]

        summary = summary.strip(" .;:-")
        if len(summary) >= 12:
            if len(summary) > 120:
                summary = summary[:117].rstrip() + "..."
            return summary

    return "Description not completed yet."


def extract_skill_info(skill_dir: Path) -> tuple[str, str]:
    skill_file = skill_dir / "SKILL.md"
    skill_text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(skill_text)

    name = normalize_space(frontmatter.get("name", "")) or skill_dir.name
    summary = compress_summary(frontmatter.get("description", ""), body)
    return name, summary


def collect_custom_skills(skills_root: Path, builtin_names: set[str]) -> list[tuple[str, str]]:
    custom_skills: list[tuple[str, str]] = []
    for child in sorted(skills_root.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_dir():
            continue
        if child.name == ".system":
            continue
        if child.name in builtin_names:
            continue
        if not (child / "SKILL.md").is_file():
            continue
        custom_skills.append(extract_skill_info(child))
    return custom_skills


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List local custom Codex skills with concise summaries."
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=resolve_default_skills_root(),
        help="Override the local skills directory to scan.",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    builtin_reference = script_dir.parent / "references" / "builtin_skills.txt"
    builtin_names = load_builtin_names(builtin_reference)

    skills_root = args.skills_root.resolve()
    custom_skills = collect_custom_skills(skills_root, builtin_names)

    if not custom_skills:
        print(f"No custom local skills found in {skills_root}.")
        return

    print(f"Found {len(custom_skills)} custom local skill(s) in {skills_root}:")
    for name, summary in custom_skills:
        print(f"- {name}: {summary}")


if __name__ == "__main__":
    main()
