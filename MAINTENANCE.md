# Maintenance & Sync Guide

This document tracks how to keep the book in sync with the two child projects as they evolve.

---

## 📋 Pre-Release Sync Checklist

**Run this checklist before publishing any book release:**

```markdown
## Full Sync Verification (2026-06-06)

### Child Projects Functional
- [ ] `log-analysis-ai-usecase-app` builds successfully
  ```bash
  cd ../log-analysis-ai-usecase-app
  mvn clean package -DskipTests
  ```
- [ ] `log-analysis-ai-usecase-app` runs with Docker Compose
  ```bash
  docker-compose up -d && sleep 45 && curl http://localhost:8080/bytebite/health
  ```
- [ ] `log-analysis-streamlit-ai-toolkit` installs and runs
  ```bash
  pip install -r requirements.txt && streamlit run app.py
  ```

### Book Content & Commands
- [ ] All curl commands in Chapters 4-8, 13 still work
- [ ] All file paths (../log-analysis-ai-usecase-app/...) are still valid
- [ ] Log format examples match actual Tomcat output (DD-MMM-YYYY HH:MM:SS.ms UTC)
- [ ] All `failureType` parameters match FailureInjectionUtil.java
- [ ] All endpoints match current web.xml routing

### Cross-References
- [ ] Internal chapter links work (Ch 4 → Ch 3 reference)
- [ ] Links to child projects resolve correctly
- [ ] Diagram paths are valid (./diagrams/XX-*.svg)

### Toolkit Integration
- [ ] Chapter 9-12 code examples match streamlit_app/ implementation
- [ ] Prompt examples match prompts/ folder (if it exists)
- [ ] UI screenshots/descriptions match current Streamlit version
- [ ] ChromaDB setup matches toolkit's requirements.txt

### Logs & Output
- [ ] Actual Tomcat logs still match format shown in examples
- [ ] HikariCP messages still match Chapter 4 examples
- [ ] LDAP messages still match Chapter 5 examples
- [ ] Deadlock messages still match Chapter 7 examples

### Diagrams
- [ ] SVG diagrams in ./diagrams/ match current architecture
- [ ] Diagrams referenced in chapters exist
- [ ] No orphaned diagrams (all are referenced in at least one chapter)

### Status Markers
- [ ] Each chapter has Status header with date and reviewer
- [ ] No chapters marked as "TODO" or incomplete
```

**Release Sign-Off**:
```
Verified on: [DATE]
By: [Name/Role]
Build: [App version]
Toolkit: [Agent version]
Ready to publish: ☐ Yes ☐ No (if No, list issues)
```

---

## 🔄 When Child Projects Change

### Scenario 1: New Endpoint Added to ByteBite App

**What changes**:
- New servlet in `src/main/java/com/bytebite/servlet/`
- New routing in `web.xml`
- New failure injection type (new `?failureType=` parameter)

**Book impact**:
- [ ] Update Chapter 2 (system architecture) to show new endpoint
- [ ] If it's a failure scenario, create new chapter (e.g., Chapter 9 if it was missing)
- [ ] Update BOOK_INDEX.md
- [ ] Add lab commands to relevant chapters
- [ ] Update logs examples if new endpoints appear in traces

**Checklist**:
```java
// Check new failure type in FailureInjectionUtil.java
// Copy exact failureType string to book
public void inject(String failureType) {
    if ("new_failure_type".equals(failureType)) { // ← Use this in book
```

### Scenario 2: Log Format Changes

**What changes**:
- Timestamp format modification
- Log level changes (DEBUG → INFO)
- Message wording in failure signatures

**Book impact**:
- [ ] Update ALL log examples in Chapters 3-8 and 13
- [ ] Search & replace old format with new
- [ ] Re-run labs to capture fresh logs
- [ ] Update "key signals" tables in each chapter

**Example S&R**:
```
OLD: [HikariPool] Connection is not available...
NEW: [HikariCP] Unable to acquire connection...
```

### Scenario 3: New LLM Provider Added to Toolkit

**What changes**:
- New LLM support in `streamlit_app/llm_manager.py` (or similar)
- New configuration options

**Book impact**:
- [ ] Update Chapter 9 (toolkit overview) to mention new provider
- [ ] Add setup instructions to Chapter 9
- [ ] Update Chapter 11 if prompting differs per provider
- [ ] Add notes on cost/performance per provider

### Scenario 4: Toolkit Retrieval Strategy Changes

**What changes**:
- New embedding model (e.g., better semantic understanding)
- New chunking strategy
- New similarity scoring

**Book impact**:
- [ ] Update Chapter 10 (embeddings & semantic search)
- [ ] Re-run semantic search examples (may have different results)
- [ ] Update "why embeddings > keywords" comparison
- [ ] Test with real logs to show improvement

### Scenario 5: New Prompt Template in Toolkit

**What changes**:
- RCA prompt modified
- New validation prompt added
- Confidence scoring prompt adjusted

**Book impact**:
- [ ] Update Chapter 11 (expert RCA with LLMs)
- [ ] Show new prompt template
- [ ] Compare outputs with old vs. new
- [ ] Document why change improves accuracy

---

## 🚨 Common Sync Issues & Fixes

### Issue 1: "curl commands no longer work"

