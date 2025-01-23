# Redis TUI

A terminal user interface for browsing and managing Redis data.

## Features

- Tree-based navigation of Redis keys
- Support for all Redis data types (strings, lists, sets, hashes, sorted sets)
- Pattern-based filtering
- Data type filtering
- TTL display and management
- Basic Redis operations (view, edit, delete)
- Search functionality
- Configurable Redis connection

## Prerequisites

### Redis Installation

#### macOS
Using Homebrew:
```bash
brew install redis
brew services start redis
```

#### Other Platforms
- Linux: [Redis Installation Guide for Linux](https://redis.io/docs/getting-started/installation/install-redis-on-linux/)
- Windows: [Redis Installation Guide for Windows](https://redis.io/docs/getting-started/installation/install-redis-on-windows/)
- Docker: `docker run --name redis -p 6379:6379 -d redis`

### Verify Redis Installation
```bash
redis-cli ping
```
If you see `PONG` as the response, Redis is running correctly!

## Installation

### Option 1: Install from source (recommended for development)
1. Clone the repository:
```bash
git clone https://github.com/gregk/redis_tui.git
cd redis_tui
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install in development mode:
```bash
pip install -e .
```

### Option 2: Install using pip (coming soon)
```bash
pip install redis-tui
```

## Usage

There are two ways to run Redis TUI:

1. Using the installed command:
```bash
redis-tui
```

2. Running the module directly:
```bash
python -m src.app
```

### Connection Options

Connect to a specific Redis instance:
```bash
redis-tui --host localhost --port 6379 --db 0
```

Or when running as a module:
```bash
python -m src.app --host localhost --port 6379 --db 0
```

Load sample data for testing/demo purposes:
```bash
redis-tui --samples
```

## Key Bindings

- `↑`/`↓`: Navigate keys
- `←`/`→`: Collapse/expand tree nodes
- `Enter`: Select key
- `f`: Toggle between key tree and data view
- `d`: Toggle raw data view
- `q`: Quit
- `r`: Refresh data

## Configuration

Redis connection details can be provided via:
1. Command line arguments
2. Environment variables:
   ```bash
   export REDIS_HOST=localhost
   export REDIS_PORT=6379
   export REDIS_DB=0
   ```
3. Configuration file:
   ```yaml
   # ~/.config/redis-tui/config.yaml
   redis:
     host: localhost
     port: 6379
     db: 0
   ```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/redis-tui.git
cd redis-tui
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Contributing

Contributions are welcome! Please see our contributing guidelines for more details.

## License

MIT License 