# Order Processor - Project Details

## Never Forget
- Always use UV for package and venv management
- Always update the project_plan when you finish a task
- Do not Share .env never ever
- Always do TDD - test driven development
- When you finish a task, run all tests to make sure nothing broke
- Always add tests for any new function/feature
- **ALWAYS read PROJECT_PLAN.md before starting ANY phase** - understand expected outcomes and all tasks

## 🎯 CORE GOAL
When you read PROJECT_DETAILS.md and PROJECT_PLAN.md, you should have:
- **Complete context** about what the project is
- **Clear understanding** of what you should and should NOT do
- **Current status** of what's completed and what's pending
- **Next steps** clearly defined

## Overview
An automated order processing system that monitors a folder for new order configurations and executes trades via Alpaca Markets API. The system is designed for paper trading strategies with support for crypto, stocks, and options trading.

## 🚨 CRITICAL RULES - NEVER VIOLATE
1. **Test-Driven Development is MANDATORY** - Write tests FIRST
2. **Run ALL tests after EVERY change** - No exceptions
3. **This is a FINANCIAL application** - Zero tolerance for bugs
4. **Never commit code without passing tests**
5. **Never expose API credentials or sensitive data**
6. **AUDIT LOGGING is MANDATORY** - Every action must be logged for compliance

## Core Requirements

### 1. Technology Stack
- **Python**: Main programming language
- **UV**: Package and virtual environment management
- **Alpaca Markets API**: Direct API usage (not the Python SDK)
- **File-based Configuration**: JSON files for order definitions

### 2. Folder Monitoring System
- **Two-Process Architecture**:
  - **New Order Monitor**: Uses watchdog for event-based detection in `pending/` folder
  - **Status Monitor**: Polls `processing/` folder to check order status with Alpaca
- **Platform-agnostic**: Works on Mac, Windows, Linux, AWS
- **Configurable intervals**: Status polling interval set in `config.yaml` (default: 5 minutes)
- Process orders based on priority (lower number = higher priority)
- Move files through workflow: pending → processing → filled/failed
- Real-time status updates in the JSON files

### 3. Order Types Support
- **Crypto**: BTC/USD, ETH/USD, etc.
- **Stocks**: Regular equity orders
- **Options**: Single and multi-leg strategies (up to 4 legs)

### 4. Order Management
- Place orders via Alpaca REST API
- Monitor order status continuously
- Update status fields in real-time
- Handle partial fills
- Move completed orders to `filled/` folder
- Move failed orders to `failed/` folder with error details

## Project Structure

```
orderprocessor/
├── .env                    # API credentials (NEVER commit)
├── .gitignore             # Git ignore file
├── config.yaml            # Application configuration
├── pyproject.toml         # UV project configuration
├── PROJECT_DETAILS.md     # This file
├── PROJECT_PLAN.md        # Implementation roadmap
├── README.md              # User documentation
│
├── src/
│   ├── __init__.py
│   ├── main.py            # Entry point
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic models
│   ├── monitor.py         # Folder monitoring
│   ├── order_processor.py # Order processing logic
│   ├── api_client.py      # Alpaca API wrapper
│   └── utils.py           # Utilities
│
├── orders/
│   ├── pending/           # New orders placed here
│   ├── processing/        # Orders being processed
│   ├── filled/            # Completed orders
│   └── failed/            # Failed orders
│
├── logs/                  # Application logs
│   ├── app.log           # General application logs
│   ├── audit.log         # Audit trail (DO NOT DELETE)
│   └── error.log         # Error logs
│
├── dashboard/             # Web dashboard for monitoring
│   ├── app.py            # FastAPI application
│   ├── static/           # Frontend files
│   │   ├── index.html    # Main dashboard page
│   │   ├── style.css     # Dashboard styling
│   │   └── app.js        # WebSocket client
│   └── templates/        # HTML templates if needed
│
└── tests/                 # Unit tests
    ├── unit/             # Unit tests for each module
    ├── integration/      # Integration tests
    └── fixtures/         # Test data and mocks
```

## Configuration File (config.yaml)

