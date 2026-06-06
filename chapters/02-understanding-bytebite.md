# Chapter 2: Understanding the ByteBite System
## Your Hands-On Troubleshooting Laboratory

---

## What is ByteBite?

ByteBite is a **restaurant order management system** with five intentionally engineered failure injection points. It's not a production system—it's a learning laboratory designed to:

1. **Generate realistic failures** that match production patterns
2. **Produce detailed logs** of those failures
3. **Enable safe experimentation** without affecting real customers
4. **Provide immediate feedback** on your diagnostic techniques

Think of it as a flight simulator for production troubleshooting. You practice on controlled failures, so when real production issues hit, you already know how to respond.

---

## System Architecture at a Glance

```
┌─────────────────────────────────────┐
│        Web Browser (User)           │
│   HTML5 + Vanilla JavaScript        │
└────────────┬────────────────────────┘
             │ HTTP/HTTPS (ports 8080/8443)
             ▼
┌─────────────────────────────────────┐
│   Apache Tomcat 11 (JDK 21)         │
│  ┌─────────────────────────────┐   │
│  │ 6 Servlets (request handlers)   │
│  │ 4 Filters (middleware)          │
│  │ 3 Services (business logic)     │
│  └─────────────────────────────┘   │
└────┬──────────────────┬────────────┘
     │                  │
  JDBC│           JNDI/LDAP│
     │                  │
     ▼                  ▼
┌──────────────┐  ┌──────────────┐
│PostgreSQL 15 │  │ OpenLDAP 1.5 │
│(Port 5432)   │  │ (Port 389)   │
└──────────────┘  └──────────────┘
```

### Key Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Java (Temurin JDK) | 21 | Execute Java application |
| **App Server** | Apache Tomcat | 11 | Servlet container, HTTP handling |
| **Database** | PostgreSQL | 15-alpine | Persistent data storage |
| **Auth Service** | OpenLDAP | 1.5.0 | User authentication via directory |
| **Logging** | SLF4J + JUL | Built-in | Structured application logging |
| **Orchestration** | Docker Compose | 3.8 | Multi-container deployment |
| **Frontend** | HTML5 + JavaScript | Vanilla | Browser-based user interface |
| **Connection Pool** | HikariCP | Built-in | Database connection management |

---

## Core Components Explained

### Layer 1: Servlet Layer (Request Handlers)

The servlet layer processes HTTP requests. Each servlet handles a specific feature:

| Servlet | Endpoint | Purpose | Failure Point |
|---------|----------|---------|---------------|
| **LoginServlet** | `/login` | User authentication | LDAP timeout injection |
| **MenuServlet** | `/api/menu` | Menu item retrieval | DB connection leak injection |
| **CheckoutServlet** | `/checkout` | Order processing | SSL validation injection |
| **AnalyticsServlet** | `/api/analytics` | Event tracking | OOM heap injection |
| **KDSServlet** | `/api/kds` | Kitchen display system | Deadlock injection |
| **HealthServlet** | `/health` | System health check | Database/LDAP connectivity |

### Layer 2: Filter Layer (Middleware)

Filters intercept requests before they reach servlets, handling cross-cutting concerns:

| Filter | Purpose | Key Feature |
|--------|---------|------------|
| **RequestLoggingFilter** | Log all HTTP requests/responses | Timing, status codes |
| **LDAPAuthenticationFilter** | Validate user sessions | Checks LDAP directory |
| **CORSFilter** | Allow cross-origin requests | CORS headers |
| **SecurityHeadersFilter** | Add security headers | CSP, HSTS, X-Frame-Options |

### Layer 3: Service Layer (Business Logic)

Services contain the actual business logic, accessed by servlets:

| Service | Responsibility |
|---------|-----------------|
| **UserService** | User management, LDAP lookups |
| **OrderService** | Order creation, status updates |
| **AnalyticsService** | Event tracking, reporting |

### Layer 4: Configuration & Initialization

These components set up the system at startup:

| Component | Purpose |
|-----------|---------|
| **AppInitializationListener** | Application startup setup |
| **DataSourceInitListener** | Database connection pool initialization |
| **DatabaseConfig** | JDBC connection configuration |
| **LDAPConfig** | LDAP/Tomcat Realm setup |

### Supporting Utilities

Helper classes used throughout:

| Utility | Purpose |
|---------|---------|
| **FailureInjectionUtil** | Central dispatcher for failure injection |
| **JsonResponseUtil** | JSON response formatting |
| **SecurityUtil** | Password hashing, CSRF tokens |
| **DateTimeUtil** | Timestamp handling |
| **PaginationUtil** | Request pagination |
| **Constants** | Shared configuration values |

---

## The Database Schema: 11 Tables

