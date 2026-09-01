---
name: code-modification-safety-auto
description: "Automated workflow for verifying code safety before modifications - prevents breaking changes"
---

## Trigger
Use this workflow when making changes to existing code - it will automatically verify safety.

## How It Works

This is an **automated workflow** (not just a checklist). It runs in 3 phases:

### Phase 1: Analyze
- Reads the complete file structure
- Identifies all functions, variables, and imports
- Maps dependencies and what depends on this code
- Creates a detailed code analysis

### Phase 2: Verify  
- Adversarially reviews the analysis for safety
- Identifies potential breaking changes
- Assesses risk level: LOW, MEDIUM, HIGH, CRITICAL
- Generates warnings about specific dangers

### Phase 3: Report
- Generates comprehensive safety report
- Provides actionable recommendations
- **BLOCKS changes if risk is HIGH or CRITICAL**
- Clears changes if risk is LOW or MEDIUM (with recommendations)

## Usage

**Before making code changes:**
1. Invoke this workflow
2. Provide file path and type of changes planned
3. Get automated safety verdict
4. Follow recommendations before proceeding

## Key Features

✅ **Automatic Dependency Detection** - finds what's connected
✅ **Adversarial Verification** - agents try to REFUTE safety claims
✅ **Risk Assessment** - clear risk levels and recommendations  
✅ **Breaking Change Prevention** - blocks dangerous modifications
✅ **Detailed Reporting** - know exactly what's at risk

## Risk Levels

- **LOW**: Safe to proceed with changes
- **MEDIUM**: Proceed with recommendations
- **HIGH**: Review carefully, may need refactoring
- **CRITICAL**: ⛔ BLOCK - Do not modify without major rework

## Output

The workflow returns:
- ✅ `safe_to_proceed` - boolean verdict
- 📊 `risk_level` - severity assessment
- 🔗 `dependencies_found` - count of dependencies
- ⚠️ `warnings` - specific breaking change risks
- 💡 `recommendations` - how to modify safely
- 📋 `full_analysis` - detailed technical analysis

## The Principle

**Don't break existing code!**

This workflow enforces it through automation - before you can make changes, you get a detailed safety verification that prevents mistakes.
