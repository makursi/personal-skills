# Personal Skills

A personal collection of Agent Skills, and the single source of truth for them. Skills are written here once and linked into each agent's skills directory, so editing a file here updates the installed skill immediately.

## Status

Maintained.

## Getting started

Requires Python 3.13 with PyYAML, and Node.js 22 — the versions CI uses.

Validate every skill in the repository:

```bash
python scripts/validate-skills.py
```

Preview the install without writing to disk:

```bash
node scripts/install-skills.mjs --dry-run
```

## Usage

Start a new skill from the template:

```bash
cp -r templates/skill-template skills/my-skill
```

The copy prints nothing; `skills/my-skill/` then exists. Edit its `SKILL.md`: set `name` to `my-skill`, keep the frontmatter English, and replace the body with real steps. Run the validation command above; with the new skill filled in it exits 0 and reports two skills, zero errors, and zero warnings.

## Architecture

```text
.
├── AGENTS.md                  # rules agents follow in this repository
├── CONTRIBUTING.md            # how to add or change a skill
├── GLOSSARY.md                # the repository's vocabulary
├── LICENSE                    # MIT
├── README.md                  # this file
├── docs/
│   ├── adr/                   # decisions that are hard to reverse
│   └── agents/                # agent-facing conventions and design notes
├── skills/                    # one directory per skill; the only place skills are written
│   └── write-readme/          # write a repository README from a fixed skeleton
├── templates/skill-template/  # starting point for a new skill
├── scripts/                   # validation and installation
└── .github/workflows/         # CI
```

## Documentation

- [AGENTS.md](./AGENTS.md): what agents read before changing the repository
- [GLOSSARY.md](./GLOSSARY.md): the words to use in docs and pull requests
- [docs/adr/](./docs/adr/): decisions that are hard to reverse, and the alternatives they reject
- [docs/agents/design-notes.md](./docs/agents/design-notes.md): why the repository is shaped this way, and what it rules out
- [CONTRIBUTING.md](./CONTRIBUTING.md): the contribution flow and the pull request format

## Getting help

Open an issue at [github.com/makursi/personal-skills/issues](https://github.com/makursi/personal-skills/issues).

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md) first. Work on a branch, run the validation command above, and fill all three sections of the pull request template: Summary, Evidence, and Merge Danger.

## License

MIT. See [LICENSE](./LICENSE).
