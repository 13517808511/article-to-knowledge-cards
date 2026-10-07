# make-knowledge-cards

把一篇文章转换成 **5–8 张知识卡片**的 Agent Skill，遵循 [Agent Skills](https://agentskills.io/specification) 开放规范（MIT 许可）。

- 输入：直接粘贴的文章，或本地 `.md` / `.markdown` / `.txt` 文件
- 每张卡片只讲一个知识点，包含：**标题、核心知识、简明解释、示例或自测**
- 只提取原文中真正重要的信息：去重、不编造；原文信息不足时不凑数（3–4 张并附说明，或直接告知内容过少）
- 暂不支持：网页抓取、PDF/Word 等文档解析、Anki 导出、图形界面

## 使用方法

在支持 Agent Skills 的客户端（Codex、TRAE 等）加载 `skills/make-knowledge-cards` 目录，然后：

- 直接粘贴文章，并要求"做成知识卡片"；或
- 提供本地 `.md` / `.markdown` / `.txt` 文件的路径

默认在对话中输出卡片；需要保存时可要求写入 `<文件名>.cards.md`。

## 输入输出示例

输入（粘贴文本或文件内容）：

```text
周报要写本周产出的结果，而不是罗列"做了什么"的过程。
结果尽量用数据量化，例如"接口平均响应时间从 800ms 降到 320ms"，
比"优化了接口性能"更有说服力。
```

输出：

```markdown
# 知识卡片：写周报

### 1. 写结果而非罗列过程
- **核心知识：** 周报要写本周产出的结果，而不是罗列"做了什么"的过程。
- **简明解释：** 结果描述产出了什么，过程描述做了哪些动作；周报要求写前者。
- **示例或自测：** 自测："优化了接口性能"这句话写的是结果还是过程？

### 2. 用数据量化结果
- **核心知识：** 结果应尽量用数据量化表达。
- **简明解释：** 量化让改进幅度可以被直接判断，比笼统的定性描述更有说服力。
- **示例或自测：** "接口平均响应时间从 800ms 降到 320ms"比"优化了接口性能"更有说服力。
```

完整输入输出样例见 `examples/`（中文粘贴长文、英文 Markdown、信息不足的短文）。

## 目录结构

```text
skills/make-knowledge-cards/      技能本体
├── SKILL.md                      技能指令（含输出格式与硬规则）
├── agents/openai.yaml            UI 元数据
├── scripts/validate_cards.py     卡片结构校验器（Python 标准库，无第三方依赖）
└── LICENSE.txt                   MIT
examples/                         三类文章的输入与卡片输出样例
tools/skill-creator/              开发用的官方 skill-creator 工具（Apache-2.0，来源 openai/skills）
```

校验命令：

```shell
# 校验技能结构（需要 PyYAML）
uv run --with pyyaml python tools/skill-creator/scripts/quick_validate.py skills/make-knowledge-cards

# 校验一份卡片是否符合格式契约
uv run python skills/make-knowledge-cards/scripts/validate_cards.py examples/outputs/01-feynman-cards.md
```
