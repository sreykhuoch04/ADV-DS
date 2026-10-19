"""
TP-2: CleaningData - OOP and Design Patterns
A comprehensive data cleaning library demonstrating design patterns
"""

__version__ = "1.0.0"
__author__ = "ADV-DS"

from .exercise1_csv_reader import CSVReader
from .exercise2_strategy_pattern import (
    MissingValueStrategy,
    DropMissing,
    FillMean,
    FillMode,
    FillMedian,
    DataCleaner
)
from .exercise3_decorators import (
    log_action,
    log_time,
    validate_data,
    performance_report,
    DecoratedCSVReader,
    DecoratedDataCleaner
)
from .exercise4_factory_pattern import (
    DataTransform,
    NormalizeColumns,
    StandardizeColumns,
    RemoveDuplicates,
    StandardizeText,
    RemoveOutliers,
    TransformFactory
)
from .exercise5_template_pattern import (
    DataPipeline,
    CSVDataPipeline,
    AdvancedCSVPipeline
)

__all__ = [
    # Exercise 1
    'CSVReader',
    
    # Exercise 2
    'MissingValueStrategy',
    'DropMissing',
    'FillMean',
    'FillMode',
    'FillMedian',
    'DataCleaner',
    
    # Exercise 3
    'log_action',
    'log_time',
    'validate_data',
    'performance_report',
    'DecoratedCSVReader',
    'DecoratedDataCleaner',
    
    # Exercise 4
    'DataTransform',
    'NormalizeColumns',
    'StandardizeColumns',
    'RemoveDuplicates',
    'StandardizeText',
    'RemoveOutliers',
    'TransformFactory',
    
    # Exercise 5
    'DataPipeline',
    'CSVDataPipeline',
    'AdvancedCSVPipeline',
]
