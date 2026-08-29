---
name: context-map
description: '项目上下文梳理：在修改代码前定位与任务相关的文件、依赖、测试和现有模式。适用于新增功能、修复缺陷和重构前的影响分析。'
---

# Context Map

Before implementing any changes, analyze the codebase and create a context map.

## Task

{{task_description}}

## Instructions

1. Search the codebase for files related to this task
2. Identify direct dependencies (imports/exports)
3. Find related tests
4. Look for similar patterns in existing code

## Output Format

```markdown
## Context Map

### Files to Modify
| File | Purpose | Changes Needed |
|------|---------|----------------|
| path/to/file | description | what changes |

### Dependencies (may need updates)
| File | Relationship |
|------|--------------|
| path/to/dep | imports X from modified file |

### Test Files
| Test | Coverage |
|------|----------|
| path/to/test | tests affected functionality |

### Reference Patterns
| File | Pattern |
|------|---------|
| path/to/similar | example to follow |

### Risk Assessment
- [ ] Breaking changes to public API
- [ ] Database migrations needed
- [ ] Configuration changes required
```

Do not proceed with implementation until this map is reviewed.
