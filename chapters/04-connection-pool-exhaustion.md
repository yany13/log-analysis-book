# Chapter 4: Connection Pool Exhaustion (DB Leak)
## Diagnosing Resource Starvation

---

## The Failure Pattern

### What Happens

When an application doesn't properly close database connections, they remain in use even after the code finishes with them. HikariCP (the connection pool) has a fixed size (default: 20 connections). Once all connections are held and none are available for new requests, new requests wait for a connection to become available.

**Timeline:**
1. **Normal state** (first 19 requests): Connections available → requests process → connections returned → success
2. **Request 20** (pool fills): All 20 connections now in use
3. **Request 21** (no available): Waits up to 30 seconds for a connection
4. **Request 21** (timeout): No connections freed → timeout error
5. **Cascade** (requests queue up): All subsequent requests timeout

### Why This Happens in Production

1. **Forgotten connection close** - Developer writes:
   ```java
   Connection conn = pool.getConnection();
   PreparedStatement stmt = conn.prepareStatement(sql);
   stmt.executeQuery();  // Forgot: stmt.close() and conn.close()
   ```

2. **Exception before close** - Connection close is skipped:
   ```java
   Connection conn = pool.getConnection();
   stmt = conn.prepareStatement(sql);
   if (badData) throw new Exception();  // Never reaches close()
   stmt.close();
   conn.close();
   ```

3. **Long-running transactions** - Holding connections during slow operations

4. **Thread crash** - Thread holding connection dies without closing it

---

## How to Trigger the Failure in ByteBite

### Step 1: Start the System
```bash
cd D:\workspace\ai\code\log-analysis-ai-usecase-app
docker-compose up -d
sleep 45
docker-compose ps
```

### Step 2: Trigger the Failure
```bash
# First request (triggers failure injection, leaks connection)
curl "http://localhost:8080/bytebite/api/menu?failureType=db_leak"

# Subsequent requests (each leaks a connection)
for i in {1..20}; do
  curl "http://localhost:8080/bytebite/api/menu?failureType=db_leak" &
done
wait

# Once pool is exhausted, normal requests also timeout
curl "http://localhost:8080/bytebite/api/menu"
```

### Step 3: Monitor Logs in Real-Time
```bash
docker-compose logs -f tomcat | grep -E "Connection|leak|timeout|HikariPool"
```

---

## What the Logs Reveal

### Expected Log Output

As you trigger the failure, watch for these patterns:

```
[HikariPool housekeeper] 
  ⚠️ Connection leak scenario - connections being held
  DEBUG: getConnection timeout approaching (28/30 seconds)

[MenuServlet] 
  Retrieving menu items from database
  ⚠️ Connection leak scenario detected
  Closing statement but NOT returning connection

[HikariPool] 
  Connections: 0 available, 20 pending, 20 total
  ❌ Connection is not available, request timed out after 30000ms
```

### Key Signals to Look For

| Signal | Meaning |
|--------|---------|
| `getConnection()` calls increasing in logs | More requests competing for connections |
| `available: 0` | No connections currently available |
| `pending: <high number>` | Requests waiting for a connection |
| Timeout after 30000ms | Waited full 30 seconds, gave up |
| Same request pattern repeating | Indicates systematic leak, not random issue |

---

## Diagnostic Approach: The 4-Step Method

### Step 1: Identify the Failure Window
**Question**: When did things start going wrong?

Look for the first occurrence of:
```
Connection is not available, request timed out
```

This is your failure start time. Everything before this was probably fine.

### Step 2: Correlate with Request Rate
**Question**: What changed? Did request volume spike?

Check the request logging filter output:
```bash
docker-compose logs tomcat | grep "RequestLoggingFilter" | grep -c "menu"
```

If menu requests suddenly went from 1/sec to 100/sec, request spike → possible legitimate cause.
If steady 5/sec with sudden timeout, likely a leak.

### Step 3: Check HikariCP Pool State
**Question**: Are connections being released?

Look for patterns like:
```
Available connections: 20 → 19 → 18 → 17 ... → 1 → 0 (stays at 0)
```

If it drops to zero and **stays there**, something is holding connections.
If it fluctuates, connections are being released (healthy).

### Step 4: Find the Culprit Code
**Question**: Which endpoint is leaking?

Check the logs for which endpoint was executing:
```
MenuServlet processing request
AnalyticsServlet processing request
KDSServlet processing request
```

When you see the timeout, trace back to which servlet was running.

---

## Real-World Analysis: Sample Log Session

### Initial State (Pool Healthy)
```
[HikariPool-1] Created new connection for thread Thread-23
[HikariPool-1] Available connections: 20
[MenuServlet] Retrieved 12 menu items
```
✅ Connections acquired and released normally

### Early Stages (Leak Starting)
```
[MenuServlet] Retrieved 12 menu items
⚠️ Connection leak scenario detected
[HikariPool-1] Available connections: 19
[MenuServlet] Retrieved 12 menu items
⚠️ Connection leak scenario detected
[HikariPool-1] Available connections: 18
```
⚠️ Available count dropping—connections not being returned

