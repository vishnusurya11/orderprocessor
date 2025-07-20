# Order Processor - Project Plan

## Project Status: 🚧 In Development

Last Updated: 2025-01-20

## Overview
This plan tracks the development from MVP (basic order processing) to full product (dashboard, notifications, production-ready).

## 🎯 MVP (Minimum Viable Product)
**Goal**: Basic order processing that can place and track orders

### ✅ Phase 0: Project Planning & Documentation
- [x] Define project requirements and structure
- [x] Create PROJECT_DETAILS.md documentation  
- [x] Design order configuration schema
- [x] Plan monitoring approach (watchdog + polling)
- [x] Define logging requirements
- [x] Setup notification system design
- [x] Establish TDD workflow

### ✅ Phase 1: Project Setup & Infrastructure
**Status**: COMPLETED | **Completed**: Jan 20, 2025

**Expected Outcome**: Complete project skeleton ready for development with all tools configured

- [x] Initialize UV project with pyproject.toml
  - [x] Add all dependencies (watchdog, httpx, pydantic, pytest, fastapi, etc.)
  - [x] Configure pytest settings (pytest.ini)
  - [x] Setup linting (ruff) and type checking (mypy)
  - [x] Configure pre-commit hooks
  
- [x] Create .gitignore file with:
  - [x] .env, __pycache__, .pytest_cache
  - [x] logs/*.log, orders/*/
  - [x] .coverage, htmlcov/
  
- [x] Create folder structure:
  ```
  alpaca-trade-manager/
  ├── orders/
  │   ├── pending/      # Watch this folder
  │   ├── processing/   # Active orders here
  │   ├── filled/       # Completed orders
  │   └── failed/       # Failed orders
  ├── logs/            # All log files
  ├── src/
  │   ├── __init__.py
  │   └── (empty for now)
  └── tests/
      ├── __init__.py
      ├── conftest.py   # Pytest fixtures
      ├── unit/
      └── integration/
  ```
  
- [x] Setup Git repository
  - [x] git init
  - [x] Initial commit with structure
  - [x] Create develop branch
  - [x] Setup branch protection rules (manual)
  
- [x] Create config.yaml template with all settings
- [x] Create .env.example with:
  ```
  ALPACA_API_KEY=your_api_key_here
  ALPACA_SECRET_KEY=your_secret_here
  TELEGRAM_BOT_TOKEN=your_bot_token
  TELEGRAM_CHAT_ID=your_chat_id
  ```

**Verification**: ✅
- Can run `uv run pytest` (warns about no tests)
- Can run `uv run ruff check src/` (no errors)
- Can run `uv run mypy src/` (no errors)
- Folder structure exists and is correct
- All dependencies installed with `uv sync`

### Phase 2: Core Models & Configuration (TDD)
**Status**: Not Started | **Target**: Week 1

**Expected Outcome**: Fully validated data models and configuration system with 100% test coverage

- [ ] **Order Model** (src/models.py)
  - [ ] Write comprehensive tests FIRST (tests/unit/test_models.py):
    - [ ] test_order_validation_valid_crypto (BTC/USD with all fields)
    - [ ] test_order_validation_valid_stock (AAPL with limit order)
    - [ ] test_order_validation_valid_options (Multi-leg strategy)
    - [ ] test_order_validation_invalid_symbol (empty, special chars)
    - [ ] test_order_validation_invalid_quantity (negative, zero, too large)
    - [ ] test_order_validation_missing_required_fields
    - [ ] test_order_priority_validation (must be positive integer)
    - [ ] test_order_json_serialization
    - [ ] test_order_status_initialization
  - [ ] Implement Order Pydantic model with:
    - [ ] All fields from schema (order_id, symbol, qty, etc.)
    - [ ] Proper validation rules
    - [ ] Status sub-model
    - [ ] Support for options legs
  - [ ] All tests passing (100% coverage)
  
- [ ] **Configuration Model** (src/config.py)
  - [ ] Write tests first (tests/unit/test_config.py):
    - [ ] test_load_config_from_yaml
    - [ ] test_config_env_override (env vars override YAML)
    - [ ] test_config_missing_file_uses_defaults
    - [ ] test_config_invalid_yaml_raises_error
    - [ ] test_config_validates_required_fields
  - [ ] Implement Config loader with:
    - [ ] YAML file parsing
    - [ ] Environment variable substitution
    - [ ] Default values
    - [ ] Validation of all settings
  - [ ] All tests passing

