# TP-2: CleaningData - Applying OOP and Design Patterns

A comprehensive data cleaning project demonstrating Object-Oriented Programming principles and Design Patterns in Python.

## 📋 Project Overview

This project implements a complete CSV data cleaning pipeline using:
- **OOP Principles**: Classes, inheritance, encapsulation, polymorphism
- **Design Patterns**: Strategy, Decorator, Factory, Template Method
- **Best Practices**: Clean code, modularity, reusability

## 🎯 Learning Objectives

1. **OOP Fundamentals**: Build reusable, maintainable data science classes
2. **Strategy Pattern**: Implement interchangeable algorithms for missing value handling
3. **Decorator Pattern**: Add logging, timing, and validation without modifying original code
4. **Factory Pattern**: Create transformation objects dynamically
5. **Template Method Pattern**: Define a consistent pipeline workflow

## 📁 Project Structure

```
TP-2_CleaningData/
│
├── src/
│   ├── exercise1_csv_reader.py         # CSVReader class (OOP foundation)
│   ├── exercise2_strategy_pattern.py   # Missing value strategies
│   ├── exercise3_decorators.py         # Logging and timing decorators
│   ├── exercise4_factory_pattern.py    # Transformation factory
│   └── exercise5_template_pattern.py   # Complete pipeline
│
├── data/
│   └── (Your CSV files here)
│
├── tests/
│   └── (Unit tests)
│
├── main.py                             # Main demo script
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running Individual Exercises

```bash
# Exercise 1: CSV Reader
python src/exercise1_csv_reader.py

# Exercise 2: Strategy Pattern
python src/exercise2_strategy_pattern.py

# Exercise 3: Decorators
python src/exercise3_decorators.py

# Exercise 4: Factory Pattern
python src/exercise4_factory_pattern.py

# Exercise 5: Complete Pipeline
python src/exercise5_template_pattern.py
```

### Running the Complete Demo

```bash
python main.py
```

## 📚 Exercise Breakdown

### Exercise 1: CSVReader Class (OOP Foundation)

**Key Concepts**: Classes, constructors, methods, encapsulation

```python
reader = CSVReader('data/sample_data.csv')
df = reader.read()
reader.preview(10)
reader.info()
```

**Features**:
- Load CSV files with error handling
- Preview data with customizable rows
- Display dataset information

---

### Exercise 2: Strategy Pattern for Missing Values

**Key Concepts**: Strategy Pattern, inheritance, polymorphism

```python
# Different strategies for handling missing values
strategies = [
    DropMissing(),
    FillMean(),
    FillMode(),
    FillMedian()
]

cleaner = DataCleaner(FillMean())
cleaned_df = cleaner.clean(df)

# Change strategy at runtime
cleaner.set_strategy(DropMissing())
```

**Available Strategies**:
- `DropMissing`: Remove rows with missing values
- `FillMean`: Fill with column mean
- `FillMode`: Fill with most frequent value
- `FillMedian`: Fill with column median

---

### Exercise 3: Decorators for Logging and Timing

**Key Concepts**: Decorator Pattern, function wrapping, aspect-oriented programming

```python
@log_action
@log_time
def process_data():
    # Your code here
    pass
```

**Available Decorators**:
- `@log_action`: Log when methods start and finish
- `@log_time`: Measure execution time
- `@validate_data`: Validate data before processing
- `@performance_report`: Detailed performance metrics

---

### Exercise 4: Factory Pattern for Transformations

**Key Concepts**: Factory Pattern, object creation, abstraction

```python
factory = TransformFactory()

# Create transformations dynamically
normalize = factory.create_transform('normalize', columns=['Age', 'Salary'])
remove_dupes = factory.create_transform('remove_duplicates')
standardize = factory.create_transform('standardize_text', columns=['Name'])
```

**Available Transformations**:
- `normalize`: Min-Max scaling to [0, 1]
- `standardize`: Z-score standardization (mean=0, std=1)
- `remove_duplicates`: Remove duplicate rows
- `standardize_text`: Lowercase and trim text
- `remove_outliers`: Remove outliers using IQR method

---

### Exercise 5: Complete Pipeline (Template Method Pattern)

**Key Concepts**: Template Method Pattern, algorithm skeleton, workflow definition

```python
pipeline = CSVDataPipeline(
    input_file='data/input.csv',
    output_file='data/output.csv',
    missing_strategy=FillMean(),
    transformations=[
        {'type': 'remove_duplicates'},
        {'type': 'standardize_text', 'columns': ['Name']},
        {'type': 'normalize', 'columns': ['Age', 'Salary']}
    ]
)

