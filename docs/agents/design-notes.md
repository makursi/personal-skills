# 设计决策记录

这份文件记录这个仓库为什么长这样。改结构、改约定之前先读它，避免重新推导已经定下的结论。

四个部分：待决问题、已定分支、未决分支、已否决分支及理由。

## 待决问题

一个个人 AI Agent Skills 仓库，要做到什么程度才算基建完成？

前提约束：只收本人编写的 skill，不收第三方。一期先建基建，再用第一个 skill 验收它：`write-readme` 已落地，`skills/` 不再留空。

原判断「一期只建基建，`skills/` 保持为空」已被推翻：模板、校验、安装与 CI 先后跑通后，链路不再缺待验证的对象；继续留空只会让「基建完成」停在占位物上。第一个真实 skill 才是这套基建的验收对象，写它并装进消费目录是本期的收尾动作。

分发面与安装面已定，下一处分叉是 skill 变多之后的目录与索引。

## 已定分支

| # | 决策 | 结论 | 理由 |
|---|---|---|---|
| 1 | 仓库身份 | 唯一真源。skill 只在这里写，单向安装到消费目录 | 双向同步必然冲突。现有 84 个全局 skill 是第三方实体副本，与本仓库职责不重叠 |
| 2 | 收录范围 | 只收本人编写的 skill | 第三方 skill 重发布到 public 仓库有授权风险，且带来维护负担 |
| 3 | 一期内容 | 先建骨架，再用第一个 skill 验收；不预先囤 skill | 先验证模板、校验、安装整条链路，链路通了再往里搬东西 |
| 4 | 脚本语言 | Python 校验 + Node 安装，不写 bash | 主环境是 Windows + pwsh；校验要同时跑在本机和 Ubuntu CI |
| 5 | 文档语言 | `SKILL.md` frontmatter 英文、正文中文 | 触发靠 `description` 匹配，英文命中稳；正文自己维护，中文更快 |
| 6 | 仓库布局 | 保留 `skills/` 一层，skill 平铺 | 划出仓库设施与内容的边界，安装脚本只扫一个目录 |
| 7 | 分类方式 | 目录不分类，靠 `metadata.tags` | 消费者按 `description` 匹配而非路径；分类目录会强迫每次新建都回答归类问题 |
| 8 | 校验严格度 | 硬失败 5 条，其余告警 | CI 拦结构性错误，不统一文风 |
| 9 | 模板深度 | `SKILL.md` + 三个空目录 + `.gitkeep` | 空目录本身是规范的一部分，告诉写作者资料放哪 |
| 13 | LICENSE | MIT | 与 antfu/skills、humanlayer/skills 一致 |
| 14 | 远端 | `github.com/makursi/personal-skills`，public，`main` | 已建 |
| 15 | 首个提交 | 只做本地 commit，push 由本人执行 | public 仓库的首个提交定调，且凭据交互失败会留半截状态 |
| 16 | Issue tracker | GitHub Issues，用 `gh` CLI | 远端本来在 GitHub，`gh` 已安装 |
| 17 | Agent 约定文件 | 只建 `AGENTS.md`，不建 `CLAUDE.md` | 本仓库服务于 DeepSeek Harness，不绑定 Claude Code |
| 18 | Triage 标签 | 保留五个默认角色，标签串与角色同名 | 仓库新建，没有历史标签要兼容 |
| 19 | Domain docs | single-context：根 `GLOSSARY.md` + `docs/adr/` | 仓库没有 monorepo 信号 |
| 20 | `docs/agents/*.md` 语言 | 英文，与 skill 种子模板逐字一致 | `/triage` 会按字面读 `PRs as a request surface: yes` 这类开关，翻译有解析风险 |
| 21 | 外部 PR 作为 triage 入口 | 开启，`PRs as a request surface: yes` | 仓库公开，外部 PR 是真实需求来源；开关就在 `docs/agents/issue-tracker.md`，一个词就能关掉 |
| 22 | `GLOSSARY.md` 与 `docs/adr/` | 现在就建，不等懒创建 | 术语和难回退的决定已经存在，留空目录没有意义 |
| 23 | PR 体例 | 三节：Summary、Evidence、Merge Danger，含 Door 与 Blast Radius | 落到 `.github/pull_request_template.md`，GitHub 新建 PR 时自动填充 |
| 24 | 第一个 skill 的 invocation | user-invoked：`disable-model-invocation: true`，`description` 只留一句给人读的用途说明 | 只在显式输入时生效，不占每次会话的上下文，也不会被 Agent 自行触发去改别人仓库；代价是只能靠人记住它 |
| 25 | README 骨架 | 固定 H2 顺序，分必写六节与条件小节两层；`assets/README-template.md` 是唯一骨架 | 顺序固定才让两次产出可比；条件小节按项目类型出现，不适用就整节省略，不为过检查填占位 |
| 26 | 验收分工 | 脚本判机械项，正文自检清单判语义项 | 链接目标、体积、手写目录不靠 Agent 自信；内容真假、命令可执行、状态一致仍由人读，脚本刻意不越界 |
| 27 | 不加 ADR | 只记入这份设计决策记录，不建 `docs/adr/` 条目 | 固定小节顺序是双向门：改它只是改一张表和一份模板，够不上 ADR 的门槛 |
| 28 | 与 `zh-tech-writing` 的边界 | 互不调用，也不复制它的规则 | 这个 skill 产出英文 README，`zh-tech-writing` 管中文文风；方向相反，复制只会带来对不上的约束 |
| 29 | 本仓库 README 的语言与骨架 | 根 `README.md` 用英文，按本 skill 的固定 H2 骨架写 | 仓库 README 正是这个 skill 要治理的产物，先在自己的 README 上跑一遍才算验证规则；`docs/agents/design-notes.md` 与 skill 正文仍用中文 |
| 30 | 分发命令 | `npx skills add makursi/personal-skills -g`，装进消费目录 `~/.agents/skills` | 官方 `skills` CLI 是平台认可的安装路径；一条命令跨机器，junction 与符号链接做不到 |
| 31 | 安装器数量 | 只留 `skills` CLI 一个安装器，仓库自带的 `scripts/install-skills.mjs` 随后删除 | 两套安装器会各自演化出不同的消费目录形状，排错时先要判断是哪套装的 |
| 32 | `metadata.scope` | 从 frontmatter 移除；装全局还是项目级由 `npx skills add -g` 决定 | 安装作用域是消费者当下的选择，不该由 skill 作者在 frontmatter 里预先声明 |
| 33 | skill 命名 | 不加仓库名前缀，直接用 skill 名 | skill 名同时是调用名，前缀会污染它；本仓库的 skill 名已足够独特，冲突风险不值得让每个名字变长 |
| 34 | 版本 | 跟随 `main`，不打 tag、不发版本号 | 个人仓库没有兼容矩阵要维护；CLI 取仓库最新状态，版本号只会多一层要同步的元数据 |

