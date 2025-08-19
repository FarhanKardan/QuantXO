import pandas as pd
from pathlib import Path
from datetime import datetime
import re
import sys
sys.path.append(str(Path(__file__).parent.parent))
from models import TickData

class DataReader:
    def __init__(self, data_dir="data"):
        script_dir = Path(__file__).parent
        self.data_dir = script_dir.parent / data_dir
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def iterate_ticks(self, start_date, end_date, limit=None):
        """Iterate over ticks and yield TickData objects"""
        # Get files in date range
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        matching_files = []
        for file in self.data_dir.glob("*.csv"):
            if file.is_file():
                date_match = re.search(r'(\d{4}[-_]\d{2}[-_]\d{2})', file.name)
                if date_match:
                    file_date_str = date_match.group(1).replace('_', '-')
                    file_date = pd.to_datetime(file_date_str)
                    if start_dt <= file_date <= end_dt:
                        matching_files.append(file.name)
        
        if not matching_files:
            return
        
        # Get symbol from first filename
        symbol = matching_files[0].split('_')[0]
        
        count = 0
        for filename in sorted(matching_files):
            file_path = self.data_dir / filename
            df = pd.read_csv(file_path)
            
            # Convert timestamps and calculate size
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['size'] = df['price'] * df['volume']
            
            # Keep only essential columns
            df = df[['timestamp', 'price', 'side', 'size']]
            
            for _, row in df.iterrows():
                try:
                    # Standardize side to "Buy" or "Sell"
                    side = str(row['side']).strip().lower()
                    if side in ['buy', 'b', '1']:
                        standardized_side = 'Buy'
                    elif side in ['sell', 's', '0']:
                        standardized_side = 'Sell'
                    else:
                        standardized_side = 'Buy'  # Default to Buy if unknown
                    
                    tick_data = TickData(
                        symbol=symbol,
                        side=standardized_side,
                        size=float(row['size']),
                        price=float(row['price']),
                        timestamp=row['timestamp']
                    )
                    
                    yield tick_data
                    count += 1
                    
                    if limit and count >= limit:
                        return
                        
                except (ValueError, TypeError):
                    continue

def main():
    reader = DataReader()
    start_date = "2024-05-01"
    end_date = "2024-05-01"
    
    print("Testing iterate_ticks (first 5 ticks):")
    count = 0
    for tick in reader.iterate_ticks(start_date, end_date):
        print(f"Tick {count + 1}: {tick.symbol} {tick.side} {tick.price} {tick.size}")
        count += 1
        if count >= 5:
            break

if __name__ == "__main__":
    main()
