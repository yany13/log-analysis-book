# AI Agents for Production Troubleshooting: A Hands-On Learning Book

**Learn to design and deploy AI Agents that diagnose production failures through log analysis.**

This book teaches senior engineers how to architect AI Agents for real-world troubleshooting scenarios using two practical projects: ByteBite (a troubleshooting app that generates failure logs) and the Streamlit Toolkit (a RAG-based agent that analyzes them).

---

## 📚 Book Overview

### What You'll Learn

1. **Production Failure Patterns** – Recognize 5 common failure signatures in logs
2. **Systematic Diagnosis** – Apply diagnostic frameworks to find root causes
3. **Agent Architecture** – Understand how AI Agents reason about logs (retrieval, prompting, validation)
4. **Hands-On Labs** – Trigger real failures, analyze logs manually, then with an agent
5. **Hybrid Workflows** – Combine human expertise with AI to solve faster

### Who This Is For

- **Senior Engineers** (5+ years) wanting to master production troubleshooting
- **CTOs / Technical Leads** designing incident response systems
- **SREs / DevOps Engineers** deploying AI-assisted operations
- **Anyone** building RAG systems for domain-specific knowledge

### Time Commitment

- **Part I (Chapters 0-3)**: 2-3 hours – Foundational concepts
- **Part II (Chapters 4-8)**: 7-10 hours – Failure scenarios + manual analysis
- **Part III (Chapters 9-12)**: 5-8 hours – Agent architecture + toolkit
- **Part IV (Chapters 13-16)**: 6-10 hours – Integration, scaling, team training
- **Total**: 20-31 hours for complete mastery

---

## 🎯 Learning Paths

### Path 1: Complete Mastery (6-8 weeks)
**For**: CTOs, architecture teams, SRE leads

1. Read Part I (foundations)
2. Work through Part II scenarios in order
3. Master Part III (AI tools)
4. Advanced patterns in Part IV
5. Build your own lab (Chapter 16)

### Path 2: Hands-On Practitioner (2-3 weeks)
**For**: Developers, junior engineers

1. Chapters 1-2 (quick context)
2. Choose 2-3 failure scenarios (Ch 4-6)
3. Chapters 9-10 (toolkit basics)
4. Chapter 13 (integrated workflow)

### Path 3: Executive Summary (2-3 hours)
**For**: Engineering managers, product leads

- Chapter 1 (failure patterns overview)
- Chapter 9 (agent capabilities)
- Chapter 15 (organizational impact)

### Path 4: Team Training (2 days)
**For**: Engineering teams learning together

- Group session: Part I (2 hours)
- Small teams: 2 scenarios each (6 hours)
- Group: Chapters 9-10 (2 hours)
- Team exercise: Chapter 13 (2 hours)
- Debrief: Chapter 15 (1 hour)

---

## 📖 Chapter Structure

### **Part I: Foundations (Chapters 0-3)**

| Chapter | Topic | Duration | Type |
|---------|-------|----------|------|
| 0 | Book Introduction | 20 min | Reading |
| 1 | Production Failures in the Wild | 45 min | Reading |
| 2 | Understanding the ByteBite System | 60 min | Reading + Setup |
| 3 | Reading Logs Like a Detective | 60 min | Hands-On Lab |

**Outcomes**: Understand failure patterns, can trigger failures, know how to search logs.

### **Part II: The 5 Failure Scenarios (Chapters 4-8)**

| Chapter | Failure | Duration | Lab Commands |
|---------|---------|----------|--------------|
| 4 | Connection Pool Exhaustion | 90 min | `?failureType=db_leak` |
| 5 | LDAP Authentication Timeout | 90 min | `?failureType=ldap_timeout` |
| 6 | Memory Exhaustion (OOM) | 90 min | `?failureType=oom` |
| 7 | Thread Deadlock | 120 min | `{"failureType":"deadlock"}` |
| 8 | SSL/TLS Certificate Validation | 90 min | `{"failureType":"ssl"}` |

**Each includes**: Failure mechanics → symptom recognition → log analysis → diagnostic framework → code patterns → mitigation.

**Outcomes**: Can manually diagnose each failure pattern from logs.

### **Part III: Building the AI Agent (Chapters 9-12)**

| Chapter | Topic | Duration | Focus |
|---------|-------|----------|-------|
| 9 | Streamlit Toolkit Overview | 60 min | Agent architecture |
| 10 | Embeddings & Semantic Search | 90 min | Retrieval strategy |
| 11 | Expert RCA with LLMs | 120 min | Prompting patterns |
| 12 | Knowledge Base Design | 90 min | What to index, organization |

**Outcomes**: Understand agent design, can write effective prompts, know how to structure knowledge bases.

### **Part IV: Integration & Advanced (Chapters 13-16)**

