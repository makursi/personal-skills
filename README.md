# Personal Skills Repository

我自己的 AI Agent Skills 仓库。skill 在这里编写，这里是唯一真源，再安装到各 Agent 的 skills 目录。

## 目录结构

```text
.
├── AGENTS.md                  # Agent 在本仓库的约定
├── CONTRIBUTING.md            # 给人看的贡献流程
├── docs/agents/               # Agent 读取的约定文件
├── skills/                    # 唯一真源，一个目录一个 skill
│   └── write-readme/          # 按固定骨架写仓库 README
├── templates/skill-template/  # 新 skill 的起点
├── scripts/                   # 校验与安装
└── .github/workflows/         # CI
```

## 快速开始

校验全部 skill：

```bash
python scripts/validate-skills.py
```

试运行安装，不写磁盘：

```bash
node scripts/install-skills.mjs --dry-run
```

## 新建一个 skill

```bash
cp -r templates/skill-template skills/<skill-name>
```

然后改 `SKILL.md` 的 frontmatter 和正文，规则见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 约定

| 项 | 规则 |
|---|---|
| 目录名 | 小写字母、数字、连字符，最长 64 字符，与 frontmatter 的 `name` 一致 |
| frontmatter | 用英文。`name` 和 `description` 必填，`description` 不超过 1024 字符 |
| 正文 | 用中文 |
| 参考资料 | 放 `references/`，按需读取，不整段塞进 `SKILL.md` |
| 脚本 | 放 `scripts/` |
| 静态资源 | 放 `assets/` |

安装到 `~/.agents/skills` 用的是目录 junction，指向本仓库。改了仓库里的文件，Agent 立刻看到新版本。

## 文档

- [AGENTS.md](./AGENTS.md)：Agent 动手前读的约定
- [GLOSSARY.md](./GLOSSARY.md)：仓库用词，写文档和 PR 时对齐说法
- [docs/adr/](./docs/adr/)：难以回退的决定，以及否决掉的替代方案
- [docs/agents/design-notes.md](./docs/agents/design-notes.md)：为什么这样设计，以及对哪些做法说不
- [CONTRIBUTING.md](./CONTRIBUTING.md)：新增和修改 skill 的流程，以及 PR 体例