### Mid Stage (Pressure Building)
```
[HikariPool-1] Available connections: 5
[RequestLoggingFilter] GET /api/menu - Started
[RequestLoggingFilter] GET /api/menu - Started
[RequestLoggingFilter] GET /api/menu - Started
[MenuServlet] Waiting for connection... (0 available, 3 pending)
[MenuServlet] Waiting for connection... (0 available, 4 pending)
```
⚠️ Multiple requests queued, waiting for connections

### Failure (Pool Exhausted)
```
[HikariPool-1] Available connections: 0
[HikariPool-1] Pending requests: 7
[MenuServlet] ❌ Connection is not available, request timed out after 30000ms
[MenuServlet] ❌ Unable to get menu - database connection timeout
[RequestLoggingFilter] GET /api/menu - Response: 500 Internal Server Error (30123ms)
```
❌ Complete pool exhaustion—requests failing

---

## Differentiate from Similar Issues

### Connection Leak vs. Database Overload

| Connection Leak | Database Overload |
|---|---|
| **Pool size drops then stays low** | **Connections in use but functional** |
| **Timeout at 30 seconds** | **Slow responses, but complete** |
| **Same requests affected** | **All requests slow uniformly** |
| **Fix: find code leak** | **Fix: tune queries, add indexes** |

**How to tell**: If the problem goes away after 10 minutes, database might have recovered from overload. If it persists for hours, likely a connection leak.

### Connection Leak vs. Network Issue

| Connection Leak | Network Timeout |
|---|---|
| **Log shows HikariPool timeout** | **No HikariPool message** |
| **Other services unaffected** | **Network calls fail across services** |
| **Database itself is responsive** | **Database connection itself slow** |

**How to tell**: SSH into database container and check if it's responsive. If yes, then it's not network.

---

## Hunting the Leak: Code Patterns

Once you've identified the endpoint causing the leak, check the code for these patterns:

### ❌ Pattern 1: No Finally Block
```java
Connection conn = pool.getConnection();
PreparedStatement stmt = conn.prepareStatement(sql);
stmt.executeQuery();
stmt.close();
conn.close();  // Never reached if exception occurs above
```

**Problem**: Exception before close() leaves connection hanging.

### ✅ Fix 1: Try-With-Resources (Modern)
```java
try (Connection conn = pool.getConnection();
     PreparedStatement stmt = conn.prepareStatement(sql)) {
    stmt.executeQuery();
}  // Automatically closes both
```

### ❌ Pattern 2: Connection in Object, Forgotten Close
```java
public class OrderService {
    private Connection conn;  // Oops: connection as field
    
    public void processOrder() {
        conn = pool.getConnection();
        // ... process ...
        // Developer forgot to close conn
    }
}
```

**Problem**: Connection stays open as long as service object exists.

### ✅ Fix 2: Use Try-Catch-Finally
```java
Connection conn = null;
try {
    conn = pool.getConnection();
    // ... process ...
} finally {
    if (conn != null) conn.close();
}
```

### ❌ Pattern 3: Exception Swallowing
```java
try {
    Connection conn = pool.getConnection();
    // ... query ...
    conn.close();
} catch (Exception e) {
    logger.error("Failed", e);
    // Developer forgot to close connection in catch block
}
```

---

## Mitigation Strategies

### Short Term (During Incident)
1. **Restart the service**: Clears all leaked connections
   ```bash
   docker-compose restart tomcat
   ```

2. **Increase pool size** (temporary): Buys time while investigating
   Edit `docker/tomcat/server.xml`:
   ```xml
   <maxTotal>40</maxTotal>  <!-- Increased from 20 -->
   ```

3. **Block the offending endpoint**: Reduce load on pool
   Edit filter configuration to return 503 for the problematic endpoint

### Long Term (Fix)
1. **Find and fix the leak**: Review code patterns above
2. **Add tests**: Test for connection leaks:
   ```java
   @Test
   public void testMenuServletClosesConnections() {
       // Trigger 1000 requests
       // Verify pool still has available connections
       assertEquals("Pool should have capacity", 20, pool.getAvailableCount());
   }
   ```

3. **Add monitoring**: Track available connections, alert when < 5:
   ```
   ALERT: HikariPool available connections < 5 (current: 3)
   ```

---

## Key Takeaways for DB Connection Leaks

1. **Always use try-with-resources or try-finally** to guarantee cleanup
2. **Never hold connections longer than necessary** - get, use, close
3. **Monitor pool metrics** - if available connections drop and don't recover, investigate immediately
4. **Reproduce locally** - trigger the failure, confirm your fix works, test at scale
5. **Load test** - run 1000+ concurrent requests to catch leaks that only happen under load

---

## Chapter Review Questions

1. What's the difference between a connection leak and a database that's overloaded?
2. Why do connections not get released in exception scenarios?
3. What's the advantage of try-with-resources over try-finally-close?
4. How would you set an alert to catch connection pool exhaustion before it affects users?
5. If pool size is 20 and you have 100 concurrent users, what happens?

---

**Next Chapter**: Chapter 5 – Authentication Service Failures (LDAP Timeout)
