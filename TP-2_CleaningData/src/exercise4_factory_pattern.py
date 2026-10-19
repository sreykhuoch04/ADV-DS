"""
Exercise 4: Implement Factory Pattern for Data Transformations
Objective: Practice Factory Pattern for scalable creation of transformation objects
"""

from abc import ABC, abstractmethod
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class DataTransform(ABC):
    """
    Abstract base class for data transformations.
    All transformation classes must implement the apply() method.
    """
    
    @abstractmethod
    def apply(self, df):
        """
        Apply the transformation to the dataframe.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Transformed dataframe
        """
        pass
    
    @abstractmethod
    def describe(self):
        """Return a description of the transformation."""
        pass


class NormalizeColumns(DataTransform):
    """
    Normalize numeric columns to range [0, 1] using Min-Max scaling.
    """
    
    def __init__(self, columns=None):
        """
        Initialize normalizer.
        
        Args:
            columns (list): Specific columns to normalize. If None, normalize all numeric columns.
        """
        self.columns = columns
        self.scaler = MinMaxScaler()
    
    def apply(self, df):
        """Normalize specified columns."""
        df_transformed = df.copy()
        
        if self.columns is None:
            # Normalize all numeric columns
            numeric_cols = df_transformed.select_dtypes(include=['number']).columns.tolist()
        else:
            numeric_cols = self.columns
        
        if numeric_cols:
            df_transformed[numeric_cols] = self.scaler.fit_transform(df_transformed[numeric_cols])
            print(f"  ✓ Normalized columns: {numeric_cols}")
        
        return df_transformed
    
    def describe(self):
        return "Normalize numeric columns to [0, 1] range"


class StandardizeColumns(DataTransform):
    """
    Standardize numeric columns (mean=0, std=1) using Standard Scaling.
    """
    
    def __init__(self, columns=None):
        """
        Initialize standardizer.
        
        Args:
            columns (list): Specific columns to standardize. If None, standardize all numeric columns.
        """
        self.columns = columns
        self.scaler = StandardScaler()
    
    def apply(self, df):
        """Standardize specified columns."""
        df_transformed = df.copy()
        
        if self.columns is None:
            numeric_cols = df_transformed.select_dtypes(include=['number']).columns.tolist()
        else:
            numeric_cols = self.columns
        
        if numeric_cols:
            df_transformed[numeric_cols] = self.scaler.fit_transform(df_transformed[numeric_cols])
            print(f"  ✓ Standardized columns: {numeric_cols}")
        
        return df_transformed
    
    def describe(self):
        return "Standardize numeric columns (mean=0, std=1)"


class RemoveDuplicates(DataTransform):
    """
    Remove duplicate rows from the dataframe.
    """
    
    def __init__(self, subset=None, keep='first'):
        """
        Initialize duplicate remover.
        
        Args:
            subset (list): Columns to consider for identifying duplicates
            keep (str): Which duplicates to keep ('first', 'last', or False)
        """
        self.subset = subset
        self.keep = keep
    
    def apply(self, df):
        """Remove duplicate rows."""
        original_shape = df.shape
        df_transformed = df.drop_duplicates(subset=self.subset, keep=self.keep)
        
        removed = original_shape[0] - df_transformed.shape[0]
        print(f"  ✓ Removed {removed} duplicate rows")
        
        return df_transformed
    
    def describe(self):
        return "Remove duplicate rows"


class StandardizeText(DataTransform):
    """
    Standardize text columns (lowercase, strip whitespace).
    """
    
    def __init__(self, columns=None):
        """
        Initialize text standardizer.
        
        Args:
            columns (list): Specific columns to standardize. If None, standardize all text columns.
        """
        self.columns = columns
    
    def apply(self, df):
        """Standardize text in specified columns."""
        df_transformed = df.copy()
        
        if self.columns is None:
            # Standardize all object/string columns
            text_cols = df_transformed.select_dtypes(include=['object']).columns.tolist()
        else:
            text_cols = self.columns
        
        for col in text_cols:
            if col in df_transformed.columns:
                df_transformed[col] = df_transformed[col].astype(str).str.strip().str.lower()
        
        print(f"  ✓ Standardized text in columns: {text_cols}")
        
        return df_transformed
    
    def describe(self):
        return "Standardize text (lowercase, strip whitespace)"