result = pipeline.run()
```

**Pipeline Steps**:
1. **Load**: Read CSV file
2. **Clean**: Handle missing values
3. **Transform**: Apply transformations
4. **Validate**: Check data quality
5. **Save**: Write to output file

---

## 💡 Design Patterns Explained

### Strategy Pattern
- **Purpose**: Define a family of algorithms, encapsulate each one, make them interchangeable
- **Use Case**: Different ways to handle missing values
- **Benefit**: Add new strategies without modifying existing code

### Decorator Pattern
- **Purpose**: Attach additional responsibilities to objects dynamically
- **Use Case**: Add logging, timing, validation to methods
- **Benefit**: Extend functionality without inheritance

### Factory Pattern
- **Purpose**: Create objects without specifying exact classes
- **Use Case**: Dynamic creation of transformation objects
- **Benefit**: Centralized object creation, easy to extend

### Template Method Pattern
- **Purpose**: Define skeleton of algorithm, let subclasses override steps
- **Use Case**: Data cleaning pipeline with fixed workflow
- **Benefit**: Consistent process, customizable steps

---

## 🔧 Usage Examples

### Example 1: Simple Cleaning

```python
from src.exercise1_csv_reader import CSVReader
from src.exercise2_strategy_pattern import DataCleaner, FillMean

# Read data
reader = CSVReader('data/sample.csv')
df = reader.read()

# Clean data
cleaner = DataCleaner(FillMean())
cleaned_df = cleaner.clean(df)
```

### Example 2: With Decorators

```python
from src.exercise3_decorators import DecoratedCSVReader

reader = DecoratedCSVReader('data/sample.csv')
reader.read()  # Automatically logged and timed
reader.preview(5)
```

### Example 3: Full Pipeline

```python
from src.exercise5_template_pattern import AdvancedCSVPipeline
from src.exercise2_strategy_pattern import FillMedian

pipeline = AdvancedCSVPipeline(
    input_file='data/raw.csv',
    output_file='data/cleaned.csv',
    missing_strategy=FillMedian(),
    transformations=[
        {'type': 'remove_duplicates'},
        {'type': 'remove_outliers', 'columns': ['Score']},
        {'type': 'normalize', 'columns': ['Age', 'Salary']}
    ]
)

result = pipeline.run()
pipeline.generate_report()
```

---

## 📊 Sample Data Format

Your CSV files should have the following format:

```csv
Name,Age,Salary,Department,Score
Alice,25,50000,IT,85
Bob,30,60000,HR,92
Charlie,35,70000,IT,78
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_csv_reader.py

# Run with coverage
python -m pytest --cov=src tests/
```

---

## 🎓 Key Takeaways

1. **OOP Makes Code Reusable**: Encapsulate functionality in classes
2. **Design Patterns Solve Common Problems**: Use proven solutions
3. **Separation of Concerns**: Each class has one responsibility
4. **Open/Closed Principle**: Open for extension, closed for modification
5. **Composition Over Inheritance**: Prefer object composition

---

## 📝 Assignment Checklist

- [x] Exercise 1: CSVReader class implemented
- [x] Exercise 2: Strategy Pattern for missing values
- [x] Exercise 3: Decorators for logging and timing
- [x] Exercise 4: Factory Pattern for transformations
- [x] Exercise 5: Complete pipeline with Template Method

---

## 🚀 Extensions (Bonus)

1. Add more transformation types (encoding, feature engineering)
2. Implement data validation rules
3. Add configuration file support (YAML/JSON)
4. Create visualization for pipeline results
5. Add parallel processing for large datasets

---

## 📚 Resources

- [Python OOP Tutorial](https://docs.python.org/3/tutorial/classes.html)
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 👨‍💻 Author

ADV-DS TP-2 Project

---

## 📄 License

This project is for educational purposes.