**Diagnosis**:
```bash
cd ../log-analysis-ai-usecase-app
curl "http://localhost:8080/bytebite/api/menu?failureType=db_leak"
# Returns: 404 Not Found
```

**Fix**:
1. Check if endpoint exists: `grep -r "api/menu" src/main/java/`
2. Check web.xml routing: `grep -A 5 "MenuServlet" web.xml`
3. Check if failure type is registered: `grep "db_leak" FailureInjectionUtil.java`
4. Update book command if endpoint moved/renamed

### Issue 2: "Log examples don't match actual logs"

**Diagnosis**:
```bash
docker-compose logs tomcat | head -20
# Logs show different format/content than Chapter 4 example
```

**Fix**:
1. Capture fresh logs: `docker-compose logs tomcat > actual_logs.txt`
2. Compare with book example (use diff tool)
3. Update Chapter examples to match
4. Note what changed in CHANGELOG

### Issue 3: "Toolkit prompts aren't working"

**Diagnosis**:
```
Book Chapter 11 shows prompt example, but toolkit has different prompt.
```

**Fix**:
1. Find current prompt: `ls ../log-analysis-streamlit-ai-toolkit/prompts/`
2. Compare with book example
3. Update Chapter 11 with actual prompt
4. Document why prompts differ (version, model, etc.)

### Issue 4: "Diagrams are outdated"

**Diagnosis**:
```
Book references architecture diagram, but app code has changed.
```

**Fix**:
1. Regenerate diagram from actual code (use plant UML or draw.io)
2. Update SVG file in ./diagrams/
3. Verify it matches all references in chapters
4. Document what changed in diagram

---

## 📝 Change Log Template

Create a CHANGELOG.md at the root if tracking major changes:

```markdown
# Changelog

## [v1.0.0] - 2026-06-30

### Changed
- Chapter 4: Updated HikariPool log examples (new timestamp format)
- Chapter 9: Added OpenAI provider support
- Diagrams: Updated 05-servlet-architecture-02.svg to show new error handling

### Fixed
- Chapter 5: LDAP timeout endpoint is now /login (was /authenticate)
- Chapter 13: Corrected curl command (query param syntax)

### Added
- Chapter 12: New knowledge base tagging strategy section
- Toolkit link in Chapter 9 setup instructions

### Removed
- Chapter 8: Deprecated SSL force config section (no longer needed)

### Notes
- Tested against commit abc1234 of both child projects
- Verified all commands work on Windows 10, Docker Desktop 4.xx
```

---

## 🔗 Dependency Graph

```
log-analysis-book/
│
├── Imports from log-analysis-ai-usecase-app:
│   ├── Chapters 2, 4-8, 13-16 (labs, logs, commands)
│   ├── Diagrams: 01-infrastructure, 04-servlet-architecture, 05-failures
│   ├── CLAUDE.md compliance (failure types, stack, timestamps)
│   └── Tech stack (Tomcat 11, PostgreSQL 15, HikariCP, JDK 21)
│
└── Imports from log-analysis-streamlit-ai-toolkit:
    ├── Chapters 9-12 (agent architecture, prompting)
    ├── Diagrams: 09-streamlit-toolkit-hierarchy
    ├── Tech stack (Streamlit, ChromaDB, LLMs, Python)
    └── Prompt examples (RCA, validation, classification)
```

---

## 🧪 Testing Strategy

### Before Publishing Each Chapter

```bash
# 1. Build & run both projects
cd ../log-analysis-ai-usecase-app && mvn package -DskipTests && docker-compose up -d
cd ../log-analysis-streamlit-ai-toolkit && streamlit run app.py

# 2. Run all commands from chapter
curl "http://localhost:8080/bytebite/api/menu?failureType=db_leak"
curl -X POST "http://localhost:8080/bytebite/login?failureType=ldap_timeout" -d "username=admin&password=admin"

# 3. Capture actual logs
docker-compose -f ../log-analysis-ai-usecase-app/docker-compose.yml logs tomcat > logs_for_chapter.txt

# 4. Compare with chapter examples
diff logs_for_chapter.txt chapters/04-connection-pool-exhaustion.md

# 5. Update chapter if logs differ
```

### Integration Testing

Every 2 weeks, run end-to-end (Chapter 13 workflow):

```bash
# 1. Trigger 3 different failures
curl "http://localhost:8080/bytebite/api/menu?failureType=db_leak"
curl "http://localhost:8080/bytebite/api/analytics?failureType=oom"
curl -X POST "http://localhost:8080/bytebite/api/kds" -H "Content-Type: application/json" -d '{"failureType":"deadlock"}'

# 2. Export logs
docker exec bytebite-tomcat tar czf - /usr/local/tomcat/logs/ > logs.tar.gz

# 3. Upload to Streamlit toolkit
# (Follow Chapter 13 UI steps)

# 4. Verify agent diagnoses correctly
# (Compare agent output with expected root causes)
```

---

## 🎯 Quarterly Maintenance

**Every 3 months**, run full audit:

- [ ] Both projects still build/run
- [ ] All book commands still work
- [ ] No broken links or file paths
- [ ] Log format unchanged
- [ ] Diagrams still accurate
- [ ] New features documented
- [ ] Deprecated features removed
- [ ] Reader feedback incorporated

---

**Questions?** Check CLAUDE.md for writing directives, README.md for structure overview.