- [ ] **Logging Setup** (src/utils.py)
  - [ ] Write tests first (tests/unit/test_utils.py):
    - [ ] test_logger_json_format
    - [ ] test_audit_logger_separate_file
    - [ ] test_log_rotation_size
    - [ ] test_log_includes_all_fields
  - [ ] Implement logging with:
    - [ ] JSON structured format
    - [ ] Separate audit logger
    - [ ] Proper log levels
    - [ ] Rotation by size
  - [ ] All tests passing

**Verification**:
- Run `uv run pytest tests/unit/ -v` - all tests pass
- Run `uv run pytest --cov=src --cov-report=term-missing` - 100% coverage
- Models properly validate all edge cases
- Can load and parse config.yaml

### Phase 3: Alpaca API Client (TDD)
**Status**: Not Started | **Target**: Week 2

**Expected Outcome**: Robust API client that handles all edge cases with 100% test coverage

- [ ] **API Authentication** (src/api_client.py)
  - [ ] Write tests first (tests/unit/test_api_client.py):
    - [ ] test_auth_with_valid_credentials
    - [ ] test_auth_with_invalid_credentials_raises
    - [ ] test_paper_trading_url_selection
    - [ ] test_live_trading_url_selection
    - [ ] test_missing_env_vars_raises_clear_error
  - [ ] Implement AlpacaClient class with:
    - [ ] Credential loading from env
    - [ ] Paper/Live URL switching
    - [ ] Proper auth headers
    - [ ] Connection testing
  
- [ ] **Order Placement**
  - [ ] Write comprehensive tests with mocked responses:
    - [ ] test_place_order_success_crypto
    - [ ] test_place_order_success_stock
    - [ ] test_place_order_success_option_multi_leg
    - [ ] test_place_order_insufficient_funds_error
    - [ ] test_place_order_invalid_symbol_error
    - [ ] test_place_order_market_closed_error
    - [ ] test_place_order_timeout_with_retry
    - [ ] test_place_order_rate_limit_backoff
    - [ ] test_place_order_network_error_retry
    - [ ] test_place_order_malformed_response
  - [ ] Implement place_order method with:
    - [ ] Full order type support
    - [ ] Proper error handling
    - [ ] Retry logic using tenacity
    - [ ] Rate limit respect
    - [ ] Clear error messages
  
- [ ] **Order Status Checking**
  - [ ] Write tests for all states:
    - [ ] test_get_order_status_pending
    - [ ] test_get_order_status_filled
    - [ ] test_get_order_status_partially_filled
    - [ ] test_get_order_status_cancelled
    - [ ] test_get_order_status_rejected
    - [ ] test_get_order_status_not_found
    - [ ] test_get_order_status_api_error
  - [ ] Implement get_order_status with:
    - [ ] Parse all order states
    - [ ] Return standardized format
    - [ ] Handle missing orders
  
- [ ] **Integration Helpers**
  - [ ] Create mock fixtures for all API responses
  - [ ] Document all possible API errors
  - [ ] Add request/response logging

**Verification**:
- All API calls properly mocked in tests
- Retry logic works correctly
- 100% test coverage on api_client.py
- Can switch between paper/live trading

### Phase 4: Basic Order Processing (TDD)
**Status**: Not Started | **Target**: Week 2

**Expected Outcome**: Complete order processing pipeline from file detection to order placement

- [ ] **File Monitoring** (src/monitor.py)
  - [ ] Write tests first (tests/unit/test_monitor.py):
    - [ ] test_detect_new_json_file
    - [ ] test_ignore_non_json_files
    - [ ] test_handle_multiple_files_by_priority
    - [ ] test_file_validation_before_queue
    - [ ] test_duplicate_order_id_detection
    - [ ] test_watchdog_error_recovery
  - [ ] Implement FileMonitor with:
    - [ ] Watchdog event handler
    - [ ] JSON file validation
    - [ ] Priority queue (heapq)
    - [ ] Duplicate detection
    - [ ] Error handling
  
- [ ] **Order Processor** (src/order_processor.py)
  - [ ] Write integration tests (tests/integration/test_order_flow.py):
    - [ ] test_process_valid_order_end_to_end
    - [ ] test_move_file_pending_to_processing
    - [ ] test_move_file_processing_to_filled
    - [ ] test_move_file_processing_to_failed
    - [ ] test_update_json_status_during_processing
    - [ ] test_handle_api_failure_gracefully
    - [ ] test_process_multiple_orders_by_priority
    - [ ] test_recovery_from_crash
  - [ ] Implement OrderProcessor with:
    - [ ] Take order from queue
    - [ ] Move to processing/
    - [ ] Call API client
    - [ ] Update JSON status
    - [ ] Move to final folder
    - [ ] Audit logging
  
