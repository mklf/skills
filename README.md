# self-skills

自定义的 Claude / Agent 技能（Skill）合集，附带一个将技能目录打包为 zip 的工具脚本。

每个技能是一个独立目录，内含 `SKILL.md`（技能定义，含 YAML frontmatter 的 `name` / `description`）以及可选的辅助脚本。

## 技能列表

### `leetcode/`
LeetCode 启发式教学技能（Python 3）。扮演资深算法教授，采用苏格拉底式追问引导学生自己解题：

- 只出 Medium/Hard 原题，默认延续同一知识点连续训练。
- 严格防剧透：用户明确求答案前，不输出思路、伪代码或参考答案。
- 提供完整题目描述与可直接运行的 Python 3 + pytest 代码框架。
- 通过 `scripts/manage_records.py` 维护出题记录（防重复）和卡壳记录（供复习）。

记录管理脚本用法：

```bash
# 出题前查重（支持多个题号）
python ./scripts/manage_records.py exists --id 42 56 239

# 记录已出题 / 卡壳
python ./scripts/manage_records.py add-issued --id 42
python ./scripts/manage_records.py add-struggle --id 42

# 批量删除记录
python ./scripts/manage_records.py delete-issued --id 42 56 239
python ./scripts/manage_records.py delete-struggle --id 42 56 239
```

记录存放于 `leetcode/leetcode.json`（已出题）和 `leetcode/leetcode_struggle.json`（卡壳）。

### `read-arxiv-paper/`
读取 arxiv 论文的技能。给定 arxiv URL，下载论文的 **TeX 源码**（而非 PDF），解压后定位入口文件（如 `main.tex`），递归阅读全部源文件，最终产出一篇详尽、易读的 Markdown 介绍。

## 工具脚本

### `package_skill.py`
将一个技能目录打包成 zip 归档（自动跳过 `.DS_Store` 与 `__pycache__`），便于分发或安装。

```bash
# 输出到 <当前目录>/<skill_name>.zip
python package_skill.py leetcode

# 指定输出路径
python package_skill.py read-arxiv-paper --output /path/to/out.zip
```

## 目录结构

```
.
├── leetcode/
│   ├── SKILL.md
│   └── scripts/
│       └── manage_records.py
├── read-arxiv-paper/
│   └── SKILL.md
├── package_skill.py
└── README.md
```
