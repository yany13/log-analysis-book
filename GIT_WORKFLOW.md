# Book Repository: Git Workflow & Standards

**Repository**: log-analysis-book  
**Status**: Live with active development  
**Created**: 2026-06-06  

---

## 📋 Repository Overview

This git repository tracks the **"AI Agents for Production Troubleshooting"** book—an educational resource teaching engineers to diagnose production failures using AI agents + log analysis.

### Quick Facts
- **Type**: Educational documentation / Technical book
- **Format**: 16 chapters (4 parts), markdown + SVG diagrams
- **Related Projects**: 2 sibling projects (app + toolkit)
- **License**: MIT
- **Status**: In active development (4/16 chapters complete)

---

## 🌿 Branch Strategy

### Main Branches

**`master`** - Production-ready, published content
- ✅ Reviewed by author
- ✅ Technically verified (labs tested)
- ✅ Ready for readers

**`develop`** - Active development branch
- 🔄 Work-in-progress chapters
- 🔄 New sections being written
- 🔄 May be incomplete

### Feature Branches

For writing new chapters or major rewrites:

```
feature/chapter-05-ldap-timeout        (New failure scenario)
feature/chapter-09-streamlit-toolkit   (New agent architecture section)
feature/part-iii-ai-agents             (Multiple chapters)
fix/ch-04-db-leak-clarification        (Improve existing chapter)
docs/update-book-index                 (Documentation updates)
```

### Branch Naming Convention

```
<type>/<scope-description>

Types:
  feature/    - New chapter or major section
  fix/        - Bug fixes, clarifications in existing chapters
  docs/       - Documentation, README, CLAUDE.md updates
  refactor/   - Reorganize chapters, improve structure

Scope examples:
  chapter-05-ldap-timeout
  part-iii-complete
  fix-ch-04-pool-exhaustion
  update-book-index
```

---

## 📝 Commit Message Format

All commits must follow this format:

```
<type>: <subject> (50 chars max)

<body (72 chars per line, if needed)>

Closes: <issue#>
Related: <other commits, PRs, or context>
```

### Commit Types

| Type | Usage | Example |
|------|-------|---------|
| `feat` | New chapter or major section | `feat: add Chapter 5 - LDAP timeout scenarios` |
| `fix` | Bug fix, clarification | `fix: clarify pool exhaustion diagnosis in Ch 4` |
| `refactor` | Reorganize, improve structure | `refactor: reorganize chapters into consistent format` |
| `docs` | Documentation updates | `docs: update CLAUDE.md with prompting examples` |
| `style` | Formatting (rare for docs) | `style: normalize markdown heading levels` |
| `test` | Add/update lab exercises | `test: add verification steps for deadlock scenario` |

### Examples

```
Good:
  feat: add Chapter 5 - LDAP authentication timeout diagnosis
  
  - Explains LDAP timeout pattern recognition
  - Shows log analysis steps
  - Includes remediation strategies
  - Provides hands-on lab commands

Better:
  feat: add Chapter 5 - LDAP authentication timeout diagnosis
  
  Failure Pattern: Authentication service timeout
  Root Causes: Directory unavailability, network latency
  Diagnosis: Manual log analysis, then agent RCA
  Lab: Trigger ?failureType=ldap_timeout, analyze catalina.log
  
  Related: Completes Part II (5 failure scenarios)
  Closes: BOOK-5
```

---

## 🔄 Workflow: Writing a Chapter

### 1. Create Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/chapter-05-ldap-timeout
```

### 2. Write Chapter
- Create `chapters/05-ldap-authentication-timeout.md`
- Add diagrams to `diagrams/` (if new)
- Follow structure from CLAUDE.md
- Test labs manually (against ByteBite app)
- Cross-reference other chapters

### 3. Commit Work (incremental)
```bash
# As you write sections, commit frequently
git add chapters/05-*.md
git commit -m "feat: draft LDAP timeout failure pattern section"

git add chapters/05-*.md
git commit -m "feat: add LDAP diagnostic framework section"

