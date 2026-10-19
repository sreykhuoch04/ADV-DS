"""
Unit tests for Exercise 1: CSVReader class
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from exercise1_csv_reader import CSVReader


class TestCSVReader(unittest.TestCase):
    """Test cases for CSVReader class"""
    
    @classmethod
    def setUpClass(cls):
        """Create test data file"""
        cls.test_file = 'test_data.csv'
        test_data = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'Salary': [50000, 60000, 70000]
        })
        test_data.to_csv(cls.test_file, index=False)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test file"""
        import os
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
    
    def test_initialization(self):
        """Test CSVReader initialization"""
        reader = CSVReader(self.test_file)
        self.assertEqual(reader.file_path, self.test_file)
        self.assertIsNone(reader.data)
    
    def test_read_success(self):
        """Test successful CSV reading"""
        reader = CSVReader(self.test_file)
        df = reader.read()
        
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (3, 3))
        self.assertListEqual(list(df.columns), ['Name', 'Age', 'Salary'])
    
    def test_read_nonexistent_file(self):
        """Test reading nonexistent file"""
        reader = CSVReader('nonexistent.csv')
        df = reader.read()
        
        self.assertIsNone(df)
    
    def test_preview(self):
        """Test preview method"""
        reader = CSVReader(self.test_file)
        reader.read()
        
        # Should not raise any errors
        reader.preview(2)
        reader.preview(5)  # More than available rows
    
    def test_info(self):
        """Test info method"""
        reader = CSVReader(self.test_file)
        reader.read()
        
        # Should not raise any errors
        reader.info()


if __name__ == '__main__':
    unittest.main()