- [ ] **Main Application** (src/main.py)
  - [ ] Write tests (tests/unit/test_main.py):
    - [ ] test_app_startup_checks
    - [ ] test_graceful_shutdown_sigterm
    - [ ] test_recovery_processing_folder
    - [ ] test_config_loading
    - [ ] test_thread_coordination
  - [ ] Implement main app with:
    - [ ] Load configuration
    - [ ] Start monitor thread
    - [ ] Start processor thread
    - [ ] Signal handlers
    - [ ] Health checks
    - [ ] Clean shutdown

**Verification**:
- Can process a test order file end-to-end
- Files move correctly between folders
- Status updates work
- Graceful shutdown works
- All tests passing

### Phase 5: MVP Testing & Validation
**Status**: Not Started | **Target**: Week 3

**Expected Outcome**: Production-ready MVP that reliably processes orders

- [ ] **Integration Testing**
  - [ ] Create test order files for all scenarios:
    - [ ] Valid crypto order (BTC/USD)
    - [ ] Valid stock order (AAPL)
    - [ ] Invalid orders (missing fields, bad data)
    - [ ] High priority order processing
  - [ ] Run end-to-end tests:
    - [ ] Place 10 orders rapidly
    - [ ] Verify correct processing order
    - [ ] Check all files moved correctly
    - [ ] Verify audit logs complete
  
- [ ] **Paper Trading Validation**
  - [ ] Configure for Alpaca paper account
  - [ ] Test each order type:
    - [ ] Market orders
    - [ ] Limit orders
    - [ ] Stop orders
  - [ ] Verify with Alpaca dashboard
  - [ ] Check status updates accurate
  
- [ ] **Performance Testing**
  - [ ] Measure order processing time
  - [ ] Test with 100 orders in queue
  - [ ] Monitor CPU/memory usage
  - [ ] Verify 5-second target met
  
- [ ] **Bug Fixes & Hardening**
  - [ ] Fix any issues found
  - [ ] Add tests for bug scenarios
  - [ ] Re-run all tests
  - [ ] Update documentation
  
- [ ] **MVP Documentation**
  - [ ] Create quick start guide
  - [ ] Document order file format
  - [ ] List common errors
  - [ ] Add troubleshooting section

**Verification**:
- Processed 100+ test orders successfully
- No crashes during 24-hour test run
- All edge cases handled gracefully
- Ready for real paper trading

## 🚀 Full Product Features

### Phase 6: Active Order Monitoring
**Status**: Not Started | **Target**: Week 3

**Expected Outcome**: Continuous monitoring of active orders with detailed status tracking

- [ ] **Status Monitor Service** (src/status_monitor.py)
  - [ ] Write tests first (tests/unit/test_status_monitor.py):
    - [ ] test_poll_processing_folder
    - [ ] test_check_order_status_change
    - [ ] test_update_json_with_new_status
    - [ ] test_detect_filled_orders
    - [ ] test_detect_failed_orders
    - [ ] test_handle_partial_fills
    - [ ] test_configurable_poll_interval
  - [ ] Implement StatusMonitor with:
    - [ ] Scan processing/ folder
    - [ ] Check each order status via API
    - [ ] Compare before/after states
    - [ ] Update JSON if changed
    - [ ] Move completed orders
    - [ ] Log all status checks
  
- [ ] **Enhanced Event Logging**
  - [ ] Add detailed event types:
    - [ ] STATUS_CHECK (with before/after)
    - [ ] STATUS_CHANGED
    - [ ] PARTIAL_FILL
    - [ ] ORDER_COMPLETED
  - [ ] Include timing metrics:
    - [ ] Time since submission
    - [ ] Time in current state
    - [ ] API response time
  
- [ ] **Integration with Main App**
  - [ ] Add status monitor thread
  - [ ] Coordinate with processor
  - [ ] Share API client instance
  - [ ] Prevent conflicts

**Verification**:
- Status checks run every 5 minutes
- Changes detected and logged
- Files move when orders complete
- No race conditions

### Phase 7: Web Dashboard
**Status**: Not Started | **Target**: Week 4

- [ ] **Backend API**
  - [ ] FastAPI app structure
  - [ ] Order list endpoint
  - [ ] Order timeline endpoint
  - [ ] WebSocket support
  - [ ] Write API tests
  
