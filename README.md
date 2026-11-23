# Personal Skills

A personally authored collection of Agent Skills, published so anyone can install it. Installation is handled by the official [`skills` CLI](https://github.com/vercel-labs/skills): the skill files are copied into the canonical `~/.agents/skills` directory, and each per-agent directory links to that copy, or gets a copy too when linking is unavailable. This repository remains the single place where the skills are written.

## Status

Maintained.

## Getting started

Requires Node.js 22.20 or newer for the `skills` CLI, and Python 3.13 with PyYAML to run the repository scripts.

Install the collection globally:

```bash
npx skills add makursi/personal-skills -g
```

`-g` puts the skills in `~/.agents/skills`, the only destination guaranteed to exist. For other agents (Claude Code, Cursor, and so on) the CLI targets the agents it detects; it asks which platforms to install only when it must, and a non-interactive run (`-y`) picks for you. List what is installed:

```bash
npx skills list -g
```

## Usage

Run the `write-readme` skill's checker against this repository:

```bash
python skills/write-readme/scripts/check-readme.py .
```

```text
README：README.md（仓库根目录）

0 个违规。
检查通过。
```

To add or change a skill, follow [CONTRIBUTING.md](./CONTRIBUTING.md).

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
├── scripts/                   # skill validation
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

Read [CONTRIBUTING.md](./CONTRIBUTING.md) first. Work on a branch, run `python scripts/validate-skills.py`, and fill all three sections of the pull request template: Summary, Evidence, and Merge Danger.

## License

MIT. See [LICENSE](./LICENSE).
