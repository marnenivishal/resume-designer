# CLAUDE.md

See **[AGENTS.md](AGENTS.md)** — it is the single source of instructions for every AI
tool, and duplicating it here would guarantee the two drift apart.

Claude Code specifics:
- `SKILL.md` is the skill definition; it activates automatically when a resume, CV, or
  ATS question comes up.
- Install: clone into `~/.claude/skills/resume-designer` (all projects) or
  `.claude/skills/` (one project).

The one rule, repeated because it matters: **run `scripts/ats_check.py` and report what
it says.** Never call a resume "ATS-friendly" without it.