- [ ] **Frontend**
  - [ ] HTML/CSS layout
  - [ ] JavaScript for updates
  - [ ] Real-time WebSocket
  - [ ] Order filtering/search

### Phase 8: Telegram Notifications
**Status**: Not Started | **Target**: Week 4

- [ ] **Notification Service**
  - [ ] Write tests for Telegram client
  - [ ] Implement severity levels
  - [ ] Message formatting
  - [ ] Batching logic
  
- [ ] **Integration**
  - [ ] Hook into order events
  - [ ] Daily summaries
  - [ ] Error alerts

### Phase 9: Production Readiness
**Status**: Not Started | **Target**: Week 5

- [ ] **Error Recovery**
  - [ ] Startup recovery tests
  - [ ] Crash recovery
  - [ ] Data integrity checks
  
- [ ] **Performance**
  - [ ] Load testing
  - [ ] Optimization
  - [ ] Resource monitoring
  
- [ ] **Documentation**
  - [ ] Complete README
  - [ ] API documentation
  - [ ] Deployment guide
  - [ ] Troubleshooting guide

### Phase 10: Deployment & Operations
**Status**: Not Started | **Target**: Week 5

- [ ] **Deployment Scripts**
  - [ ] systemd service file
  - [ ] Environment setup script
  - [ ] Health check endpoint
  
- [ ] **Monitoring**
  - [ ] Metrics collection
  - [ ] Alerting setup
  - [ ] Log aggregation
  
- [ ] **Optional Enhancements**
  - [ ] Docker containerization
  - [ ] Kubernetes deployment
  - [ ] CI/CD pipeline

## Git Workflow 📋

### Branch Strategy
- `main` - Production ready code only
- `develop` - Integration branch
- `feature/*` - Individual features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Emergency fixes

### Commit Convention
```
feat: Add order validation
fix: Handle API timeout correctly  
test: Add tests for order processor
docs: Update README with examples
refactor: Simplify status checking logic
```

### Pull Request Process
1. Create feature branch from develop
2. Write tests first (TDD)
3. Implement feature
4. All tests must pass
5. Update PROJECT_PLAN.md
6. Create PR to develop
7. Code review required
8. Merge when approved

## Development Log 📅

### Week 1 (Jan 20-26, 2025)
- [x] Jan 20: Completed project planning and documentation
- [x] Jan 20: Completed Phase 1 - Project setup and infrastructure
- [ ] Jan 21: Start Phase 2 - Core models with TDD
- [ ] Jan 22-23: Complete models and configuration
- [ ] Jan 24-25: Start Phase 3 - API client
- [ ] Jan 26: Weekly review and planning

### Week 2 (Jan 27 - Feb 2, 2025)
- [ ] Complete API client
- [ ] Implement order processing
- [ ] MVP testing

[Additional weeks to be planned...]

## Testing Strategy 🧪

### Test Coverage Requirements
- **Overall**: 90% minimum
- **Financial Operations**: 100% required
- **API Interactions**: 100% required
- **Error Handling**: 100% required

### Test Execution
```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_models.py -v

# Run only unit tests
uv run pytest tests/unit/ -v

# Run only integration tests  
uv run pytest tests/integration/ -v
```

## Success Criteria ✅

### MVP Success
- [ ] Can process orders from JSON files
- [ ] Orders successfully placed with Alpaca
- [ ] Status tracked and files moved correctly
- [ ] All tests passing with >90% coverage
- [ ] No critical bugs in paper trading

### Full Product Success
- [ ] Dashboard shows real-time order status
- [ ] Telegram notifications working
- [ ] 99% uptime during market hours
- [ ] <5 second order processing time
- [ ] Zero duplicate orders
- [ ] Complete audit trail

## Risk Register 🚨

| Risk | Impact | Mitigation |
|------|---------|------------|
| API Rate Limits | High | Implement queuing and backoff |
| File System Issues | High | Atomic operations, locks |
| Network Failures | Medium | Retry logic, offline queue |
| Data Loss | High | Status persistence, backups |
| Security Breach | Critical | Env vars, no hardcoded secrets |

## Next Immediate Actions 🎯

1. Initialize UV project with all dependencies
2. Create folder structure
3. Setup Git repository
4. Write first tests for Order model
5. Implement Order model to pass tests

## Questions/Blockers ❓

- None currently

## Notes 📝

- Always follow TDD - tests first, then code
- Update this plan after completing each task
- Run all tests before any commit
- Keep MVP scope minimal - just order processing
- Add features incrementally after MVP works