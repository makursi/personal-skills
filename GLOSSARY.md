# Personal Skills Repository

这个仓库存放我自己编写的 Agent Skills。名字界定了范围：个人、可复用、跨 Agent 共享。

## 语言

**Skill**：
一个目录，含 `SKILL.md`，描述一种可复用的能力。
_Avoid_：技能包、插件、prompt 模板

**SKILL.md**：
Skill 的入口文件，由 frontmatter 和正文组成。
_Avoid_：skill.md、README、main.md

**frontmatter**：
`SKILL.md` 顶部的 YAML 块，承载触发条件和元数据。
_Avoid_：头部、metadata（那是它的一个子键）

**description**：
frontmatter 中决定 Skill 何时被触发的字段，用英文写。
_Avoid_：摘要、介绍、desc

**渐进式加载**：
正文只写指针，资料放 `references/` 按需读取的做法。
_Avoid_：分层加载、懒加载

**唯一真源**：
定义 Skill 的唯一位置。本仓库的 `skills/` 是唯一真源。
_Avoid_：主副本、基准版本

**分发**：
让仓库外的人拿到并安装 Skill 的途径。
_Avoid_：发布、同步、导出

**安装**：
把 Skill 从唯一真源落到某个消费目录的动作，方向只有一条。
_Avoid_：同步、部署、分发

**复制安装**：
安装时在消费目录生成独立副本，副本与真源的一致性由安装器负责。
_Avoid_：拷贝安装、导出安装

**链接安装**：
安装时在消费目录生成指向真源的链接，改真源即时生效。
_Avoid_：软链安装、挂载安装

**消费目录**：
Agent 读取 Skill 的目录，是安装的终点。
_Avoid_：目标目录、安装目录

**第三方 Skill**：
由别人编写、通过外部管理器安装的 Skill，不属于本仓库。
_Avoid_：外部 skill、公共 skill

## 协作

**triage 角色**：
五个固定的协作状态：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。
_Avoid_：状态机、流程状态

**Door**：
合入后的可回退性。单向门不可回退，双向门可回退。
_Avoid_：风险等级、危险程度

**Blast Radius**：
改动波及的范围，用一个词概括。
_Avoid_：影响范围、波及面