ByteBite stores data across 11 tables in the `bytebite` schema:

### User Management (3 tables)
```sql
users              -- User profiles (username, email, created_at)
user_roles         -- Available roles (admin, manager, staff, customer)
user_role_mapping  -- Which users have which roles
```

### Session Management (1 table)
```sql
sessions           -- User sessions (session_id, user_id, expires_at)
```

### Order Management (3 tables)
```sql
orders             -- Order records (order_id, user_id, status, total_amount)
order_items        -- Line items in orders (product, quantity, price)
kds_orders         -- Kitchen display system orders
```

### Analytics & Monitoring (4 tables)
```sql
analytics_events   -- Event tracking (JSONB for flexible schemas)
api_audit_log      -- API call logging (endpoint, method, status, duration)
application_logs   -- Application-level events
menu_items         -- Menu items available for ordering
```

---

## The Five Engineered Failures Explained

### Failure 1: DB Connection Leak (`/api/menu`)

**Trigger**: `GET /api/menu?failureType=db_leak`

**What Happens**:
1. MenuServlet gets a database connection from HikariCP pool
2. Normally: executes query → closes statement → returns connection
3. **With failure injection**: Gets connection → executes query → statement closed → **connection NOT returned**
4. After multiple requests: All 20 connections in pool are held, waiting connection never becomes available

**What You'll See in Logs**:
```
[HikariPool] Connection is not available, request timed out after 30000ms
```

**How to Diagnose**:
- HikariCP logs show available connection count dropping
- Thread dumps show threads blocked on `pool.getConnection()`
- User requests timeout with 504 errors

---

### Failure 2: LDAP Authentication Timeout (`/login`)

**Trigger**: `POST /login?failureType=ldap_timeout` with credentials

**What Happens**:
1. LoginServlet receives login request with username/password
2. Normally: checks LDAP directory → user found → returns success
3. **With failure injection**: tries to connect LDAP → connection timeout (30+ seconds)
4. User gets timeout or "invalid credentials" error

**What You'll See in Logs**:
```
LDAP connection timeout (failure injection)
com.sun.jndi.ldap.connect.pool.PooledConnection - Connection attempt timeout
```

**How to Diagnose**:
- Auth filter logs show LDAP lookup attempts
- Response times for login requests are 30+ seconds
- Multiple failed login attempts in logs

---

### Failure 3: Heap Exhaustion (OOM)

**Trigger**: `GET /api/analytics?action=all-time-report&failureType=oom`

**What Happens**:
1. AnalyticsServlet receives request for all-time report
2. Normally: queries events with pagination, returns paginated results
3. **With failure injection**: loads **all events into memory** instead of paginating
4. If you have thousands of events → heap fills up
5. JVM terminates with OutOfMemoryError

**What You'll See in Logs**:
```
OutOfMemoryError: Java heap space
```

**How to Diagnose**:
- Heap usage spikes to 100%
- GC logs show increasingly frequent garbage collection
- OOM error appears just before process crash

---

### Failure 4: Thread Deadlock (`/api/kds`)

**Trigger**: `POST /api/kds` with JSON `{"failureType":"deadlock"}`

**What Happens**:
1. KDSServlet updates order and inventory (requires two locks)
2. Normally: acquires locks in consistent order → updates → releases
3. **With failure injection**: Thread 1 acquires Order lock then Inventory lock; Thread 2 acquires Inventory lock then tries Order lock
4. Circular waiting: neither thread can proceed
5. Requests hang indefinitely

**What You'll See in Logs**:
```
DEADLOCK SCENARIO: Both threads are now BLOCKED
Thread-15 is waiting for lock held by Thread-16
Thread-16 is waiting for lock held by Thread-15
```

**How to Diagnose**:
- Logs show deadlock message
- Thread dumps show circular lock waiting
- Some requests complete, others hang (intermittent failures)

---

### Failure 5: SSL Certificate Validation (`/checkout`)

**Trigger**: `POST /checkout` with JSON `{"failureType":"ssl"}`

**What Happens**:
1. CheckoutServlet tries to validate payment processor certificate
2. Normally: certificate is valid, trust chain is OK
3. **With failure injection**: uses self-signed certificate → trust chain invalid
4. SSL handshake fails
5. Checkout process fails

**What You'll See in Logs**:
```
SSL Certificate Validation Failed
Certificate is self-signed or expired
```

**How to Diagnose**:
- SSL/TLS logs show certificate validation errors
- Checkout endpoint returns HTTP error
- Certificate inspection shows validity issues

---

## Getting ByteBite Running

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose 3.8+
- Git (to clone the repository)

### Quick Start (5 minutes)

