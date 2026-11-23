# 审计报告格式

开头两行交代审计对象：

```text
目标目录：<仓库根，或指定的子包路径>
被审计文件：README.md（<n> 行）/ 不存在
```

正文一张表，一个小节一行：

| 列 | 填什么 |
|---|---|
| 小节 | 骨架里的小节名 |
| 现状 | 有 / 缺 / 不准确 / 不适用，定义见 `SKILL.md`「审计」 |
| 证据 | 一条可核对的事实，形状见范例；缺写「无」 |
| 建议动作 | 保留 / 改写 / 新增 / 删除 |

动作词的含义：

- **保留**：准确，不需要改。
- **改写**：写出换成哪条事实，以及事实的来源。
- **新增**：写出要落的事实与来源。
- **删除**：过期，且没有来源可以替代。
- 条件小节不成立：现状「不适用」，证据写缺的条件，动作「—」。

表后列待确认问题：

```text
## 待确认

- <事实>：清单里查不到，问人。
```

## 范例：本仓库

```text
目标目录：仓库根
被审计文件：README.md（61 行）
```

| 小节 | 现状 | 证据 | 建议动作 |
|---|---|---|---|
| 开篇 | 有 | `README.md:1-3`：标题加两句，说清是什么、为什么 | 保留 |
| 徽章与截图 | 不适用 | 未发布到包管理器：根目录无 `package.json`，`git remote -v` 只有 `origin https://github.com/makursi/personal-skills.git`；无界面 | — |
| Status | 不准确 | `README.md:5` 称「`skills/` 里还没有 skill」，而 `skills/write-readme/` 已存在 | 改写：换成一行维护状态，删掉「只有基建」 |
| Getting started | 有 | `README.md:20-32`；两条命令对应的 `scripts/validate-skills.py:153` 与 `scripts/install-skills.mjs:64` 都在，退出码 0 | 保留 |
| Usage | 不准确 | `README.md:34-40` 只有复制命令和一句下一步，没有预期输出 | 改写：补一条预期结果（复制模板后校验通过） |
| Configuration | 不适用 | 无配置文件；`scripts/` 的两个脚本不读 `environ` / `process.env` | — |
| Architecture | 不准确 | `README.md:9-18` 的结构树漏了根目录的 `GLOSSARY.md`、`LICENSE` 与 `docs/adr/`（三者都在） | 改写：结构树补齐 |
| Documentation | 有 | `README.md:57-61` 的五个相对链接目标全部存在 | 保留 |
| Getting help | 缺 | `README.md:1-61` 没有 issue、讨论区或联系人；`git remote -v` 给出 GitHub 地址 | 新增：GitHub Issues 链接；联系人待问 |
| Contributing | 有 | `README.md:40` 指向 `CONTRIBUTING.md`，`CONTRIBUTING.md:42-50` 有 PR 体例 | 保留 |
| License | 缺 | `README.md:1-61` 没有 License 小节；`LICENSE:1` 是 MIT | 新增：一行 MIT + `[LICENSE](./LICENSE)` |
| 尾部致谢 | 不适用 | 无 citation 文件，也没有相关项目声明 | — |

## 待确认

- 维护状态：`README.md:5` 暗示未完成，是实验性还是维护中？清单查不到意图，问人。
- 维护者联系方式：Getting help 要写的人或频道。
- 是否对外发布：决定徽章要不要出现。