git add chapters/05-*.md
git commit -m "feat: add LDAP real-world analysis & mitigation"
```

### 4. Update Book Index
```bash
git add BOOK_INDEX.md
git commit -m "docs: update BOOK_INDEX.md - add Chapter 5"
```

### 5. Update CLAUDE.md if Needed
```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md - new prompting examples"
```

### 6. Push & Create PR
```bash
git push origin feature/chapter-05-ldap-timeout
# Create PR: feature/chapter-05-ldap-timeout → develop
```

### 7. Merge to Develop
```bash
# After review & verification
git checkout develop
git merge --no-ff feature/chapter-05-ldap-timeout
git push origin develop
```

### 8. Tag Release (when moving master)
```bash
git checkout master
git merge --no-ff develop
git tag -a v1.1.0 -m "Release v1.1.0: Chapters 0-5 complete"
git push origin master --tags
```

---

## 📊 File Organization

```
log-analysis-book/
├── .git/                           (Git metadata)
├── .gitignore                      (Exclude backups, drafts)
├── .gitattributes                  (Line ending handling)
├── LICENSE                         (MIT license)
├── GIT_WORKFLOW.md                (This file)
│
├── README.md                       (Reader-facing: learning paths)
├── CLAUDE.md                       (Writing directives)
├── MAINTENANCE.md                 (Sync with child projects)
├── BOOK_INDEX.md                  (Chapter index)
│
├── chapters/                       (Markdown chapters)
│   ├── 00-book-introduction.md
│   ├── 01-production-failures-in-the-wild.md
│   ├── 02-understanding-bytebite.md
│   ├── 03-reading-logs-like-a-detective.md       [TODO]
│   ├── 04-connection-pool-exhaustion.md
│   ├── 05-ldap-authentication-timeout.md        [TODO]
│   ├── ... (chapters 6-16)
│
├── diagrams/                       (SVG architecture & patterns)
│   ├── 01-infrastructure-architecture.svg
│   ├── 04-servlet-architecture.svg
│   ├── 05-servlet-architecture-*.svg
│   └── ... (other diagrams)
│
└── book_versions/                  (Reference materials)
    └── Chapters_Overviewv3.0.docx
```

---

## 🧪 Before Committing

### Self-Check (Author)

- [ ] Chapter follows CLAUDE.md rules (architecture-first, zero boilerplate)
- [ ] All commands are copy-paste ready
- [ ] Lab exercises tested against ByteBite app
- [ ] Cross-references to other chapters are correct
- [ ] Diagrams referenced & placed in diagrams/ folder
- [ ] No grammar/spelling errors (run spell-check)
- [ ] Markdown syntax is valid
- [ ] Learning goals are clear
- [ ] Code examples are self-documenting (minimal comments)
- [ ] Failure signatures match app CLAUDE.md

### Technical Verification (Before Merging to master)

- [ ] All labs work (app running, commands succeed)
- [ ] Agent outputs match expected root causes (toolkit verification)
- [ ] Book chapter references app/toolkit correctly
- [ ] BOOK_INDEX.md updated
- [ ] MAINTENANCE.md still accurate
- [ ] Cross-references between chapters are valid

---

## 🏷️ Tagging & Releases

### Version Format: `vX.Y.Z`

- **X** = Major (parts completed: 0=none, 1=Part I, 2=Parts I-II, etc.)
- **Y** = Minor (chapters completed within part)
- **Z** = Patch (fixes, clarifications)

### Examples

```
v0.1.0   Initial commit (scaffolding only)
v1.0.0   Part I complete (chapters 0-3)
v1.4.0   Part I + Part II chapters 4 complete
v2.0.0   Parts I & II complete (chapters 0-8)
v2.1.0   Part II improved (typo fixes, clarity)
v3.0.0   Parts I, II, III complete (chapters 0-12)
v4.0.0   Complete book (chapters 0-16)
```

### Creating a Release Tag

```bash
git checkout master
git tag -a v1.4.0 -m "Release v1.4.0: Part I + Chapter 4 (DB Leak) complete"
git push origin master --tags
```

---

## 🔗 Integration with Child Projects

### Before Writing a Chapter

**Check child project status:**
```bash
# App project
cd ../log-analysis-ai-usecase-app
git log --oneline -5
docker-compose ps  # Ensure it runs

# Toolkit project
cd ../log-analysis-streamlit-ai-toolkit
git log --oneline -5
streamlit run app.py  # Ensure it works
```

### Update MAINTENANCE.md

When you update a chapter that references app/toolkit:

```bash
git add MAINTENANCE.md
git commit -m "docs: update MAINTENANCE.md - sync with child projects"
```

### Cross-Project Testing

Before merging to master:

```bash
# 1. Start app
cd ../log-analysis-ai-usecase-app
docker-compose up -d

