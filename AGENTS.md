# AGENTS.md

在这个仓库里改动文件前，先读这份约定。

## 唯一真源

`skills/<name>/` 是 skill 的唯一真源。要改 skill 就改这里，不改 `~/.agents/skills` 里的副本。

安装方向只有一条：仓库 → 消费目录，由 `scripts/install-skills.mjs` 完成。复制回来的做法会制造冲突。

## 改完就跑校验

改动 `skills/` 下任何文件后运行：

```bash
python scripts/validate-skills.py
```

退出码 0 才算完成。告警不拦提交，但先看一遍再决定改不改。要一次看全就加 `--strict`，它把告警也当失败。

## 新增 skill 的流程

1. `cp -r templates/skill-template skills/<name>`
2. 写 `SKILL.md`：frontmatter 用英文，正文用中文
3. 资料放 `references/`，脚本放 `scripts/`，静态资源放 `assets/`
4. 跑校验

## Pull request

PR 描述一律用英文写，并按 `/pr` 技能的规范成型：`Summary`、`Evidence`、`Merge Danger` 三节都要有，缺一节即不合格。

- `Summary` 选最小视图说清改了什么，别用散文复述 diff。
- `Evidence` 给改前和改后的真实输出；写“已验证”不算证据。
- `Merge Danger` 写明 Door 和 Blast Radius。

模板在 `.github/pull_request_template.md`，与 `/pr` 技能同构；用词取 `GLOSSARY.md`。

## 文档指针

- `GLOSSARY.md`：仓库用词。输出里用这里的词，不用 `_Avoid_` 列的别称。
- `docs/adr/`：难以回退的决定和理由。改架构前读一遍，别推翻已经定下的取舍。
- `.github/pull_request_template.md`：写 PR 描述用，三节都要填。
- `docs/agents/design-notes.md`：设计决策与理由。要动仓库结构或新增约定前读它。
- `docs/agents/issue-tracker.md`：issue 落在哪、怎么读写。
- `docs/agents/triage-labels.md`：五个 triage 角色对应的标签串。
- `docs/agents/domain.md`：`GLOSSARY.md` 与 ADR 的读取规则。
- `CONTRIBUTING.md`：给人看的贡献流程。
- `README.md`：仓库定位与目录说明。

## Agent skills

### Issue tracker

Issues 在 GitHub 的 `makursi/personal-skills`，用 `gh` 读写。见 `docs/agents/issue-tracker.md`。

### Triage labels

五个 canonical triage 角色，标签串与角色同名。见 `docs/agents/triage-labels.md`。

### Domain docs

single-context：根目录的 `GLOSSARY.md` 加 `docs/adr/`。见 `docs/agents/domain.md`。
