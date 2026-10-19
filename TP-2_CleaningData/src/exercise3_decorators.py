"""
Exercise 3: Add Decorators for Logging and Timing
Objective: Learn the Decorator Pattern to add reusable functionality
"""

import time
import functools
from datetime import datetime
from pathlib import Path


def log_action(func):
    """
    Decorator to log when a method starts and finishes.
    Demonstrates how decorators can add logging without modifying original code.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] 🚀 Starting: {func.__name__}")
        
        result = func(*args, **kwargs)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✓ Finished: {func.__name__}")
        
        return result
    return wrapper


def log_time(func):
    """
    Decorator to measure and log execution time.
    Demonstrates performance monitoring through decoration.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"⏱️  Execution time for {func.__name__}: {elapsed:.4f} seconds")
        
        return result
    return wrapper


def validate_data(func):
    """
    Decorator to validate that data exists before processing.
    Demonstrates defensive programming through decoration.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.data is None or self.data.empty:
            print(f"⚠️  Warning: No data loaded for {func.__name__}")
            return None
        return func(self, *args, **kwargs)
    return wrapper


# Apply decorators to our previous classes
import pandas as pd
from exercise1_csv_reader import CSVReader
from exercise2_strategy_pattern import DataCleaner, MissingValueStrategy


class DecoratedCSVReader(CSVReader):
    """
    Enhanced CSVReader with decorators for logging and timing.
    Demonstrates how decorators extend functionality without modifying base logic.
    """
    
    @log_action
    @log_time
    def read(self):
        """Read CSV with logging and timing."""
        return super().read()
    
    @log_action
    @validate_data
    def preview(self, n=5):
        """Preview data with logging and validation."""
        return super().preview(n)
    
    @log_action
    @validate_data
    def info(self):
        """Show info with logging and validation."""
        return super().info()


class DecoratedDataCleaner(DataCleaner):
    """
    Enhanced DataCleaner with decorators for logging and timing.
    """
    
    @log_action
    @log_time
    def clean(self, df):
        """Clean data with logging and timing."""
        return super().clean(df)


def performance_report(func):
    """
    Advanced decorator that provides detailed performance metrics.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import tracemalloc
        
        # Start tracking memory
        tracemalloc.start()
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        # Get performance metrics
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\n📊 Performance Report for {func.__name__}:")
        print(f"   ⏱️  Time: {end_time - start_time:.4f} seconds")
        print(f"   💾 Memory: Current={current / 1024:.2f} KB, Peak={peak / 1024:.2f} KB")
        
        return result
    return wrapper


class AdvancedDecoratedCSVReader(CSVReader):
    """
    CSV Reader with advanced performance monitoring.
    """
    
    @performance_report
    def read(self):
        """Read CSV with performance monitoring."""
        return super().read()
    
    @performance_report
    def preview(self, n=5):
        """Preview with performance monitoring."""
        return super().preview(n)


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("Example 1: Decorated CSV Reader")
    print("="*60)
    
    # Create sample CSV for testing
    sample_data = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 28, 32],
        'Salary': [50000, 60000, 70000, 55000, 65000]
    })
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    sample_file = data_dir / "test_sample.csv"
    sample_data.to_csv(sample_file, index=False)
    
    # Use decorated reader
    reader = DecoratedCSVReader(sample_file)
    reader.read()
    reader.preview(3)
    
    print("\n" + "="*60)
    print("Example 2: Decorated Data Cleaner")
    print("="*60)
    
    # Create data with missing values
    from exercise2_strategy_pattern import FillMean
    
    data_with_nulls = pd.DataFrame({
        'Name': ['Alice', 'Bob', None, 'David'],
        'Age': [25, None, 35, 28],
        'Salary': [50000, 60000, None, 55000]
    })
    
    print("Original data:")
    print(data_with_nulls)
    
    cleaner = DecoratedDataCleaner(FillMean())
    cleaned_data = cleaner.clean(data_with_nulls)
    
    print("\n" + "="*60)
    print("Example 3: Advanced Performance Monitoring")
    print("="*60)
    
    advanced_reader = AdvancedDecoratedCSVReader(sample_file)
    advanced_reader.read()
    advanced_reader.preview(3)