# 2. Start toolkit
cd ../log-analysis-streamlit-ai-toolkit
streamlit run app.py

# 3. Test your lab scenario from the book
# (Follow the exact commands from your chapter)

# 4. Verify app generates expected logs
# 5. Verify toolkit diagnoses correctly
# 6. Compare against book's expected output
```

---

## 📖 Sample Git Log

```
109880e Initial commit: AI Agents for Production Troubleshooting book
a3f2b1c feat: add Chapter 4 - Connection Pool Exhaustion diagnosis
b2e1a0f docs: update BOOK_INDEX with failure scenarios
c1d0f8e refactor: reorganize chapter structure into 4 parts
d0c7e6f feat: add 12 SVG architectural diagrams
e9b6d5f docs: initial CLAUDE.md with writing directives
f8a5c4e initial: scaffold chapters/ and diagrams/ folders
```

---

## 🚀 Continuous Improvement

### Code Review Checklist (For peer review)

- [ ] Content is accurate (no technical errors)
- [ ] Labs are reproducible (tested against current versions)
- [ ] Tone is peer-to-peer CTO (not condescending, not vague)
- [ ] Architecture explained before details
- [ ] No boilerplate (high-impact examples only)
- [ ] Self-documenting code (minimal comments)
- [ ] Cross-references valid
- [ ] Learning goals clear
- [ ] Diagrams enhance understanding

### Feedback Loop

```
Author writes chapter
     ↓
Peer review (technical accuracy, clarity)
     ↓
Labs tested against app + toolkit
     ↓
Revisions made
     ↓
Merge to develop
     ↓
Wait for next release batch
     ↓
Merge to master + tag release
```

---

## 📚 Related Repositories

This book references two sibling projects:

1. **log-analysis-ai-usecase-app** (ByteBite)
   - Generates failure logs for chapters 4-8, 13-16
   - Must run for hands-on labs
   - Git: [app repo]

2. **log-analysis-streamlit-ai-toolkit** (Agent)
   - Analyzes logs for chapters 9-12, 13-16
   - Demonstrates AI-assisted diagnosis
   - Git: [toolkit repo]

---

## ⚠️ Important Notes

### DO NOT Commit

- ❌ Backup files (`CLAUDE.md.backup.*`)
- ❌ Draft chapters (`draft_*`, `WIP_*`, `temp_*`)
- ❌ Word documents in progress (`~$*.docx`)
- ❌ Generated PDFs (regenerated from source)
- ❌ Editor configs (`.vscode/`, `.idea/`)
- ❌ Credential files (`.env`, `secrets/`)

### DO Commit

- ✅ Markdown chapters (`.md`)
- ✅ SVG diagrams (`.svg`)
- ✅ Configuration (CLAUDE.md, BOOK_INDEX.md)
- ✅ Documentation (README.md, MAINTENANCE.md)
- ✅ License & git config (LICENSE, .gitignore, .gitattributes)

---

## 🎓 Getting Started (New Contributors)

```bash
# 1. Clone the repository
git clone [book repo URL]
cd log-analysis-book

# 2. Read the guide
cat README.md              # Learning paths for readers
cat CLAUDE.md              # Writing directives for authors
cat GIT_WORKFLOW.md        # This file (git standards)

# 3. Create your feature branch
git checkout develop
git checkout -b feature/chapter-05-your-topic

# 4. Write your chapter
# (Follow CLAUDE.md guidelines)

# 5. Test your labs
# (Follow MAINTENANCE.md sync checklist)

# 6. Commit & push
git add chapters/05-*.md
git commit -m "feat: add Chapter 5 - your topic"
git push origin feature/chapter-05-your-topic

# 7. Create a pull request
# (On GitHub/GitLab)
```

---

## 📊 Status & Metrics

**Current Status** (2026-06-06):
- ✅ 4 chapters complete (0, 1, 2, 4)
- 📝 12 chapters to write (3, 5-16)
- ✅ 12 diagrams created
- ✅ CLAUDE.md & infrastructure set up

**Progress**:
- Part I: 3/4 chapters (75%)
- Part II: 1/5 chapters (20%)
- Part III: 0/4 chapters (0%)
- Part IV: 0/4 chapters (0%)
- **Overall**: 4/16 chapters (25%)

---

**Last Updated**: 2026-06-06  
**Next Step**: Write Chapter 3 (Reading Logs Like a Detective), then complete Part II