```bash
# 1. Navigate to project
cd D:\workspace\ai\code\log-analysis-ai-usecase-app

# 2. Start all services
docker-compose up -d

# 3. Wait for services (30-45 seconds)
sleep 45

# 4. Check status
docker-compose ps

# 5. Verify application is accessible
curl http://localhost:8080/bytebite/health
```

### Default Access Credentials

| Service | Username | Password |
|---------|----------|----------|
| ByteBite App | admin | admin |
| PostgreSQL | bytebite | bytebite_secure_pwd_123 |
| OpenLDAP Admin | cn=admin,dc=bytebite,dc=local | admin_secure_pwd_123 |

### Available URLs

| Feature | URL |
|---------|-----|
| **Login Page** | http://localhost:8080/bytebite/login |
| **Menu** | http://localhost:8080/bytebite/menu |
| **Checkout** | http://localhost:8080/bytebite/checkout |
| **Analytics** | http://localhost:8080/bytebite/analytics |
| **Kitchen Display System** | http://localhost:8080/bytebite/kds |
| **Health Check** | http://localhost:8080/bytebite/health |

---

## Monitoring ByteBite Logs

### Real-Time Logs (All Services)
```bash
docker-compose logs -f
```

### Tomcat Logs Only
```bash
docker-compose logs -f tomcat
```

### Filter for Failures
```bash
docker-compose logs tomcat | grep -E "FAILURE|DEADLOCK|OOM|CONNECTION LEAK|SSL"
```

### Search Specific Log File
```bash
docker exec bytebite-tomcat \
  grep "failureType" /usr/local/tomcat/logs/catalina.*.log
```

---

## Directory Structure Inside Container

ByteBite files are organized inside the containers:

### Tomcat Container
```
/usr/local/tomcat/
├── logs/
│   └── catalina.YYYY-MM-DD.log    (Daily log files)
├── conf/
│   ├── server.xml                 (Tomcat config)
│   ├── context.xml                (App context)
│   └── keystore.jks               (SSL certificates)
└── webapps/
    └── bytebite.war               (Deployed application)
```

### PostgreSQL Container
```
/var/lib/postgresql/data/
├── bytebite_db/
└── [database files]
```

### OpenLDAP Container
```
/var/lib/ldap/
└── [directory data]
/etc/ldap/slapd.d/
└── [LDAP configuration]
```

---

## Triggering Failures for Learning

Each failure can be triggered via HTTP request parameter or JSON body:

### Example: Trigger DB Leak
```bash
curl "http://localhost:8080/bytebite/api/menu?failureType=db_leak"
```

### Example: Trigger LDAP Timeout
```bash
curl -X POST "http://localhost:8080/bytebite/login?failureType=ldap_timeout" \
  -d "username=admin&password=admin"
```

### Example: Trigger OOM (Requires Auth)
```bash
# First, get a session
curl -c /tmp/cookies.txt -X POST "http://localhost:8080/bytebite/login" \
  -d "username=admin&password=admin"

# Then trigger OOM
curl -b /tmp/cookies.txt \
  "http://localhost:8080/bytebite/api/analytics?action=all-time-report&failureType=oom"
```

### Example: Trigger Deadlock (Requires Auth)
```bash
curl -b /tmp/cookies.txt -X POST "http://localhost:8080/bytebite/api/kds" \
  -H "Content-Type: application/json" \
  -d '{"orderId":"ORD-1", "status":"COMPLETED", "failureType":"deadlock"}'
```

---

## Key Insights for Troubleshooting

### 1. Failure Injection is Controlled
- Failures only happen when you explicitly request them (with `?failureType=` parameter)
- No random failures, no cascading effects—just what you triggered
- This lets you isolate and diagnose each pattern independently

### 2. Logs Tell the Story
- Every failure leaves diagnostic breadcrumbs in catalina.log
- The log tells you exactly what happened and when
- Your job is learning to read that story

### 3. Reproducibility
- Unlike production, you can reproduce failures on demand
- Makes it safe to experiment with diagnostic techniques
- You can re-trigger the same failure until you fully understand it

### 4. Real Components
- ByteBite uses real technologies (Tomcat, PostgreSQL, OpenLDAP)
- Not simplified or mocked versions
- What you learn here applies directly to production systems

---

## Next Steps

You now understand the ByteBite system structure. In the following chapters, you'll:

1. **Chapter 3**: Learn how to read and interpret logs
2. **Chapters 4-8**: Dive deep into each failure scenario, analyzing logs like a detective
3. **Chapter 9+**: Learn to automate this analysis with AI

Each chapter includes:
- How to trigger the failure
- What symptoms appear
- How to diagnose it systematically
- Real log excerpts you'll analyze
- Tips and tricks from experienced engineers

---

**Next Chapter**: Chapter 3 – Reading Logs Like a Detective