```yaml
# Application configuration
monitoring:
  new_orders:
    method: "watchdog"              # Event-based monitoring
    folder: "orders/pending"
  
  active_orders:
    method: "polling"               # Status checking
    folder: "orders/processing"
    interval_seconds: 300           # 5 minutes (configurable)
    
api:
  base_url: "https://paper-api.alpaca.markets"  # or live URL
  timeout: 30
  retry_attempts: 3
  rate_limit_per_minute: 200
  
logging:
  level: "INFO"                     # DEBUG, INFO, WARNING, ERROR
  app_log: "logs/app.log"
  audit_log: "logs/audit.log"
  error_log: "logs/error.log"
  rotate_size_mb: 100
  
system:
  timezone: "US/Eastern"            # Market timezone
  market_hours_only: true           # Run only during market hours
  
notifications:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"  # From .env
    chat_id: "${TELEGRAM_CHAT_ID}"      # From .env
```

## Order Configuration Schema

```json
{
  "order_id": "unique_identifier",
  "priority": 1,
  "symbol": "BTC/USD",
  "asset_class": "crypto",
  "order_type": "limit",
  "side": "buy",
  "qty": 0.01,
  "limit_price": 45000,
  "stop_price": null,
  "time_in_force": "day",
  
  // For multi-leg options
  "legs": [...],
  
  // Status tracking (system-managed)
  "status": {
    "current": "pending",
    "submitted_at": null,
    "filled_at": null,
    "filled_qty": 0,
    "filled_avg_price": null,
    "alpaca_order_id": null,
    "last_update": "ISO-8601 timestamp",
    "error": null
  },
  
  // Optional
  "notes": "Strategy description",
  "metadata": {}
}
```

## API Integration Guidelines

### Authentication
- Use API key and secret from `.env` file
- Never hardcode credentials
- Support both paper and live trading endpoints

### Rate Limiting
- Implement exponential backoff
- Respect Alpaca's rate limits
- Queue requests appropriately

### Error Handling
- Retry transient failures
- Log all errors with context
- Graceful degradation
- Clear error messages in failed orders

## Security Requirements

1. **Credentials Management**
   - Store API keys in `.env` file only
   - Never commit `.env` to version control
   - Use environment variables for all secrets

2. **File Permissions**
   - Ensure order files have appropriate permissions
   - Validate all JSON inputs
   - Sanitize file paths

3. **API Security**
   - Use HTTPS for all API calls
   - Validate API responses
   - Handle authentication failures gracefully

## Performance Requirements

1. **Monitoring**
   - Check for new files every 1-2 seconds
   - Process orders within 5 seconds of detection

2. **Order Updates**
   - Poll order status every 1-5 seconds
   - Update JSON files atomically
   - Handle concurrent file access

3. **Resource Usage**
   - Minimize CPU usage during idle periods
   - Efficient file watching (use inotify/FSEvents)
   - Proper connection pooling for API calls

## Development Guidelines

### 🚨 CRITICAL: Test-Driven Development (TDD)
**This is a financial application - NO SURPRISES allowed!**

1. **THE IRON RULE: NO CODE WITHOUT TESTS**
   - **STEP 1**: Write the test FIRST
   - **STEP 2**: Run test - it MUST fail (Red)
   - **STEP 3**: Write minimal code to pass (Green)
   - **STEP 4**: Refactor if needed (Refactor)
   - **STEP 5**: Run ALL tests - must pass

2. **Strict TDD Workflow Example**
   ```python
   # FIRST: Write the test (this comes BEFORE implementation)
   def test_place_order_success():
       """Test that a valid order is placed successfully"""
       order = Order(symbol="AAPL", qty=100, side="buy", order_type="limit", limit_price=150.00)
       result = api_client.place_order(order)
       
       assert result.status == "submitted"
       assert result.alpaca_id is not None
       assert mock_alpaca_api.called_with_correct_params()
   
   # Run test - it MUST fail because place_order() doesn't exist yet
   # ONLY NOW write the actual place_order() function
   ```

3. **Required Test Categories for EVERY Feature**
   - **Happy Path**: Normal successful operation
   - **Error Cases**: Every possible failure mode
   - **Edge Cases**: Boundaries, nulls, empty values, malformed data
   - **Integration**: Interaction with other components

4. **Example: Order Placement Tests (MUST write ALL before coding)**
   ```
   REQUIRED tests before implementing order placement:
   ✓ test_place_order_valid_crypto()
   ✓ test_place_order_valid_stock()
   ✓ test_place_order_valid_option()
   ✓ test_place_order_invalid_symbol()
   ✓ test_place_order_negative_quantity()
   ✓ test_place_order_zero_quantity()
   ✓ test_place_order_insufficient_funds()
   ✓ test_place_order_api_timeout()
   ✓ test_place_order_api_rate_limited()
   ✓ test_place_order_market_closed()
   ✓ test_place_order_invalid_credentials()
   ✓ test_place_order_file_permissions_error()
   ✓ test_place_order_duplicate_order_id()
   ```

