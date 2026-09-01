---
name: code-modification-safety
description: "Safety checklist for modifying existing code without breaking functionality"
---

## Trigger
Use this skill when making changes to existing code in any project.

## Steps

### 1. Read Full Context
- [ ] Read the complete file before making any changes
- [ ] Understand the overall structure and purpose
- [ ] Note all function definitions and dependencies
- [ ] Check what other files import or use this code

### 2. Identify Dependencies
- [ ] List all functions/variables that this code depends on
- [ ] List all functions/variables that depend on this code
- [ ] Check for side effects or global state changes
- [ ] Verify import statements and external dependencies

### 3. Plan Minimal Changes
- [ ] Make the smallest possible change to achieve the goal
- [ ] Avoid refactoring unrelated code
- [ ] Keep the same function signatures if possible
- [ ] Preserve variable names and structure

### 4. Make Changes
- [ ] Use Edit tool (not Write) to modify specific sections
- [ ] Change only what needs to be changed
- [ ] Add comments explaining why changes were made
- [ ] Keep existing comments intact

### 5. Verify No Breakage
- [ ] Check that all function calls still work
- [ ] Verify return types haven't changed unexpectedly
- [ ] Confirm imports still resolve correctly
- [ ] Test related functionality if possible
- [ ] Review the diff to ensure nothing unintended changed

### 6. Document Changes
- [ ] Explain what was changed and why
- [ ] Note any breaking changes (if unavoidable)
- [ ] Update version numbers or changelogs if applicable

## Key Principles

**Never:** 
- Overwrite files unnecessarily (use Edit, not Write)
- Change unrelated code
- Remove working functionality
- Break existing dependencies

**Always:**
- Read before editing
- Make minimal targeted changes
- Verify nothing broke
- Document your changes

## The Rule
**"Уже написанный код не ломаем!"** (Don't break existing code!)

This is the first rule of development. Every change should preserve existing functionality while adding or fixing features.