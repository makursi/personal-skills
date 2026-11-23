# 审计报告格式

开头两行交代审计对象：

```text
被审计目录：<仓库根目录，或指定的子包路径>
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

## 范例：一个最小 CLI 项目

样例项目叫 `greet`，项目树如下：

```text
greet/
├── LICENSE
├── package.json
└── src/
    └── cli.js
```

它当前的 `README.md` 摘录如下，左侧是行号；证据按这些行号引用，摘录固定在本文件里，不会随任何仓库的改动漂移：

````text
 1 | # greet
 2 |
 3 | Prints a greeting for the name you pass in.
 4 |
 5 | ## Status
 6 |
 7 | Coming soon.
 8 |
 9 | ## Getting started
10 |
11 | Requires Node.js 20 or later.
12 |
13 | ```bash
14 | npm install
15 | node src/cli.js Ada
16 | ```
17 |
18 | ## Usage
19 |
20 | Run it with a name.
21 |
22 | ## Architecture
23 |
24 | ```text
25 | ├── package.json
26 | └── src/cli.js
27 | ```
28 |
29 | ## Contributing
30 |
31 | See CONTRIBUTING.md.
````

```text
被审计目录：仓库根目录
被审计文件：README.md（31 行）
```

| 小节 | 现状 | 证据 | 建议动作 |
|---|---|---|---|
| 开篇 | 有 | `README.md:1-3`：标题加一句话，说清打印问候、输入是名字 | 保留 |
| 徽章与截图 | 不适用 | 项目未发布到包管理器，也没有 CI 或覆盖率服务；纯命令行，无界面 | — |
| Status | 不准确 | `README.md:5-7` 只有一句占位式的 "Coming soon."，没写维护中、实验性还是已弃用 | 改写：问人确认维护意图，换成其中一行状态 |
| Getting started | 有 | `README.md:9-16`：先写 Node.js 20，再给 `npm install` 与 `node src/cli.js Ada`；入口 `src/cli.js` 在项目树里 | 保留 |
| Usage | 不准确 | `README.md:18-20` 只有一句 "Run it with a name."，没有示例和预期输出 | 改写：补 `node src/cli.js Ada` 及输出 `Hello, Ada!` |
| Configuration | 不适用 | `src/cli.js` 只读命令行参数，不读环境变量或配置文件 | — |
| Architecture | 不准确 | `README.md:22-27` 的树漏了根目录的 `LICENSE`，它在项目树里存在 | 改写：结构树补上 `LICENSE` |
| Documentation | 不适用 | 项目树里没有 `docs/`、wiki 或外部站点 | — |
| Getting help | 缺 | `README.md:1-31` 没有 issue 区、讨论区或联系人 | 新增：问人要一个渠道，再写链接 |
| Contributing | 不准确 | `README.md:29-31` 指向 `CONTRIBUTING.md`，项目树里没有这个文件 | 改写：删掉这段指向，或先补 `CONTRIBUTING.md`（问人） |
| License | 缺 | `README.md:1-31` 没有 License 小节；`LICENSE` 在项目根 | 新增：一行 MIT + `[LICENSE](./LICENSE)` |
| 尾部致谢 | 不适用 | 没有 citation 文件，也没有需要致谢的人或相关项目 | — |

## 待确认

- 维护状态：`README.md:5-7` 的 "Coming soon." 是 experimental 还是 maintained？项目树查不到意图，问人。
- 维护者联系方式：Getting help 要写的渠道。
- Contributing：`CONTRIBUTING.md` 要不要建；不建就删掉 `README.md:29-31` 的指向。
