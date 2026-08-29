---
name: skill-zongjie
description: Summarize local custom Codex skills by listing each skill name with a concise function summary. Use when the user asks for an inventory, overview, or recap of self-created skills under the local Codex skills directory.
---

# Skill Zongjie

Use this skill to produce a compact summary of local custom skills.

## Default Workflow

1. Resolve the local skills root.
   - Prefer `$CODEX_HOME/skills`.
   - Fall back to the default local Codex skills directory when `CODEX_HOME` is unset.
2. Run the bundled script:
   - `python <skill-dir>/scripts/list_custom_skills.py`
3. Return one flat list that includes:
   - the skill name
   - a concise one-line function summary
4. Match the user's language and keep the wording brief unless the user asks for more detail.

## What Counts As A Custom Skill

Treat a skill as custom when all of the following are true:

- it lives directly under the local skills root
- it contains a top-level `SKILL.md`
- it is not `.system`
- its folder name is not listed in `references/builtin_skills.txt`

This rule is meant to catch user-added local skills reliably.

It does not reliably detect edits to bundled built-in skills. If the user explicitly asks to include modified built-ins too, do an additional manual inspection and say that it is a broader pass than the default custom-skill summary.

## Output Rules

- Prefer the format `- skill-name: short summary`.
- Do not dump full `SKILL.md` contents.
- If a skill still has placeholder text or an incomplete description, say that plainly instead of inventing details.
- If no custom skills are found, say so directly.

## Bundled Script

Use the script at `scripts/list_custom_skills.py`.

Optional override:

- `python <skill-dir>/scripts/list_custom_skills.py --skills-root <path>`

The script already:

- scans the skills root
- filters out built-in skills listed in `references/builtin_skills.txt`
- reads each candidate `SKILL.md`
- extracts `name` and `description` from YAML frontmatter when available
- falls back to the first useful paragraph when the frontmatter is incomplete
- shortens the summary so the result stays concise
