# 贡献流程

## 新增 skill

1. 复制模板：`cp -r templates/skill-template skills/<skill-name>`
2. 改 frontmatter：`name` 与目录名一致，`description` 写清做什么、什么时候用
3. 写正文：何时使用、流程、参考资料
4. 资料放 `references/`，脚本放 `scripts/`，静态资源放 `assets/`
5. 跑 `python scripts/validate-skills.py`，退出码 0 才算通过
6. 提交

## frontmatter 字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | 是 | 小写字母、数字、连字符，最长 64 字符，与目录名一致 |
| `description` | 是 | 用英文，不超过 1024 字符，写清做什么和触发场景 |
| `license` | 否 | 默认继承仓库的 MIT |
| `metadata.version` | 否 | 语义化版本 |
| `metadata.tags` | 否 | 分类标签 |
| `metadata.scope` | 否 | `global` 或 `project:<name>`，决定装到哪 |
| `disable-model-invocation` | 否 | 设为 `true` 后只能由人显式调用，Agent 不会自己触发 |

## 修改 skill

直接改仓库里的文件，然后重跑校验。消费目录里的链接是 junction，不需要重新安装。

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

PR 描述按 [`.github/pull_request_template.md`](./.github/pull_request_template.md) 填，三节都要有：

- **Summary**：用文件树、diff 或流程图说清改了什么，选最快看懂的形状。
- **Evidence**：改前和改后的真实输出，贴命令结果。写“已验证”不算。
- **Merge Danger**：说明是单向门还是双向门，以及影响面。

外部 PR 会进 triage 队列，标签约定见 `docs/agents/triage-labels.md`。

## 提交信息

一行说清改了哪个 skill、改了什么行为。
