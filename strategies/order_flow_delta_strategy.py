import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from data_feeder.historical_data_reader import DataReader
from profiling.conditions.volume import VolumeCondition
from profiling.conditions.delta import DeltaCondition
from profiling.utils.types import Trade
import warnings
warnings.filterwarnings('ignore')

class OrderFlowDeltaStrategy:
    """
    Order Flow and Delta-Based Trading Strategy
    
    Strategy Logic:
    - Uses volume profile analysis to identify high-activity price levels
    - Monitors delta (buy/sell imbalance) for momentum signals
    - Enters positions when strong order flow confirms price direction
    - Exits based on delta reversal or volume exhaustion
    """
    
    def __init__(self, initial_capital=10000, volume_threshold=500000, delta_threshold=200000):
        self.initial_capital = initial_capital
        self.volume_threshold = volume_threshold
        self.delta_threshold = delta_threshold
        self.data_reader = DataReader()
        
        # Initialize profilers
        self.volume_profiler = VolumeCondition(
            tick_size=100,
            value_area_pct=0.7,
            volume_threshold=volume_threshold,
            csv_file_path="order_flow_strategy_volume.csv"
        )
        
        self.delta_profiler = DeltaCondition(
            tick_size=100,
            value_area_pct=0.7,
            delta_threshold=delta_threshold
        )
        
    def prepare_data(self, start_date, end_date):
        """Prepare tick data with order flow analysis"""
        print("📊 Preparing order flow data from historical ticks...")
        
        # Collect all ticks
        ticks = []
        for tick in self.data_reader.iterate_ticks(start_date, end_date):
            ticks.append({
                'timestamp': tick.timestamp,
                'price': tick.price,
                'size': tick.size,
                'side': tick.side
            })
        
        if not ticks:
            print("❌ No tick data found")
            return None
            
        # Convert to DataFrame
        df = pd.DataFrame(ticks)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Calculate cumulative delta (buy volume - sell volume)
        df['delta'] = 0
        df.loc[df['side'] == 'Buy', 'delta'] = df['size']
        df.loc[df['side'] == 'Sell', 'delta'] = -df['size']
        df['cumulative_delta'] = df['delta'].cumsum()
        
        # Calculate rolling metrics
        df['rolling_volume'] = df['size'].rolling(window=100).sum()
        df['rolling_delta'] = df['delta'].rolling(window=100).sum()
        df['price_change'] = df['price'].pct_change()
        
        # Remove NaN values
        df = df.dropna()
        
        print(f"✅ Prepared {len(df)} ticks with order flow metrics")
        return df
    
    def analyze_order_flow(self, data):
        """Analyze order flow patterns and generate signals"""
        print("🔍 Analyzing order flow patterns...")
        
        # Initialize signal columns
        data['signal'] = 0
        data['position'] = 0
        data['strength'] = 0
        
        # Calculate signal strength based on multiple factors
        for i in range(100, len(data)):
            current_row = data.iloc[i]
            lookback = data.iloc[i-100:i]
            
            # Factor 1: Volume surge
            volume_surge = current_row['rolling_volume'] > lookback['rolling_volume'].mean() * 1.5
            
            # Factor 2: Delta momentum
            delta_momentum = abs(current_row['rolling_delta']) > self.delta_threshold
            
            # Factor 3: Price momentum
            price_momentum = abs(current_row['price_change']) > 0.001
            
            # Factor 4: Delta direction consistency
            recent_delta = lookback['rolling_delta'].iloc[-20:]
            delta_consistency = (recent_delta > 0).all() or (recent_delta < 0).all()
            
            # Calculate composite strength
            strength = 0
            if volume_surge: strength += 1
            if delta_momentum: strength += 2
            if price_momentum: strength += 1
            if delta_consistency: strength += 1
            
            data.iloc[i, data.columns.get_loc('strength')] = strength
            
            # Generate signals based on strength
            if strength >= 3:  # Strong signal
                if current_row['rolling_delta'] > 0:  # Strong buying pressure
                    data.iloc[i, data.columns.get_loc('signal')] = 1
                elif current_row['rolling_delta'] < 0:  # Strong selling pressure
                    data.iloc[i, data.columns.get_loc('signal')] = -1
        
        # Position changes only when signal changes
        data['position'] = data['signal'].diff()
        
        # Remove first rows (no position change)
        data = data.dropna()
        
        print(f"✅ Generated {len(data[data['position'] != 0])} position changes")
        return data
    
    def backtest(self, data):
        """Run backtest with order flow strategy"""
        print("📈 Running order flow backtest...")
        
        # Initialize backtest variables
        capital = self.initial_capital
        position = 0
        trades = []
        equity_curve = []
        
        for i, (timestamp, row) in enumerate(data.iterrows()):
            current_price = row['price']
            current_strength = row['strength']
            
            # Execute trades based on position changes
            if row['position'] == 1:  # Buy signal
                if position == 0:  # Not currently holding
                    position = capital / current_price
                    entry_price = current_price
                    entry_time = timestamp
                    entry_strength = current_strength
                    print(f"🟢 BUY: {timestamp} @ ${current_price:.2f} | Strength: {current_strength}")
                    
            elif row['position'] == -1:  # Sell signal
                if position > 0:  # Currently holding
                    exit_price = current_price
                    exit_time = timestamp
                    exit_strength = current_strength
                    pnl = (exit_price - entry_price) * position
                    capital += pnl
                    
                    trades.append({
                        'entry_time': entry_time,
                        'exit_time': exit_time,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'entry_strength': entry_strength,
                        'exit_strength': exit_strength,
                        'position': position,
                        'pnl': pnl,
                        'return': (exit_price - entry_price) / entry_price,
                        'hold_time': (exit_time - entry_time).total_seconds() / 60  # minutes
                    })
                    
                    print(f"🔴 SELL: {timestamp} @ ${current_price:.2f} | PnL: ${pnl:.2f} | Strength: {current_strength}")
                    position = 0
            
            # Calculate current equity
            current_equity = capital + (position * current_price)
            equity_curve.append({
                'timestamp': timestamp,
                'equity': current_equity,
                'price': current_price,
                'position': position,
                'strength': current_strength,
                'delta': row['rolling_delta'],
                'volume': row['rolling_volume']
            })
        
        # Close any remaining position
        if position > 0:
            final_price = data.iloc[-1]['price']
            pnl = (final_price - entry_price) * position
            capital += pnl
            print(f"🔴 CLOSE: Final @ ${final_price:.2f} | PnL: ${pnl:.2f}")
        
        # Convert to DataFrames
        trades_df = pd.DataFrame(trades)
        equity_df = pd.DataFrame(equity_curve)
        equity_df.set_index('timestamp', inplace=True)
        
        print(f"✅ Backtest completed with {len(trades_df)} trades")
        return trades_df, equity_df, capital
    
    def calculate_metrics(self, trades_df, equity_df, final_capital):
        """Calculate comprehensive performance metrics"""
        print("📊 Calculating performance metrics...")
        
        if len(trades_df) == 0:
            print("❌ No trades executed")
            return {}
        
        # Basic metrics
        total_return = (final_capital - self.initial_capital) / self.initial_capital
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        
        # Win rate
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # Average returns
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        # Risk metrics
        max_drawdown = self.calculate_max_drawdown(equity_df)
        sharpe_ratio = self.calculate_sharpe_ratio(equity_df)
        
        # Order flow specific metrics
        avg_hold_time = trades_df['hold_time'].mean() if 'hold_time' in trades_df.columns else 0
        avg_entry_strength = trades_df['entry_strength'].mean() if 'entry_strength' in trades_df.columns else 0
        avg_exit_strength = trades_df['exit_strength'].mean() if 'exit_strength' in trades_df.columns else 0
        
        metrics = {
            'Total Return (%)': total_return * 100,
            'Total Trades': total_trades,
            'Win Rate (%)': win_rate * 100,
            'Average Win': avg_win,
            'Average Loss': avg_loss,
            'Profit Factor': abs(avg_win / avg_loss) if avg_loss != 0 else float('inf'),
            'Max Drawdown (%)': max_drawdown * 100,
            'Sharpe Ratio': sharpe_ratio,
            'Average Hold Time (min)': avg_hold_time,
            'Average Entry Strength': avg_entry_strength,
            'Average Exit Strength': avg_exit_strength,
            'Final Capital': final_capital,
            'Initial Capital': self.initial_capital
        }
        
        print("✅ Performance metrics calculated")
        return metrics
    
    def calculate_max_drawdown(self, equity_df):
        """Calculate maximum drawdown"""
        peak = equity_df['equity'].expanding().max()
        drawdown = (equity_df['equity'] - peak) / peak
        return abs(drawdown.min())
    
    def calculate_sharpe_ratio(self, equity_df, risk_free_rate=0.02):
        """Calculate Sharpe ratio"""
        returns = equity_df['equity'].pct_change().dropna()
        if len(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        return np.sqrt(252) * excess_returns.mean() / returns.std() if returns.std() != 0 else 0
    
    def plot_results(self, data, trades_df, equity_df, metrics):
        """Create comprehensive plots of the order flow strategy results"""
        print("📊 Creating visualization plots...")
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(4, 1, figsize=(15, 16))
        fig.suptitle('Order Flow Delta Strategy - Backtest Results', fontsize=16, fontweight='bold')
        
        # Plot 1: Price and Signals
        axes[0].plot(data.index, data['price'], label='Price', alpha=0.7, linewidth=1)
        
        # Plot buy/sell signals
        buy_signals = data[data['position'] == 1]
        sell_signals = data[data['position'] == -1]
        
        axes[0].scatter(buy_signals.index, buy_signals['price'], 
                        color='green', marker='^', s=100, label='Buy Signal', alpha=0.8)
        axes[0].scatter(sell_signals.index, sell_signals['price'], 
                        color='red', marker='v', s=100, label='Sell Signal', alpha=0.8)
        
        axes[0].set_title('Price Action and Trading Signals')
        axes[0].set_ylabel('Price ($)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Cumulative Delta
        axes[1].plot(data.index, data['cumulative_delta'], label='Cumulative Delta', linewidth=2, color='purple')
        axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.5)
        axes[1].set_title('Cumulative Delta (Buy vs Sell Pressure)')
        axes[1].set_ylabel('Delta')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Equity Curve
        axes[2].plot(equity_df.index, equity_df['equity'], label='Portfolio Value', linewidth=2, color='blue')
        axes[2].axhline(y=self.initial_capital, color='red', linestyle='--', alpha=0.7, label='Initial Capital')
        axes[2].set_title('Portfolio Equity Curve')
        axes[2].set_ylabel('Portfolio Value ($)')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        # Plot 4: Signal Strength and Volume
        axes[3].plot(data.index, data['strength'], label='Signal Strength', linewidth=2, color='orange')
        axes[3].set_title('Signal Strength (0-5 Scale)')
        axes[3].set_xlabel('Time')
        axes[3].set_ylabel('Strength')
        axes[3].legend()
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('order_flow_strategy_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Plots saved as 'order_flow_strategy_results.png'")
    
    def run_strategy(self, start_date, end_date):
        """Run the complete order flow strategy"""
        print("🚀 Starting Order Flow Delta Strategy...")
        print("=" * 60)
        
        # Step 1: Prepare data
        data = self.prepare_data(start_date, end_date)
        if data is None:
            return None
        
        # Step 2: Analyze order flow
        data = self.analyze_order_flow(data)
        
        # Step 3: Run backtest
        trades_df, equity_df, final_capital = self.backtest(data)
        
        # Step 4: Calculate metrics
        metrics = self.calculate_metrics(trades_df, equity_df, final_capital)
        
        # Step 5: Display results
        print("\n📊 Strategy Results:")
        print("=" * 60)
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        
        # Step 6: Create plots
        self.plot_results(data, trades_df, equity_df, metrics)
        
        return {
            'data': data,
            'trades': trades_df,
            'equity': equity_df,
            'metrics': metrics
        }

def main():
    """Test the order flow strategy"""
    # Initialize strategy
    strategy = OrderFlowDeltaStrategy(
        initial_capital=10000,
        volume_threshold=500000,
        delta_threshold=200000
    )
    
    # Run strategy on historical data
    results = strategy.run_strategy("2024-05-01", "2024-05-02")
    
    if results:
        print("\n🎯 Order Flow Strategy execution completed successfully!")
    else:
        print("\n❌ Order Flow Strategy execution failed!")

if __name__ == "__main__":
    main()

