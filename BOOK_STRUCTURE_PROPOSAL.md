# Book Folder Structure Proposal

## Current vs. Proposed Structure

### CURRENT (Problematic)
```
log-analysis-book/
├── chapters/              ← Individual markdown (incomplete)
├── diagrams/              ← Flat SVG collection
├── book_versions/         ← Generated DOCX + temp files
│   ├── Chapters_Overviewv3.0.docx
│   ├── docx_work/         ← Temp files (should be removed)
│   ├── temp_unpack/       ← Temp files (should be removed)
│   └── verify_final/      ← Temp files (should be removed)
└── [scattered build scripts]
```

**Problems**:
- ❌ No build system → manual edits
- ❌ No dependency tracking → easy to break references
- ❌ Temp files pollute repo
- ❌ No validation → content becomes stale
- ❌ Hard to sync with code changes

---

### PROPOSED (Professional)
```
log-analysis-book/
├── _source/               ← SOURCE CONTENT (markdown)
│   ├── 00-intro.md
│   ├── 01-foundations.md
│   ├── 02-bytebite-overview.md
│   ├── 03-ai-toolkit.md
│   ├── failure-scenarios/
│   │   ├── 04-ldap-timeout.md
│   │   ├── 05-db-leak.md
│   │   ├── 06-oom.md
│   │   ├── 07-deadlock.md
│   │   └── 08-ssl.md
│   ├── appendices/
│   │   ├── A1-database-schema.md
│   │   └── A2-project-structure.md
│   └── templates/
│       └── [reusable sections]
│
├── diagrams/              ← DIAGRAM SOURCES (SVG)
│   ├── 01-infrastructure-architecture.svg
│   ├── 02-application-flow.svg
│   ├── 03-database-schema.svg
│   ├── 04-servlet-architecture.svg
│   ├── failure-scenarios/
│   │   ├── 05-*-login-ldap-timeout.svg
│   │   ├── 05-*-menu-db-leak.svg
│   │   ├── 05-*-analytics-oom.svg
│   │   ├── 05-*-kds-deadlock.svg
│   │   └── 05-*-checkout-ssl.svg
│   ├── infrastructure/
│   │   ├── 06-database-schema-er.svg
│   │   └── 08-docker-compose-hierarchy.svg
│   └── project-structure/
│       └── app-project-folder-structure.svg
│
├── build/                 ← BUILD SYSTEM
│   ├── build-docx.py      # Markdown+diagrams → DOCX
│   ├── sync-code-refs.py  # Auto-update from code changes
│   ├── validate-content.py
│   ├── Makefile
│   └── templates/
│
├── content-mapping/       ← DEPENDENCY TRACKING
│   ├── code-refs.yaml     # Code → Chapter references
│   ├── diagram-refs.yaml  # Diagram → Chapter mapping
│   └── changelog.md
│
├── tests/                 ← VALIDATION
│   ├── test-chapter-refs.py
│   ├── test-diagram-refs.py
│   └── test-docx-structure.py
│
├── output/                ← GENERATED (git-ignored)
│   ├── Middleware_Troubleshooting_latest.docx
│   └── Middleware_Troubleshooting_v1.0.pdf
│
├── versions/              ← RELEASE HISTORY
│   ├── v1.0.md
│   └── v1.0.docx
│
├── Makefile               ← Build orchestration
├── BOOK_INDEX.md
├── MAINTENANCE.md
├── .gitignore
└── CLAUDE.md
```

**Benefits**:
- ✅ Clear separation: source vs. generated
- ✅ Automated build: one command to regenerate
- ✅ Dependency tracking: know what code changed
- ✅ Validation: catches broken references
- ✅ Scalable: easy to add chapters
- ✅ Professional: organized like real technical books

---

## Implementation Roadmap

### Phase 1: Organize Content (Week 1)
**Goal**: Structure source files, clean up temp files

```bash
# 1. Create source directory structure
mkdir -p _source/failure-scenarios _source/appendices _source/templates
mkdir -p diagrams/failure-scenarios diagrams/infrastructure diagrams/project-structure

# 2. Move and organize chapters
mv chapters/00-book-introduction.md _source/00-intro.md
mv chapters/01-production-failures-in-the-wild.md _source/01-foundations.md
mv chapters/02-understanding-bytebite.md _source/02-bytebite-overview.md
# ... create missing chapters for 03-08

# 3. Organize diagrams
mv diagrams/05-*.svg diagrams/failure-scenarios/
mv diagrams/06-*.svg diagrams/infrastructure/
mv diagrams/08-*.svg diagrams/infrastructure/
mv diagrams/app-*.svg diagrams/project-structure/

# 4. Remove temp files
rm -rf book_versions/docx_work/ book_versions/temp_unpack/ book_versions/verify_final/
rm -rf book_versions/*.zip

# 5. Create output directory
mkdir output
mv book_versions/Chapters_Overview_with_Diagrams.docx output/
```

