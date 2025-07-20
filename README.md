# Alpaca Trade Manager

An automated trade management and order processing system for Alpaca Markets API. This system monitors a folder for order configuration files and automatically places and tracks orders through their lifecycle.

## Features

- 📁 **File-based Order Processing**: Drop JSON files to place orders
- 🔄 **Automated Order Lifecycle**: From placement to completion
- 📊 **Real-time Status Tracking**: Monitor order progress
- 🌐 **Web Dashboard**: Live order monitoring interface
- 📱 **Telegram Notifications**: Alerts based on severity levels
- 🔒 **Comprehensive Audit Trail**: Complete logging for compliance
- 🚀 **High Performance**: Process orders within seconds

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alpaca-trade-manager
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Add your Alpaca API credentials
   - Configure Telegram bot (optional)

4. **Run the system**
   ```bash
   uv run python -m src.main
   ```

5. **Place an order**
   - Create a JSON file with order details
   - Drop it in `orders/pending/`
   - Watch it process automatically!

## Order File Format

```json
{
  "order_id": "unique_order_123",
  "priority": 1,
  "symbol": "AAPL",
  "asset_class": "us_equity",
  "order_type": "limit",
  "side": "buy",
  "qty": 100,
  "limit_price": 150.00,
  "time_in_force": "day"
}
```

## Project Structure

```
alpaca-trade-manager/
├── orders/              # Order file directories
│   ├── pending/        # Place new orders here
│   ├── processing/     # Orders being processed
│   ├── filled/         # Completed orders
│   └── failed/         # Failed orders
├── src/                # Source code
├── tests/              # Test suite
├── dashboard/          # Web dashboard
└── logs/               # Application logs
```

## Development

This project follows Test-Driven Development (TDD) practices. Always write tests first!

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run linting
uv run ruff check src/

# Run type checking
uv run mypy src/
```

## Documentation

- [PROJECT_DETAILS.md](PROJECT_DETAILS.md) - Complete project specifications
- [PROJECT_PLAN.md](PROJECT_PLAN.md) - Development roadmap and progress

## License

[Your License Here]