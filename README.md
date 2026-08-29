# Skills

一组经过整理、可供 Codex 与其他 Agent 工作流复用的自定义 Skills。

## 已收录

中文名称是展示别名；原始 Skill 标识保持不变，避免影响 Agent 触发、安装路径和已有引用。

| 中文名称 | 原始 Skill 标识 | 作用 |
| --- | --- | --- |
| 知识库洁癖 | `knowledge-cleanup` | 在用户明确要求时核对并同步项目文档、规则和 Agent 记忆，清理过期、重复或互相冲突的知识。 |
| 存储空间分析 | `storage-analyzer` | 在 Windows 或 macOS 上只读分析磁盘占用，按风险等级给出清理建议并生成 HTML 报告。 |
| 技能总结 | `skill-zongjie` | 盘点本机自定义 Skills，逐项生成简洁的名称和用途摘要。 |
| 任务书领导 | `领导` | 调研实际项目，把一句话需求整理成 Agent 可以独立执行、验证和断点续跑的目标任务书。 |
| 代码深度讲解 | `代码深度讲解` | 基于 `.understand-anything/knowledge-graph.json` 和实际源码，解释文件、函数或模块的架构位置、依赖关系、数据流与实现逻辑。 |

## 安装

将需要的目录复制到 Codex Skills 目录：

```powershell
Copy-Item -Recurse -LiteralPath '.\skills\skill-zongjie' -Destination "$env:CODEX_HOME\skills"
```

如果没有设置 `CODEX_HOME`，Windows 默认位置通常为：

```text
%USERPROFILE%\.codex\skills
```

安装后重新打开 Codex 任务，让 Skill 目录重新载入。

## 使用原则

- Agent 使用 Skill 前应完整读取对应的 `SKILL.md`。
- 涉及删除、覆盖、发布或外部写入时，仍应遵守当前项目权限和用户确认要求。
- 仓库不保存令牌、密码、私钥、`.env`、运行日志或生成结果。

## 说明

这是首批公开整理版本。个人写作风格、体积较大的 PPT 工具链，以及来源需要进一步核对的第三方 Skills 暂未收录。

