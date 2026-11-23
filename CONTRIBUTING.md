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

直接改仓库里的文件，然后重跑校验。安装目录是 junction，不需要重新安装。

## 校验规则

硬失败 5 条：

1. frontmatter 能被 YAML 解析
2. `name` 存在，且等于目录名
3. `name` 匹配 `^[a-z0-9-]{1,64}$`
4. `description` 存在，且不超过 1024 字符
5. 正文里 `references/`、`scripts/`、`assets/` 的相对路径真实存在

其余问题只告警：缺 `metadata.tags`、缺 `metadata.version`、正文超过 500 行、没有二级标题、`description` 短于 20 字符。

`--strict` 把告警也当失败。

## 提交信息

一行说清改了哪个 skill、改了什么行为。
