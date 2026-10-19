"""
Exercise 5: Build a Full Cleaning Pipeline (Template Method Pattern)
Objective: Combine all concepts into one cleaning pipeline using Template Method Pattern
"""

from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime
from pathlib import Path
from exercise1_csv_reader import CSVReader
from exercise2_strategy_pattern import DataCleaner, FillMean
from exercise3_decorators import log_action, log_time
from exercise4_factory_pattern import TransformFactory


class DataPipeline(ABC):
    """
    Abstract base class defining the template for a data cleaning pipeline.
    The Template Method Pattern defines the skeleton of the algorithm,
    allowing subclasses to override specific steps.
    """
    
    def __init__(self):
        """Initialize the pipeline."""
        self.data = None
        self.cleaned_data = None
        self.transformed_data = None
    
    @log_action
    @log_time
    def run(self):
        """
        Template method that defines the pipeline workflow.
        This is the "template" - the sequence of steps is fixed,
        but each step can be customized by subclasses.
        """
        print("\n" + "="*70)
        print("🚀 STARTING DATA CLEANING PIPELINE")
        print("="*70)
        
        # Step 1: Load data
        self.load()
        
        if self.data is None:
            print("❌ Pipeline failed: No data loaded")
            return None
        
        # Step 2: Clean data
        self.clean()
        
        # Step 3: Transform data
        self.transform()
        
        # Step 4: Validate data
        self.validate()
        
        # Step 5: Save data
        self.save()
        
        print("\n" + "="*70)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        print("="*70)
        
        return self.transformed_data
    
    @abstractmethod
    def load(self):
        """Load data from source. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def clean(self):
        """Clean the data. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def transform(self):
        """Transform the data. Must be implemented by subclasses."""
        pass
    
    def validate(self):
        """
        Validate the data quality.
        Default implementation - can be overridden.
        """
        print("\n📋 Step 4: Validating Data")
        print("-" * 70)
        
        if self.transformed_data is None:
            print("⚠️  No data to validate")
            return
        
        print(f"  ✓ Shape: {self.transformed_data.shape}")
        print(f"  ✓ Missing values: {self.transformed_data.isnull().sum().sum()}")
        print(f"  ✓ Duplicates: {self.transformed_data.duplicated().sum()}")
        print("  ✓ Validation complete")
    
    @abstractmethod
    def save(self):
        """Save the processed data. Must be implemented by subclasses."""
        pass


class CSVDataPipeline(DataPipeline):
    """
    Concrete implementation of DataPipeline for CSV files.
    Demonstrates how the Template Method Pattern allows customization
    while maintaining the overall structure.
    """
    
    def __init__(self, input_file, output_file, missing_strategy=None, transformations=None):
        """
        Initialize the CSV data pipeline.
        
        Args:
            input_file (str): Path to input CSV file
            output_file (str): Path to save cleaned data
            missing_strategy: Strategy for handling missing values
            transformations (list): List of transformation specifications
        """
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.missing_strategy = missing_strategy or FillMean()
        self.transformations = transformations or []
        self.reader = None
    
    def load(self):
        """Load data from CSV file."""
        print("\n📂 Step 1: Loading Data")
        print("-" * 70)
        
        self.reader = CSVReader(self.input_file)
        self.data = self.reader.read()
        
        if self.data is not None:
            print(f"  ✓ Loaded {self.data.shape[0]} rows and {self.data.shape[1]} columns")
    
    def clean(self):
        """Clean the data using the specified strategy."""
        print("\n🧹 Step 2: Cleaning Data")
        print("-" * 70)
        
        if self.data is None:
            print("  ⚠️  No data to clean")
            return
        
        cleaner = DataCleaner(self.missing_strategy)
        self.cleaned_data = cleaner.clean(self.data)
        print(f"  ✓ Cleaned data shape: {self.cleaned_data.shape}")
    
    def transform(self):
        """Apply transformations using the Factory pattern."""
        print("\n🔄 Step 3: Transforming Data")
        print("-" * 70)
        
        if self.cleaned_data is None:
            print("  ⚠️  No data to transform")
            return
        
        self.transformed_data = self.cleaned_data.copy()
        
        if not self.transformations:
            print("  ℹ️  No transformations specified")
            return
        
        factory = TransformFactory()
        
        for i, transform_spec in enumerate(self.transformations, 1):
            print(f"\n  Transformation {i}:")
            
            transform_type = transform_spec.get('type')
            params = {k: v for k, v in transform_spec.items() if k != 'type'}
            
            try:
                transform = factory.create_transform(transform_type, **params)
                print(f"  → {transform.describe()}")
                self.transformed_data = transform.apply(self.transformed_data)
            except ValueError as e:
                print(f"  ❌ Error: {e}")
    
    def save(self):
        """Save the processed data to CSV."""
        print("\n💾 Step 5: Saving Data")
        print("-" * 70)
        
        if self.transformed_data is None:
            print("  ⚠️  No data to save")
            return
        
        try:
            self.transformed_data.to_csv(self.output_file, index=False)
            print(f"  ✓ Data saved to: {self.output_file}")
            print(f"  ✓ Saved {self.transformed_data.shape[0]} rows and {self.transformed_data.shape[1]} columns")
        except Exception as e:
            print(f"  ❌ Error saving file: {e}")


