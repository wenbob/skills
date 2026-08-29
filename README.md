# Skills

一组经过整理、可供 Codex 与其他 Agent 工作流复用的自定义 Skills。

## 已收录

中文名称是展示别名；原始 Skill 标识保持不变，避免影响 Agent 触发、安装路径和已有引用。

| 中文名称 | 原始 Skill 标识 | 作用 |
| --- | --- | --- |
| 数字生命写作 | `digital-life-khazix` | 根据题目、素材或采访内容撰写可直接发布的知乎长回答、公众号文章、热点评论和产品体验文章。 |
| 代码审查 | `code-review` | 从缺陷、安全、性能和可维护性等维度审查代码改动，并按优先级给出可执行建议。 |
| 项目上下文地图 | `context-map` | 在修改代码前定位相关文件、直接依赖、测试覆盖和仓库中的参考实现模式。 |
| 网页应用测试 | `webapp-testing` | 使用真实浏览器验证页面交互、表单流程、响应式表现和控制台日志。 |
| 安全最佳实践 | `安全最佳实践` | 按语言和框架审查安全问题，并给出安全默认的实现与加固建议。 |
| 实施计划 | `create-implementation-plan` | 为新功能、重构、升级、架构或基础设施改动生成分阶段可执行计划。 |
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

仓库同时包含个人定制 Skill 和注明来源的第三方 Skill。第三方作者、来源与许可证情况见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。体积较大的 PPT 工具链及其他未整理 Skill 暂未收录。