## 未决分支

暂时没有。新问题出现时在这里追加，并写清依赖哪条已定决策。

## 已否决分支

| 分支 | 否决理由 |
|---|---|
| 全量迁入 84 个第三方 skill | 授权风险；82 个已查到上游出处（antfu/skills、Matt Pocock、humanlayer、vercel、vuejs-ai）；批改未读代码会成为维护负担 |
| 把第三方 skill 登记进仓库做“外部依赖清单” | 一期不讨论具体 skill；且第三方继续由 skills.sh 按 lock 管理已足够 |
| 自建 skill 也登记进 `.skill-lock.json` | 会被同一安装器按 hash 覆盖手写内容 |
| 自建 skill 装到独立目录 `~/.agents/skills-local` | 需要改消费端配置来合并两个目录，绕过标准 |
| 安装脚本用 bash | 主环境是 Windows，与 CI 的 Ubuntu 也不是同一套路径语义 |
| 按领域分类目录（development / documentation / research / productivity） | 一个 skill 常常同时属于两类；分类是给人看的，消费者不看路径 |
| `install-skills.sh`（产品文档原方案） | 与操作系统不符，改为 `install-skills.mjs` |
| 建 `CLAUDE.md` | 本仓库不绑定 Claude Code，两份约定会漂移 |
| 本地 markdown issue tracker（`.scratch/`） | `gh` 跑不动是沙箱审批问题，不是架构问题；public 仓库下两种方案的暴露面相同 |
| 用 `code-review` 之外的自动化测试跑 skill 执行效果 | 一期没有 skill 可测，等有内容再补 |
| 安装方式：Windows junction / POSIX 目录符号链接（原已定 #10） | 对外分发要求别人能把仓库装到自己机器上，junction 与目录符号链接都跨不了机器，路径钉死在作者本机 |
| 安装作用域由 `metadata.scope` 驱动（原已定 #11） | 字段随复制安装一起作废：装全局还是项目级改由 `npx skills add -g` 当场决定，不再写进 frontmatter |
| 自建 skill 继续走 junction、不登记进 `.skill-lock.json`（原已定 #12） | 安装已改成 CLI 的复制安装，CLI 只做复制与锁管理；不登记就落在它的管理之外 |