class AdvancedCSVPipeline(CSVDataPipeline):
    """
    Extended pipeline with additional features.
    Demonstrates how easy it is to extend the template.
    """
    
    def validate(self):
        """Enhanced validation with detailed statistics."""
        print("\n📋 Step 4: Advanced Validation")
        print("-" * 70)
        
        super().validate()  # Call parent validation
        
        if self.transformed_data is not None:
            print("\n  Detailed Statistics:")
            print(f"  • Numeric columns: {len(self.transformed_data.select_dtypes(include=['number']).columns)}")
            print(f"  • Text columns: {len(self.transformed_data.select_dtypes(include=['object']).columns)}")
            print(f"  • Memory usage: {self.transformed_data.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    def generate_report(self):
        """Generate a cleaning report."""
        print("\n" + "="*70)
        print("📊 PIPELINE REPORT")
        print("="*70)
        
        report = {
            'Input File': self.input_file,
            'Output File': self.output_file,
            'Original Shape': self.data.shape if self.data is not None else 'N/A',
            'Final Shape': self.transformed_data.shape if self.transformed_data is not None else 'N/A',
            'Rows Removed': (self.data.shape[0] - self.transformed_data.shape[0]) if self.data is not None and self.transformed_data is not None else 'N/A',
            'Missing Strategy': self.missing_strategy.describe() if hasattr(self.missing_strategy, 'describe') else 'N/A',
            'Transformations Applied': len(self.transformations),
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for key, value in report.items():
            print(f"  {key}: {value}")
        
        return report


# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'CHARLIE', '  David  ', 'Eve', 'Alice'],
        'Age': [25, None, 35, 28, 32, 25],
        'Salary': [50000, 60000, None, 55000, 65000, 50000],
        'Department': ['IT', 'HR', 'it', 'Finance', None, 'IT'],
        'Score': [85, 92, 78, 88, 95, 85]
    })
    
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    input_file = data_dir / "pipeline_input.csv"
    output_file = data_dir / "pipeline_output.csv"
    
    sample_data.to_csv(input_file, index=False)
    
    print("Sample data created for pipeline demonstration")
    print(sample_data)
    
    # Define pipeline configuration
    from exercise2_strategy_pattern import FillMean
    
    transformations = [
        {'type': 'remove_duplicates'},
        {'type': 'standardize_text', 'columns': ['Name', 'Department']},
        {'type': 'normalize', 'columns': ['Age', 'Salary', 'Score']}
    ]
    
    # Run basic pipeline
    print("\n\n" + "="*70)
    print("RUNNING BASIC CSV PIPELINE")
    print("="*70)
    
    pipeline = CSVDataPipeline(
        input_file=input_file,
        output_file=output_file,
        missing_strategy=FillMean(),
        transformations=transformations
    )
    
    result = pipeline.run()
    
    # Run advanced pipeline
    print("\n\n" + "="*70)
    print("RUNNING ADVANCED CSV PIPELINE")
    print("="*70)
    
    advanced_pipeline = AdvancedCSVPipeline(
        input_file=input_file,
        output_file=data_dir / "pipeline_output_advanced.csv",
        missing_strategy=FillMean(),
        transformations=transformations
    )
    
    result = advanced_pipeline.run()
    advanced_pipeline.generate_report()
    
    print("\n\nFinal cleaned data:")
    print(result)