| Chapter | Topic | Duration | Focus |
|---------|-------|----------|-------|
| 13 | ByteBite + Toolkit Workflow | 120 min | End-to-end integration |
| 14 | Scaling the Approach | 90 min | Multi-service, high-volume |
| 15 | Incident Response in Practice | 60 min | Process, automation, team training |
| 16 | Building Your Own Lab | 120 min | Extending with custom failures |

**Outcomes**: Can deploy agents, train teams, build custom labs.

---

## 🚀 Getting Started

### Prerequisites

```bash
# Ensure both projects are cloned
ls D:\workspace\ai\code\log-analysis-ai-usecase-app
ls D:\workspace\ai\code\log-analysis-streamlit-ai-toolkit
```

### Quick Start (5 minutes)

```bash
# 1. Start ByteBite app (Terminal 1)
cd ../log-analysis-ai-usecase-app
docker-compose up -d
sleep 45
curl http://localhost:8080/bytebite/health

# 2. Start Streamlit toolkit (Terminal 2)
cd ../log-analysis-streamlit-ai-toolkit
pip install -r requirements.txt
streamlit run app.py

# 3. Open book in editor (Terminal 3)
cd ../log-analysis-book
# Open chapters/ in your editor
```

### Verify Setup

```bash
# Check app is running
curl http://localhost:8080/bytebite/health
# Expected: {"status":"UP"}

# Check toolkit is running
# Expected: Streamlit UI at http://localhost:8501

# Check you can trigger a failure
curl "http://localhost:8080/bytebite/api/menu?failureType=db_leak"
# Expected: Menu items response (or error if pool exhausted)
```

---

## 📂 Folder Structure

```
log-analysis-book/
│
├── README.md (this file)
├── CLAUDE.md (book-specific writing directives)
├── MAINTENANCE.md (sync checklist, when projects change)
│
├── chapters/
│   ├── 00-book-introduction.md
│   ├── 01-production-failures-in-the-wild.md
│   ├── ... (chapters 2-16)
│   └── 16-building-your-own-lab.md
│
├── diagrams/
│   ├── 01-infrastructure-architecture.svg
│   ├── 04-servlet-architecture.svg
│   └── ... (other diagrams)
│
└── BOOK_INDEX.md (comprehensive index, learning maps)
```

---

## 🔗 Related Projects

This book documents two sibling projects:

| Project | Purpose | Location |
|---------|---------|----------|
| **ByteBite App** | Generates realistic failure logs | `../log-analysis-ai-usecase-app` |
| **Streamlit Toolkit** | RAG-based AI Agent for log analysis | `../log-analysis-streamlit-ai-toolkit` |

Both must be running for hands-on labs. See CLAUDE.md for detailed setup.

---

## 💡 How to Use This Book

### Solo Learning
1. Choose your learning path (above)
2. Read chapter overview
3. Do hands-on labs in order
4. Review key takeaways
5. Practice with your own logs

### Pair Learning
1. Read chapters together
2. Discuss concepts after each section
3. Take turns driving labs
4. Share findings and insights

### Team Training
1. Present Part I as group session
2. Assign failure scenarios to small teams
3. Have teams present their findings
4. Work through Chapter 13 together
5. Run wargames with Chapter 16 patterns

---

## ✅ Success Criteria

After completing this book, you'll be able to:

- ✅ Recognize failure patterns in logs immediately
- ✅ Diagnose root causes systematically (not guessing)
- ✅ Explain why AI Agents enhance troubleshooting
- ✅ Design effective RAG systems for log analysis
- ✅ Write prompts that elicit accurate analysis from LLMs
- ✅ Validate agent outputs against known facts
- ✅ Build custom knowledge bases for your organization
- ✅ Deploy agents for incident response
- ✅ Train teams on hybrid human-AI troubleshooting

---

## 🔍 Key Concepts

### Root Cause Analysis (RCA)
The systematic process of identifying the *fundamental reason* why a failure occurred, not just surface symptoms.

### Hybrid Intelligence
Combining human domain expertise with AI pattern matching to solve complex problems faster than either alone.

### Failure Injection
Deliberately triggering controlled failures to safely learn how systems break and how to diagnose issues.

### RAG (Retrieval-Augmented Generation)
Using embeddings to semantically search a knowledge base, then passing relevant context to LLMs for better analysis.

### Knowledge Base
A curated collection of runbooks, past incidents, architecture docs, and solutions for AI retrieval.

---

## 📬 Feedback & Contributions

As you work through this book:
- Note sections that are unclear
- Try techniques and report what worked
- Build your own failure scenarios
- Share improvements and new chapters

Your real-world experience makes this resource better.

---

## 📊 Status

**Current**: Book structure created, foundational CLAUDE.md in place  
**Next**: Migrate existing chapters, write missing chapters (3, 5-8, 9-12, 13-16)  
**Timeline**: 4-6 weeks for complete draft (35+ hours writing)

See MAINTENANCE.md for sync checklist with child projects.

---

**Start here**: Open `chapters/00-book-introduction.md` or jump to your chosen learning path above.
