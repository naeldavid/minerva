
# API Documentation

## Endpoints

### GET /
Returns the main dashboard page.

### GET /api/system-stats
Returns real-time system statistics.

**Response:**
```json
{
  "cpu_usage": 25.3,
  "memory_usage": 45.7,
  "temperature": 42.1,
  "uptime": 12.5,
  "network": {
    "bytes_sent": 123456,
    "bytes_recv": 789012
  }
}
```

### GET /api/miner-stats
Returns live mining statistics.

**Response:**
```json
{
  "hashrate": 120,
  "total_mined": 0.00012345,
  "uptime": 3600,
  "estimated_daily_yield": 0.0012
}
```

### POST /api/chat
Processes AI chat requests.

**Request:**
```json
{
  "message": "Explain Raspberry Pi"
}
```

**Response:**
```json
{
  "response": {
    "content": "Raspberry Pi is a series of small computers...",
    "format": "text"
  }
}
```

### GET /health
Returns health status of the application.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "modules": {
    "system_stats": true,
    "miner_stats": true,
    "ai_client": true
  }
}
```
