---
name: code-review-expert
description: Comprehensive code review expertise. Use when reviewing code, evaluating architecture, or assessing quality. Triggers on review, evaluate, assess, audit, code quality, best practices.
metadata:
  codex_migration: '2026-06-27'
  source_path: skills/.curated/claude-main/.claude/skills/code-review-expert/SKILL.md
---

# Code Review Expert

## Codex compatibility

- Legacy Claude-specific tool names or paths are conceptual; use Codex shell/editor capabilities and the local `.agents/skills` path.


Comprehensive code review expertise for evaluating architecture and quality.

## When to Use

- Reviewing code changes before merge
- Evaluating architecture decisions
- Assessing code quality
- Auditing for security issues
- Performing pre-commit reviews

## Workflow

### Step 1: Initial Scan (10%)

Review structure and architecture overview.

### Step 2: Top-Down Review (40%)

Architecture → Modules → Functions.

### Step 3: Multi-Perspective (30%)

Review as Architect, PM, QA, UX.

### Step 4: Deep Dives (15%)

Focus on security and performance.

### Step 5: Report (5%)

Summarize and prioritize findings.

---

## Review Phases
```
Phase 1 (10%): Initial scan - structure, architecture
Phase 2 (40%): Top-down - Architecture → Modules → Functions
Phase 3 (30%): Multi-perspective - Architect, PM, QA, UX
Phase 4 (15%): Deep dives - Security, performance
Phase 5 (5%):  Report - Summarize, prioritize
```

## Severity

| Level | Action |
|-------|--------|
| 🔴 Critical | Must fix before deploy |
| 🟠 High | Fix this sprint |
| 🟡 Medium | Fix next sprint |
| 🟢 Low | Backlog |

## Quick Checklist

- [ ] No `any` types
- [ ] Error handling complete
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] Parameterized queries
- [ ] Async errors handled
