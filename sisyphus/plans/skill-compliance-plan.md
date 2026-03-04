# Sisyphus Plan: AgentSkills Format Compliance Check & Refactor

## Context
All skills in `~/.config/opencode/skills/` have been verified for basic formatting compliance. Specifically:
- **YAML Frontmatter** strictly matches the spec (`name` regex valid, `<64` chars, `description` `<1024` chars, matches folder name).
- **Directory structures** are correct.

However, the AgentSkills specification dictates progressive disclosure for efficiency:
> Keep your main `SKILL.md` under 500 lines. Move detailed reference material to separate files (e.g., `references/guide.md`).

Two skills are currently violating or dangerously close to violating this rule:
1. `docx` (590 lines)
2. `skill-creator` (494 lines)

## Objectives
- Bring `docx/SKILL.md` strictly under 300 lines by migrating large instructional sections to flat `references/` files.
- Refactor `skill-creator/SKILL.md` to safely reduce its size beneath 300 lines using the same pattern.
- Ensure all new reference files are cleanly linked one level deep in the primary `SKILL.md` files (e.g., `[Creation Guide](references/creation.md)`).

## Steps
- [ ] Read and analyze `/Users/withvanko./.config/opencode/skills/docx/SKILL.md` to identify the largest logical sections (e.g., "Editing Existing Documents", "XML Structures").
- [ ] Extract these large sections into newly created files under `/Users/withvanko./.config/opencode/skills/docx/references/`.
- [ ] Replace the extracted sections in `docx/SKILL.md` with concise summaries and Markdown links to the new reference files.
- [ ] Read and analyze `/Users/withvanko./.config/opencode/skills/skill-creator/SKILL.md`.
- [ ] Extract massive prompt injection templates or schema definitions into `/Users/withvanko./.config/opencode/skills/skill-creator/references/`.
- [ ] Replace extracted content with links in `skill-creator/SKILL.md`.
- [ ] Verify both `SKILL.md` files now report under 400 lines (using `wc -l`).

## Constraints
- Do NOT nest references deeper than one folder (e.g., `references/xml/guide.md` is forbidden).
- Do NOT alter the frontmatter of any skill.
- Maintain the exact instructional logic—just physically relocate the text to save the agent's initial context window during skill discovery.