5. **Test Framework & Tools**
   - **Framework**: pytest (with pytest-asyncio for async tests)
   - **Mocking**: pytest-mock for external services
   - **Coverage**: pytest-cov (minimum 90%, financial ops 100%)
   - **Run tests**: `uv run pytest tests/ -v --cov=src --cov-report=term-missing`

6. **Coverage Requirements**
   - **Financial operations**: 100% REQUIRED
   - **API interactions**: 100% REQUIRED  
   - **Order processing**: 100% REQUIRED
   - **Error handling**: 100% REQUIRED
   - **File operations**: 95% minimum
   - **Dashboard/UI**: 80% minimum
   - **Overall**: 90% minimum

7. **Test Organization**
   ```
   tests/
   ├── conftest.py           # Shared fixtures
   ├── unit/
   │   ├── test_models.py    # Test data models
   │   ├── test_api_client.py # Test API wrapper
   │   ├── test_monitor.py   # Test file monitoring
   │   └── test_processor.py # Test order processing
   ├── integration/
   │   ├── test_order_flow.py # Full order lifecycle
   │   └── test_error_recovery.py
   └── fixtures/
       ├── valid_orders.json
       └── api_responses.json
   ```

8. **Enforcement Checklist**
   - [ ] Were tests written BEFORE the code?
   - [ ] Do tests cover all failure scenarios?
   - [ ] Are external services properly mocked?
   - [ ] Do tests run in isolation?
   - [ ] Is coverage 100% for financial operations?
   - [ ] Did you run ALL tests after changes?

3. **Code Style**
   - Follow PEP 8
   - Use type hints everywhere
   - Write docstrings for all functions
   - Keep functions focused and small
   - Maximum function length: 20 lines

4. **Error Messages**
   - Clear, actionable error messages
   - Include relevant context
   - Log stack traces for debugging
   - Never expose sensitive information

5. **Audit Logging - MANDATORY**
   - **EVERY action must be logged** - no exceptions
   - Structured logging (JSON format) for easy parsing
   - Log levels: DEBUG, INFO, WARNING, ERROR, AUDIT
   - Include in EVERY log entry:
     - Timestamp (ISO-8601 with timezone)
     - Action performed
     - User/system performing action
     - Order ID (if applicable)
     - Before/after state for changes
     - Result (success/failure)
     - Error details if failed
   - Log retention: Minimum 1 year for audit trail
   - Separate audit log file from application logs
   
   **Order Timeline Events to Log**:
   - `ORDER_DETECTED` - New file found in pending/
   - `ORDER_VALIDATED` - Schema validation passed
   - `ORDER_SUBMITTED` - Sent to Alpaca API
   - `ORDER_ACCEPTED` - Alpaca confirmed order
   - `STATUS_CHECK` - Each monitoring check with before/after status
   - `ORDER_UPDATED` - Any status change (partial fill, etc.)
   - `ORDER_COMPLETED` - Final state (filled/cancelled/failed)
   - `ORDER_MOVED` - File moved between folders
   
   **Status Check Log Format**:
   ```json
   {
     "timestamp": "2025-01-20T10:05:00Z",
     "order_id": "order123",
     "event": "STATUS_CHECK",
     "check_details": {
       "action": "Alpaca API GET /orders/{id}",
       "response_time_ms": 245
     },
     "status_before": {"status": "pending", "filled_qty": 0},
     "status_after": {"status": "partially_filled", "filled_qty": 50},
     "changed": true
   }
   ```

### Testing Checklist (Run after EVERY change)
- [ ] All unit tests pass: `uv run pytest tests/unit/`
- [ ] All integration tests pass: `uv run pytest tests/integration/`
- [ ] Code coverage > 90%: `uv run pytest --cov=src --cov-report=term-missing`
- [ ] Financial operations at 100% coverage
- [ ] No linting errors: `uv run ruff check src/`
- [ ] Type checking passes: `uv run mypy src/`
- [ ] All tests run in < 30 seconds

## Operational Considerations

1. **Startup**
   - Check API connectivity on startup
   - Process any orders left in `processing/` folder
   - Validate folder structure exists

