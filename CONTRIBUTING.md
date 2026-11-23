# 贡献流程

## 安装与更新

安装走官方 `skills` CLI，一条命令：

```bash
npx skills add makursi/personal-skills -g
```

`-g` 是全局安装，落在 `~/.agents/skills`，这是唯一保证存在的消费目录。CLI 还会按探测结果往 Claude Code、Cursor 等目录写入，装哪些平台由它在交互里问你。省略 `-g` 则装进当前项目。

- 固定到某个 commit 或分支：`npx skills add makursi/personal-skills@<commit 或分支>`
- 只装一个 skill：`--skill <name>`
- 名字冲突时改名：`--rename <name>`
- Windows 上符号链接失败时 CLI 退回复制；要链接成功需开启开发者模式（Developer Mode）

`skills update` 会删除并重建目标目录，消费者在副本上的手改会随之丢失。要改就把改动提回本仓库。

CLI 的源取自 GitHub 的 `main`。没 push 的本地改动不会进入消费目录。作者流程：

1. 改 `skills/<name>/` 里的文件
2. 跑 `python scripts/validate-skills.py`，退出码 0
3. 提交并 push 到 `main`
4. 跑 `npx skills update -g`
5. 抽查一个装好的文件，例如 `~/.agents/skills/write-readme/SKILL.md`

忘记第 4 步，消费目录仍是旧副本，也不会报错。

作者本机有两个已知问题：

- `npx` 在 `C:\Users\29634\Desktop\W` 这个目录树下跑不起来：上层 workspace 的 `package.json` 声明了 `devEngines.packageManager: pnpm`，`npx` 直接拒绝。要在该目录树之外执行。
- CLI 拉起的子 git 进程不读全局 git 配置里的代理。先设 `HTTP_PROXY` 和 `HTTPS_PROXY`（当前是 `http://127.0.0.1:11888`）。

## 新增 skill

1. 复制模板：`cp -r templates/skill-template skills/<skill-name>`
2. 改 frontmatter：`name` 与目录名一致，`description` 写清做什么、什么时候用
3. 写正文：何时使用、流程、参考资料
4. 资料放 `references/`，脚本放 `scripts/`，静态资源放 `assets/`
5. 跑 `python scripts/validate-skills.py`，退出码 0 才算通过
6. 提交并 push 到 `main`，再按上一节更新一遍

## frontmatter 字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | 是 | 小写字母、数字、连字符，最长 64 字符，与目录名一致 |
| `description` | 是 | 用英文，不超过 1024 字符，写清做什么和触发场景 |
| `license` | 否 | 默认继承仓库的 MIT |
| `metadata.version` | 否 | 语义化版本 |
| `metadata.tags` | 否 | 分类标签 |
| `disable-model-invocation` | 否 | 设为 `true` 后只能由人显式调用，Agent 不会自己触发 |

## 修改 skill

改仓库里的 `skills/<name>/`，重跑校验，提交并 push 到 `main`，再跑 `npx skills update -g`。消费目录是复制出来的副本，不会跟着仓库即时变化；也不要把消费目录里的改动抄回来。

## 校验规则

硬失败 5 条：

1. frontmatter 能被 YAML 解析
2. `name` 存在，且等于目录名
3. `name` 匹配 `^[a-z0-9-]{1,64}$`
4. `description` 存在，且不超过 1024 字符
5. 正文里 `references/`、`scripts/`、`assets/` 的相对路径真实存在

其余问题只告警：缺 `metadata.tags`、缺 `metadata.version`、正文超过 500 行、没有二级标题、`description` 短于 20 字符。

`--strict` 把告警也当失败。

## Pull request

PR 描述用英文写，按 `/pr` 技能的规范填，三节都要有：

- **Summary**：用文件树、diff 或流程图说清改了什么，选最快看懂的形状。
- **Evidence**：改前和改后的真实输出，贴命令结果。写“已验证”不算。
- **Merge Danger**：说明是单向门还是双向门，以及影响面。

外部 PR 会进 triage 队列，标签约定见 `docs/agents/triage-labels.md`。

## 提交信息

一行说清改了哪个 skill、改了什么行为。
