"""
Exercise 2: Apply Strategy Pattern for Missing Values Handling
Objective: Learn the Strategy Pattern - one interface, many interchangeable behaviors
"""

from abc import ABC, abstractmethod
import pandas as pd


class MissingValueStrategy(ABC):
    """
    Abstract base class for missing value handling strategies.
    This defines the interface that all strategies must implement.
    """
    
    @abstractmethod
    def handle(self, df):
        """
        Handle missing values in the dataframe.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with missing values handled
        """
        pass
    
    @abstractmethod
    def describe(self):
        """Return a description of the strategy."""
        pass


class DropMissing(MissingValueStrategy):
    """Strategy to drop rows with missing values."""
    
    def handle(self, df):
        """Drop all rows containing missing values."""
        original_shape = df.shape
        df_cleaned = df.dropna()
        print(f"  Dropped {original_shape[0] - df_cleaned.shape[0]} rows with missing values")
        return df_cleaned
    
    def describe(self):
        return "Drop all rows containing missing values"


class FillMean(MissingValueStrategy):
    """Strategy to fill missing values with column mean (for numeric columns)."""
    
    def handle(self, df):
        """Fill missing values with column mean for numeric columns."""
        df_cleaned = df.copy()
        numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
        
        for col in numeric_cols:
            if df_cleaned[col].isnull().any():
                mean_value = df_cleaned[col].mean()
                df_cleaned[col].fillna(mean_value, inplace=True)
                print(f"  Filled {col} with mean: {mean_value:.2f}")
        
        return df_cleaned
    
    def describe(self):
        return "Fill missing numeric values with column mean"


class FillMode(MissingValueStrategy):
    """Strategy to fill missing values with column mode (most frequent value)."""
    
    def handle(self, df):
        """Fill missing values with the most frequent value in each column."""
        df_cleaned = df.copy()
        
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().any():
                mode_value = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else None
                if mode_value is not None:
                    df_cleaned[col].fillna(mode_value, inplace=True)
                    print(f"  Filled {col} with mode: {mode_value}")
        
        return df_cleaned
    
    def describe(self):
        return "Fill missing values with most frequent value (mode)"


class FillMedian(MissingValueStrategy):
    """Strategy to fill missing values with column median (for numeric columns)."""
    
    def handle(self, df):
        """Fill missing values with column median for numeric columns."""
        df_cleaned = df.copy()
        numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
        
        for col in numeric_cols:
            if df_cleaned[col].isnull().any():
                median_value = df_cleaned[col].median()
                df_cleaned[col].fillna(median_value, inplace=True)
                print(f"  Filled {col} with median: {median_value:.2f}")
        
        return df_cleaned
    
    def describe(self):
        return "Fill missing numeric values with column median"


class DataCleaner:
    """
    Context class that uses a MissingValueStrategy to clean data.
    Demonstrates the Strategy Pattern in action.
    """
    
    def __init__(self, strategy: MissingValueStrategy):
        """
        Initialize with a specific missing value handling strategy.
        
        Args:
            strategy (MissingValueStrategy): The strategy to use
        """
        self.strategy = strategy
    
    def set_strategy(self, strategy: MissingValueStrategy):
        """
        Change the strategy at runtime.
        
        Args:
            strategy (MissingValueStrategy): New strategy to use
        """
        self.strategy = strategy
        print(f"✓ Strategy changed to: {strategy.describe()}")
    
    def clean(self, df):
        """
        Apply the current strategy to clean the dataframe.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print(f"\n🔧 Applying strategy: {self.strategy.describe()}")
        print(f"  Missing values before: {df.isnull().sum().sum()}")
        
        df_cleaned = self.strategy.handle(df)
        
        print(f"  Missing values after: {df_cleaned.isnull().sum().sum()}")
        print("✓ Cleaning complete")
        
        return df_cleaned


# Example usage
if __name__ == "__main__":
    # Create sample data with missing values
    data = {
        'Name': ['Alice', 'Bob', None, 'David', 'Eve'],
        'Age': [25, 30, 35, None, 28],
        'Salary': [50000, None, 60000, 55000, None],
        'Department': ['IT', 'HR', 'IT', None, 'Finance']
    }
    df = pd.DataFrame(data)
    
    print("Original Data:")
    print(df)
    print(f"\nMissing values:\n{df.isnull().sum()}")
    
    # Example 1: Using DropMissing strategy
    cleaner = DataCleaner(DropMissing())
    df_cleaned1 = cleaner.clean(df.copy())
    print("\nResult with DropMissing:")
    print(df_cleaned1)
    
    # Example 2: Switching to FillMean strategy
    print("\n" + "="*50)
    cleaner.set_strategy(FillMean())
    df_cleaned2 = cleaner.clean(df.copy())
    print("\nResult with FillMean:")
    print(df_cleaned2)
    
    # Example 3: Using FillMode strategy
    print("\n" + "="*50)
    cleaner.set_strategy(FillMode())
    df_cleaned3 = cleaner.clean(df.copy())
    print("\nResult with FillMode:")
    print(df_cleaned3)