2. **Shutdown**
   - Graceful shutdown on SIGTERM
   - Complete current order processing
   - Save state if needed

3. **Monitoring**
   - Health check endpoint
   - Metrics for orders processed/failed
   - Alert on repeated failures

## Web Dashboard

### Purpose
Provide real-time visibility into order processing with a complete timeline for each order.

### Technology Stack
- **Backend**: FastAPI (async Python web framework)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no complex frameworks)
- **Real-time**: WebSockets for live updates
- **Database**: SQLite for order event history (optional)

### Dashboard Features

1. **Order List View**
   - Real-time order status updates
   - Filter by status (pending, filled, failed)
   - Filter by date range
   - Search by order ID or symbol
   - Color-coded status indicators

2. **Order Timeline View**
   - Complete chronological event log for each order
   - Shows every status check with before/after state
   - Visual progress indicator
   - Time between events
   - API response times

3. **Live Updates**
   - WebSocket connection for real-time updates
   - No page refresh needed
   - New orders appear automatically
   - Status changes highlighted

### API Endpoints
- `GET /api/orders` - List all orders with current status
- `GET /api/orders/{id}` - Get specific order details
- `GET /api/orders/{id}/timeline` - Get complete event timeline
- `WS /ws` - WebSocket for live updates
- `GET /api/stats` - System statistics (orders/hour, success rate)

### Dashboard URL
- Default: `http://localhost:8000`
- Configurable in `config.yaml`

## Notification System

### Purpose
Provide real-time alerts via Telegram for important events based on severity levels.

### Severity Levels

**SEV 1 - CRITICAL** 🔴
- **Action**: Immediate Telegram message + repeat every 5 min until acknowledged
- **Examples**:
  - System cannot connect to Alpaca API
  - Multiple order failures in succession
  - File permission errors
  - Unexpected system shutdown
- **Format**: `🚨 CRITICAL: {message}`

**SEV 2 - HIGH** 🟠
- **Action**: Immediate Telegram message (no repeats)
- **Examples**:
  - Order rejected by Alpaca
  - Order stuck in processing > 30 min
  - API rate limit reached
- **Format**: `⚠️ HIGH: {message}`

**SEV 3 - MEDIUM** 🟡
- **Action**: Batch Telegram message every 30 minutes
- **Examples**:
  - Order filled successfully
  - Partial fills
  - Configuration changes
- **Format**: `📋 Update: {count} events...`

**SEV 4 - LOW** 🟢
- **Action**: Daily summary via Telegram at market close
- **Examples**:
  - Daily statistics
  - Performance metrics
  - System health summary
- **Format**: `📊 Daily Summary: {stats}`

**SEV 5 - INFO** ⚪
- **Action**: Dashboard only (NO Telegram)
- **Examples**:
  - Routine status checks
  - Heartbeat logs
  - Debug information

### Telegram Configuration
```yaml
notifications:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"  # From .env
    chat_id: "${TELEGRAM_CHAT_ID}"      # From .env
    
  severity_settings:
    sev1:
      immediate: true
      repeat_minutes: 5
      require_ack: true
    sev2:
      immediate: true
    sev3:
      batch_minutes: 30
    sev4:
      daily_time: "16:00"  # 4 PM ET
    sev5:
      telegram_enabled: false  # Dashboard only
      
  event_severity_mapping:
    api_connection_lost: 1
    system_crash: 1
    order_failed: 2
    order_stuck: 2
    order_filled: 3
    partial_fill: 3
    daily_stats: 4
    status_check: 5
    heartbeat: 5
```

### Message Examples
```
🚨 CRITICAL: Cannot connect to Alpaca API!
Order processing halted. Check credentials.
Time: 2025-01-20 10:30:45 ET

⚠️ HIGH: Order order123 FAILED
Symbol: AAPL
Quantity: 100
Reason: Insufficient funds
Time: 2025-01-20 11:15:22 ET

📊 Daily Summary (2025-01-20)
Total Orders: 25
✅ Filled: 23 (92%)
❌ Failed: 2 (8%)
💰 Volume: $45,230
⏱️ Avg Fill Time: 3.2 min
```

## Future Enhancements (Not in MVP)
- Database for order history
- Advanced order types (OCO, trailing stop)
- Portfolio management features
- Risk management rules
- Strategy backtesting
- Mobile app
- Email/SMS notifications