### Phase 2: Build System (Week 2)
**Goal**: Create automated DOCX generation

```python
# build/build-docx.py
# Reads: _source/*.md + diagrams/* → Outputs: output/book.docx

# build/sync-code-refs.py
# Verifies: All code references still exist in code

# build/validate-content.py
# Checks: Markdown syntax, diagram references, links
```

### Phase 3: Dependency Tracking (Week 2)
**Goal**: Document what code/diagrams map to what chapters

```yaml
# content-mapping/code-refs.yaml
Chapter_4_LDAP:
  references:
    - file: src/main/java/com/bytebite/filter/LDAPAuthenticationFilter.java
      lines: 45-60
      description: "LDAP timeout simulation"
    - file: src/main/java/com/bytebite/servlet/LoginServlet.java
      method: doPost()
```

### Phase 4: Testing & CI (Week 3)
**Goal**: Validate book consistency automatically

```bash
# tests/test-chapter-refs.py
# Error if: Code file referenced in chapter doesn't exist

# tests/test-diagram-refs.py
# Error if: Diagram referenced in markdown doesn't exist
```

### Phase 5: Documentation (Week 3)
**Goal**: Document the new system

```
├── BUILD.md              # How to build the book
├── SYNC.md               # How to keep it updated
├── CONTRIBUTE.md         # How to write chapters
└── MAINTENANCE.md        # Maintenance tasks
```

---

## Usage After Migration

### Build the Book
```bash
make build
# Outputs: output/Middleware_Troubleshooting_latest.docx
```

### Keep Book in Sync with Code
```bash
make sync
# Auto-detects code changes, updates references, rebuilds DOCX
```

### Validate Everything
```bash
make test
# Runs all validation checks
```

### Update a Chapter
```bash
# Edit markdown file
vim _source/failure-scenarios/04-ldap-timeout.md

# Build and preview
make build

# Commit
git add _source/failure-scenarios/04-ldap-timeout.md
git commit -m "docs: update LDAP chapter with new findings"
```

---

## Sync Strategy: How Book Stays Current

### Automatic Sync Workflow
```
Code Change in App → GitHub Webhook
  ↓
sync-code-refs.py runs in Book repo
  ↓
Detects: "Chapter 4 references LoginServlet"
  ↓
Extracts latest code snippets
  ↓
Updates _source/failure-scenarios/04-ldap-timeout.md
  ↓
Runs: make build
  ↓
New DOCX generated automatically
  ↓
Git commit: "docs: sync LDAP chapter with code changes"
  ↓
PR created for review
```

---

## Key Files After Migration

### `.gitignore` (Updated)
```
# Generated files
output/
*.docx
*.pdf

# Build artifacts
*.pyc
__pycache__/

# Temp files
_temp/
.DS_Store
```

### `Makefile` (New)
```makefile
.PHONY: build sync test clean help

build:
	python build/build-docx.py

sync:
	python build/sync-code-refs.py

test:
	python tests/test-chapter-refs.py
	python tests/test-diagram-refs.py
	python tests/test-docx-structure.py

clean:
	rm -rf output/*
	find . -type d -name __pycache__ -exec rm -rf {} +

help:
	@echo "Available targets: build, sync, test, clean"
```

### `content-mapping/code-refs.yaml` (New)
```yaml
# Tracks which chapters reference which code

Chapter_4_LDAP_Authentication:
  files:
    - path: src/main/java/com/bytebite/filter/LDAPAuthenticationFilter.java
      lines: 45-90
      last_verified: 2026-06-06
      status: "OK"
    
Chapter_5_Database_Leak:
  files:
    - path: src/main/java/com/bytebite/util/FailureInjectionUtil.java
      method: "injectDBLeak()"
      last_verified: 2026-06-01
      status: "NEEDS_UPDATE"  # Code changed, chapter may need update
```

---

## Success Criteria

✅ Book can be regenerated with one command  
✅ Changes to code trigger book updates  
✅ Broken references caught automatically  
✅ New chapters can be added without restructuring  
✅ Diagrams organized by purpose  
✅ Version history preserved  
✅ Clean git history (no temp files)  

---

## Timeline

| Phase | Task | Time | Status |
|-------|------|------|--------|
| 1 | Organize files | 2 hrs | →
| 2 | Build system | 3 hrs | →
| 3 | Tracking | 2 hrs | →
| 4 | Testing | 2 hrs | →
| 5 | Docs | 2 hrs | →
| | **Total** | **11 hrs** | →

---

## Next Steps

1. **Review** this proposal
2. **Approve** the structure
3. **I will implement** Phase 1-2 in next session
4. **You create** missing chapters in _source/failure-scenarios/ as needed
5. **Book stays current** automatically via CI/CD

Ready to implement?
