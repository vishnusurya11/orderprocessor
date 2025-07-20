"""Pytest configuration and shared fixtures."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_order_data() -> Dict[str, Any]:
    """Return valid order data for testing."""
    return {
        "order_id": "test_order_123",
        "priority": 1,
        "symbol": "AAPL",
        "asset_class": "us_equity",
        "order_type": "limit",
        "side": "buy",
        "qty": 100,
        "limit_price": 150.00,
        "time_in_force": "day",
        "status": {
            "current": "pending",
            "submitted_at": None,
            "filled_at": None,
            "filled_qty": 0,
            "filled_avg_price": None,
            "alpaca_order_id": None,
            "last_update": "2025-01-20T12:00:00Z",
            "error": None
        },
        "notes": "Test order",
        "metadata": {}
    }


@pytest.fixture
def temp_order_dirs(tmp_path: Path) -> Generator[Dict[str, Path], None, None]:
    """Create temporary order directories for testing."""
    dirs = {
        "pending": tmp_path / "orders" / "pending",
        "processing": tmp_path / "orders" / "processing",
        "filled": tmp_path / "orders" / "filled",
        "failed": tmp_path / "orders" / "failed",
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    yield dirs


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up mock environment variables for testing."""
    monkeypatch.setenv("ALPACA_API_KEY", "test_api_key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test_secret_key")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test_chat_id")


@pytest.fixture
def mock_alpaca_response() -> Dict[str, Any]:
    """Return mock Alpaca API response for order placement."""
    return {
        "id": "alpaca_order_12345",
        "client_order_id": "test_order_123",
        "created_at": "2025-01-20T12:00:00Z",
        "updated_at": "2025-01-20T12:00:00Z",
        "submitted_at": "2025-01-20T12:00:00Z",
        "filled_at": None,
        "expired_at": None,
        "canceled_at": None,
        "failed_at": None,
        "replaced_at": None,
        "replaced_by": None,
        "replaces": None,
        "asset_id": "asset_123",
        "symbol": "AAPL",
        "asset_class": "us_equity",
        "notional": None,
        "qty": "100",
        "filled_qty": "0",
        "filled_avg_price": None,
        "order_class": "",
        "order_type": "limit",
        "type": "limit",
        "side": "buy",
        "time_in_force": "day",
        "limit_price": "150.00",
        "stop_price": None,
        "status": "pending_new",
        "extended_hours": False,
        "legs": None
    }


@pytest.fixture
def config_yaml_content() -> str:
    """Return sample config.yaml content for testing."""
    return """
monitoring:
  new_orders:
    method: "watchdog"
    folder: "orders/pending"
  
  active_orders:
    method: "polling"
    folder: "orders/processing"
    interval_seconds: 300
    
api:
  base_url: "https://paper-api.alpaca.markets"
  timeout: 30
  retry_attempts: 3
  rate_limit_per_minute: 200
  
logging:
  level: "INFO"
  app_log: "logs/app.log"
  audit_log: "logs/audit.log"
  error_log: "logs/error.log"
  rotate_size_mb: 100
  
system:
  timezone: "US/Eastern"
  market_hours_only: true
  
notifications:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
"""