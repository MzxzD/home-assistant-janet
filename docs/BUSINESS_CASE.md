# Janet Home Automation — One Repo Business Case

**Author:** Lynda (Business Lane)  
**Date:** 2026-03-10  
**Status:** Approved

---

## Executive Summary

Consolidating all Janet Home Automation documentation and integration assets into the **home-assistant-janet** repository creates a single source of truth, reduces onboarding friction, and clarifies the contribution path for the community.

---

## Why One Repo

### Single Source of Truth
- All HA docs in one place: `docs/`
- No duplicate or conflicting documentation
- Clear canonical paths for links and references

### Easier Onboarding
- New users: one repo to clone, one INDEX to read
- Contributors: one place to open issues and PRs
- Agents: one docs tree to index

### Clearer Branding
- **"Janet Home Automation"** = this repo
- Custom HA integration + full ecosystem docs
- Consistent messaging across README, docs, and external references

---

## Benefits

| Stakeholder | Benefit |
|-------------|---------|
| **Users** | Single entry point; 30-min quickstart path |
| **Developers** | One PR target; unified structure |
| **Contributors** | Clear scope: HA + Janet |
| **Investors** | Cohesive product narrative |

---

## Scope

**In scope:** Documentation, custom integration (`custom_components/janet`), migration scripts, Habitat persona reference  
**Out of scope:** janet-seed and janet-max code (stay in their repos); CallJanet-iOS (stays in CallJanet-iOS)

---

## Timeline

- **Week 1:** Docs migration complete, stub files in Janet-Projects
- **Week 2:** Habitat persona live; workspace references updated
- **Ongoing:** Deprecation notices; redirect from old paths

---

## Success Metrics

- All HA documentation navigable from [docs/INDEX.md](INDEX.md)
- Zero broken internal doc links
- Contributors can find and update docs in one repo
