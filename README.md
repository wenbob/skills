# Skills

一组经过整理、可供 Codex 与其他 Agent 工作流复用的自定义 Skills。

## 已收录

| Skill | 作用 |
| --- | --- |
| `knowledge-cleanup` | 在项目收尾时核对代码、项目文档与 Agent 记忆，减少文档陈旧和上下文漂移。 |
| `storage-analyzer` | 在 Windows 或 macOS 上只读分析磁盘占用，并按风险等级生成清理建议。 |
| `skill-zongjie` | 盘点本机自定义 Skills，并生成简洁的功能摘要。 |
| `领导` | 把一句话需求整理成 Agent 可以独立执行、验证和续跑的目标任务书。 |

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

