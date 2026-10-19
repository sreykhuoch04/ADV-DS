"""
Exercise 1: Build the CSVReader Class (OOP Foundation)
Objective: Reinforce OOP fundamentals - classes, constructors, methods, encapsulation
"""

import pandas as pd
from pathlib import Path


class CSVReader:
    """
    A class to encapsulate CSV file reading functionality.
    Demonstrates OOP principles: encapsulation, methods, and state management.
    """
    
    def __init__(self, file_path):
        """
        Initialize the CSVReader with a file path.
        
        Args:
            file_path (str): Path to the CSV file
        """
        self.file_path = file_path
        self.data = None
    
    def read(self):
        """
        Load the CSV file using pandas.
        
        Returns:
            pd.DataFrame: The loaded dataframe
        """
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"✓ Successfully loaded {self.file_path}")
            print(f"  Shape: {self.data.shape}")
            return self.data
        except FileNotFoundError:
            print(f"✗ Error: File '{self.file_path}' not found.")
            return None
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return None
    
    def preview(self, n=5):
        """
        Display the first n rows of the dataset.
        
        Args:
            n (int): Number of rows to display (default: 5)
        """
        if self.data is None:
            print("✗ No data loaded. Call read() first.")
            return
        
        print(f"\n--- Preview (top {n} rows) ---")
        print(self.data.head(n))
        print(f"\nColumns: {list(self.data.columns)}")
        print(f"Data types:\n{self.data.dtypes}")
    
    def info(self):
        """Display information about the dataset."""
        if self.data is None:
            print("✗ No data loaded. Call read() first.")
            return
        
        print("\n--- Dataset Information ---")
        self.data.info()
        print(f"\nMissing values:\n{self.data.isnull().sum()}")


# Example usage
if __name__ == "__main__":
    # Create an instance of CSVReader
    sample_file = Path(__file__).resolve().parent.parent / "data" / "sample_data.csv"
    reader = CSVReader(sample_file)
    
    # Read the CSV file
    df = reader.read()
    
    # Preview the data
    if df is not None:
        reader.preview(10)
        reader.info()
