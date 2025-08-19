# QuantXO

A quantitative trading analysis platform focused on volume profile analysis and order flow delta strategies for cryptocurrency markets.

## Overview

QuantXO is designed to analyze market microstructure through volume profiling, tick data analysis, and order flow delta calculations. It provides tools for backtesting trading strategies and understanding market behavior at the tick level.

## Features

- **Volume Profile Analysis**: Calculate Point of Control (POC) and Value Areas
- **Order Flow Delta**: Analyze buying vs selling pressure
- **Tick Data Processing**: Handle high-frequency market data
- **Historical Data Analysis**: Process CSV-based historical data
- **InfluxDB Integration**: Store and retrieve time-series data
- **Real-time WebSocket**: Connect to BitMEX for live data feeds

## Project Structure

```
QuantXO/
├── config_reader/          # Configuration management
├── data_feeder/           # Data ingestion (WebSocket, CSV)
├── influxDb/              # Database operations
├── log_handler/           # Logging utilities
├── models/                # Data models and structures
├── profiling/             # Core analysis engine
│   ├── calculation/       # POC and Value Area calculations
│   ├── clusters/          # Data clustering and aggregation
│   ├── conditions/        # Trading condition checks
│   └── utils/            # Utility functions
├── strategies/            # Trading strategy implementations
└── main.py               # Main application entry point
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd QuantXO
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` file in the root directory with your configuration:

```yaml
# Example configuration
database:
  url: "http://localhost:8086"
  token: "your-influxdb-token"
  org: "your-org"
  bucket: "market_data"

websocket:
  url: "wss://ws.bitmex.com/realtime"
```

## Usage

### Basic Volume Profile Analysis

```python
from profiling.conditions.volume import VolumeCondition
from data_feeder.historical_data_reader import DataReader

# Initialize components
data_reader = DataReader()
profiler = VolumeCondition(
    value_area_pct=0.7,
    tick_size=100,
    volume_threshold=500000,
    csv_file_path="volume_profile.csv"
)

# Process historical data
for tick_data in data_reader.iterate_ticks("2024-05-01", "2024-05-01"):
    # Your analysis logic here
    pass
```

### Running the Main Application

```bash
python main.py
```

## Data Format

The system expects CSV files with the following columns:
- `timestamp`: ISO format datetime
- `price`: Trade price
- `size`: Trade size
- `side`: Trade side (buy/sell)

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib/seaborn**: Data visualization
- **websockets**: Real-time data streaming
- **influxdb-client**: Time-series database operations
- **PyYAML**: Configuration file parsing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Contact

[Add your contact information here]