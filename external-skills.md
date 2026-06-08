# 外部 Skill 清单（external-skills.md）

本文件登记**外部仓库提供的 skill**及其安装方式。它面向 agent：当用户要求“安装某个外部 skill”时，agent 读取本文件，按对应条目的步骤自行完成安装，无需再上网查结构。

> 所有 skill 都遵循同一套 **open agent skills 标准**：一个含 `SKILL.md`（YAML frontmatter 至少有 `name` / `description`）的目录。因此同一个 skill 目录对 **Claude Code** 和 **OpenAI Codex** 通用，区别只在放置目录不同（见下表）。

---

## 目标 agent：skill 目录对照

| agent | 个人级（所有项目） | 项目级 |
|-------|------------------|--------|
| **Claude Code** | `~/.claude/skills/` | `<项目>/.claude/skills/` |
| **OpenAI Codex** | `~/.agents/skills/` | `<仓库根>/.agents/skills/` |

手动安装时把 skill 目录拷到对应目录即可；同一个 skill 想给两个 agent 都用，可分别软链到两处。

### Codex CLI 自身的安装（首次使用前）

需要 Node.js ≥ 22，三选一：

```bash
npm install -g @openai/codex                                   # npm
brew install --cask codex                                      # Homebrew
curl -fsSL https://chatgpt.com/codex/install.sh | sh           # 官方脚本（Mac/Linux）
```

装好后跑 `codex` 登录。在会话内用 `$<skill名>` 显式调用、`/skills` 浏览，或任务匹配 `description` 时自动启用。Codex 还内置 `$skill-installer`，可让它直接从仓库下载 skill。

---

## 给 agent 的通用安装流程

对清单中的任意一条，按以下顺序判定安装方式：

1. **优先尝试作为 Claude Code 插件安装。** 检查仓库根是否有 `.claude-plugin/marketplace.json`：

   ```bash
   git ls-remote <repo_url> >/dev/null 2>&1   # 确认可访问
   # 在 Claude Code 中执行斜杠命令：
   #   /plugin marketplace add <owner/repo>
   #   /plugin install <plugin-name>@<marketplace-name>
   ```

   若 `/plugin marketplace add` 报找不到 marketplace，说明该仓库未配置插件，转步骤 2。

2. **退化为手动拷贝 skill 目录。** 每个 skill 是一个含 `SKILL.md` 的目录，按上面「目录对照」表拷到目标 agent 对应的 skills 目录即可被发现：

   ```bash
   git clone <repo_url> /tmp/<name>
   mkdir -p <目标 skills 目录>        # 如 ~/.claude/skills 或 ~/.agents/skills
   cp -R /tmp/<name>/<skills 子路径>/* <目标 skills 目录>/
   ```

   （Codex 仅支持本方式，不走插件 marketplace；其内置 `$skill-installer` 也可从仓库下载。）

3. 安装后告知用户可用的 skill 名称（即各 `SKILL.md` frontmatter 里的 `name`）。

> 默认目标与作用范围：除非用户另有说明，按当前所用 agent 装到**个人级**目录（Claude Code → `~/.claude/skills/`，Codex → `~/.agents/skills/`）。

---

## 清单

### Supervisor-Skills

- **仓库**: https://github.com/HKUSTDial/Supervisor-Skills
- **简介**: HKUST(GZ) Yuyu Luo 沉淀的科研指导 skill 合集，覆盖选题、写作、画图、投稿前评审等。CC BY-NC-SA 4.0。
- **结构**: 按 Claude Code 插件组织，skill 位于 `plugins/phd-research/skills/`。
- **包含的 skill**:
  | name | 用途 |
  |------|------|
  | idea-evaluator | 用 5 维框架评估、打分研究 idea |
  | vibe-research-workflow | 引导 AI 辅助科研（Coding / Figure / Writing）|
  | intro-drafter | 从研究动机生成 Introduction 大纲 |
  | tech-paper-template | 梳理技术型整篇论文逻辑 |
  | benchmark-paper-template | 面向 Benchmark/Evaluation 类论文 |
  | pre-submission-reviewer | 以审稿人视角按 checklist 审阅初稿 |
  | figure-designer | 基于绘图范式给出配图设计建议 |
- **安装方式 A（插件，若可用）**:
  ```
  /plugin marketplace add HKUSTDial/Supervisor-Skills
  /plugin install phd-research@Supervisor-Skills
  ```
- **安装方式 B（手动拷贝，通用）**:
  ```bash
  git clone https://github.com/HKUSTDial/Supervisor-Skills /tmp/supervisor-skills
  # Claude Code: 目标改为 ~/.claude/skills ；Codex: 目标改为 ~/.agents/skills
  mkdir -p ~/.claude/skills
  cp -R /tmp/supervisor-skills/plugins/phd-research/skills/* ~/.claude/skills/
  ```

---

## 新增条目模板

```markdown
### <名称>

- **仓库**: <repo_url>
- **简介**: <一句话>
- **结构**: <skill 所在子路径 / 是否为插件>
- **包含的 skill**: <name 列表或表格>
- **安装方式 A（插件，若可用）**: <命令>
- **安装方式 B（手动拷贝）**: <命令>
```