class RemoveOutliers(DataTransform):
    """
    Remove outliers using IQR method.
    """
    
    def __init__(self, columns=None, threshold=1.5):
        """
        Initialize outlier remover.
        
        Args:
            columns (list): Columns to check for outliers
            threshold (float): IQR multiplier (default: 1.5)
        """
        self.columns = columns
        self.threshold = threshold
    
    def apply(self, df):
        """Remove outliers using IQR method."""
        df_transformed = df.copy()
        
        if self.columns is None:
            numeric_cols = df_transformed.select_dtypes(include=['number']).columns.tolist()
        else:
            numeric_cols = self.columns
        
        original_shape = df_transformed.shape
        
        for col in numeric_cols:
            Q1 = df_transformed[col].quantile(0.25)
            Q3 = df_transformed[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - self.threshold * IQR
            upper_bound = Q3 + self.threshold * IQR
            
            df_transformed = df_transformed[
                (df_transformed[col] >= lower_bound) & 
                (df_transformed[col] <= upper_bound)
            ]
        
        removed = original_shape[0] - df_transformed.shape[0]
        print(f"  ✓ Removed {removed} outlier rows")
        
        return df_transformed
    
    def describe(self):
        return f"Remove outliers using IQR method (threshold={self.threshold})"


class TransformFactory:
    """
    Factory class for creating data transformation objects.
    Demonstrates the Factory Pattern for object creation.
    """
    
    @staticmethod
    def create_transform(transform_type, **kwargs):
        """
        Create and return a transformation object based on type.
        
        Args:
            transform_type (str): Type of transformation
            **kwargs: Additional parameters for the transformation
            
        Returns:
            DataTransform: A transformation object
            
        Raises:
            ValueError: If transform_type is not recognized
        """
        transforms = {
            'normalize': NormalizeColumns,
            'standardize': StandardizeColumns,
            'remove_duplicates': RemoveDuplicates,
            'standardize_text': StandardizeText,
            'remove_outliers': RemoveOutliers
        }
        
        transform_class = transforms.get(transform_type.lower())
        
        if transform_class is None:
            available = ', '.join(transforms.keys())
            raise ValueError(f"Unknown transform type: '{transform_type}'. Available: {available}")
        
        return transform_class(**kwargs)
    
    @staticmethod
    def list_available_transforms():
        """List all available transformation types."""
        return [
            'normalize',
            'standardize',
            'remove_duplicates',
            'standardize_text',
            'remove_outliers'
        ]


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("Factory Pattern for Data Transformations")
    print("="*60)
    
    # Create sample data
    data = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'CHARLIE', '  David  ', 'Alice'],
        'Age': [25, 30, 35, 28, 25],
        'Salary': [50000, 60000, 70000, 55000, 50000],
        'Score': [85, 92, 78, 150, 88]  # 150 is an outlier
    })
    
    print("\nOriginal Data:")
    print(data)
    
    # Example 1: Using Factory to create transformations
    print("\n" + "="*60)
    print("Example 1: Remove Duplicates")
    print("="*60)
    
    factory = TransformFactory()
    transform1 = factory.create_transform('remove_duplicates')
    print(f"Transform: {transform1.describe()}")
    df1 = transform1.apply(data.copy())
    print("\nResult:")
    print(df1)
    
    # Example 2: Standardize text
    print("\n" + "="*60)
    print("Example 2: Standardize Text")
    print("="*60)
    
    transform2 = factory.create_transform('standardize_text', columns=['Name'])
    print(f"Transform: {transform2.describe()}")
    df2 = transform2.apply(data.copy())
    print("\nResult:")
    print(df2[['Name']])
    
    # Example 3: Normalize columns
    print("\n" + "="*60)
    print("Example 3: Normalize Numeric Columns")
    print("="*60)
    
    transform3 = factory.create_transform('normalize', columns=['Age', 'Salary'])
    print(f"Transform: {transform3.describe()}")
    df3 = transform3.apply(data.copy())
    print("\nResult:")
    print(df3)
    
    # Example 4: Remove outliers
    print("\n" + "="*60)
    print("Example 4: Remove Outliers")
    print("="*60)
    
    transform4 = factory.create_transform('remove_outliers', columns=['Score'])
    print(f"Transform: {transform4.describe()}")
    df4 = transform4.apply(data.copy())
    print("\nResult:")
    print(df4)
    
    # Example 5: List available transforms
    print("\n" + "="*60)
    print("Available Transformations:")
    print("="*60)
    for transform in factory.list_available_transforms():
        print(f"  • {transform}")
