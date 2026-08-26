# AI-Assisted Programming Lab Starter

**Teaching Material for the AI-Assisted Programming Workshop at HSU**

---

## Overview

This repository contains educational materials designed for the **AI-Assisted Programming workshop** at Helmut Schmidt University (HSU). It provides hands-on exercises for learning Python programming, code refactoring, data analysis, and AI-assisted development practices.

## Project Structure

```
aiprog-lab-starter/
├── README.md                    # This file
├── AGENTS.md                   # Agent instructions and project rules
├── legacy_analysis.py          # Intentionally flawed script for refactoring
├── data/
│   └── raw/
│       └── measurements.csv     # Sample field study data
└── capstone/                   # Directory for student projects
```

## Educational Objectives

- **Python Fundamentals**: Practice core Python programming concepts
- **Code Refactoring**: Learn to improve existing code structure and maintainability
- **Data Analysis**: Work with real-world CSV data for analysis and visualization
- **AI-Assisted Programming**: Develop skills in using AI tools for coding tasks
- **Best Practices**: Apply PEP 8 standards, type hints, and proper documentation

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd aiprog-lab-starter
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Verify installation:**
   ```bash
   uv run python --version
   ```

## Usage Examples

### Running the Legacy Analysis Script

The `legacy_analysis.py` script is intentionally flawed and serves as the basis for refactoring exercises:

```bash
# Run the original script
uv run python legacy_analysis.py
```

### Working with Data

The sample dataset contains environmental measurements for analysis:

```bash
# View the raw data
head -n 10 data/raw/measurements.csv

# Process data using Python
uv run python -c "
import csv
with open('data/raw/measurements.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        break  # Print header only
"
```

## Data Description

### Sample Dataset: `data/raw/measurements.csv`

- **Format**: CSV (Comma-Separated Values)
- **Header Row**: Yes
- **Columns**:
  - Column 1: Timestamp/ID
  - Column 2: Location
  - Column 3: **Temperature** (float, mixed Celsius/Fahrenheit units)
  - Column 4: Sensor ID
  - Column 5: **Humidity** (float, may use comma as decimal separator)
  - Column 6: Additional metadata

### Known Data Issues

- **Temperature Units**: Mixed Celsius and Fahrenheit values without clear distinction
- **Decimal Format**: Humidity values may use comma (`,`) instead of period (`.`) as decimal separator
- **Missing Data**: Some entries may contain missing or invalid values
- **2024 Data**: Referenced in TODO but currently missing from dataset

### Expected Data Handling

When working with this data, ensure your code:
- Handles mixed temperature units appropriately
- Properly parses both comma and period decimal separators
- Gracefully handles missing or invalid data
- Uses relative paths from the project root

## Refactoring Exercises

The `legacy_analysis.py` script contains several intentional issues for educational purposes:

### Common Refactoring Tasks

1. **Replace hardcoded paths** with relative paths using `pathlib`
2. **Extract repeated logic** into modular functions
3. **Add error handling** for data parsing and file operations
4. **Implement unit conversion** for temperature standardization
5. **Add type hints** and docstrings for better documentation
6. **Save outputs** to appropriate directories (`data/processed/`, `data/visualizations/`)

### Example Refactoring Pattern

```python
# Before: Hardcoded path
with open('/absolute/path/to/measurements.csv', 'r') as f:
    data = f.read()

# After: Relative path with pathlib
from pathlib import Path

data_path = Path('data/raw/measurements.csv')
with open(data_path, 'r') as f:
    data = f.read()
```

## Output Directories

- **Processed Data**: Save cleaned/processed data to `data/processed/`
- **Visualizations**: Save plots and charts to `data/visualizations/`

## Student Contributing Guidelines

### General Rules

- **Preserve Educational Intent**: Keep changes incremental and focused on learning objectives
- **Follow Best Practices**: Adhere to PEP 8, use type hints, add docstrings
- **Modular Design**: Prefer small, focused functions over monolithic scripts
- **Path Handling**: Always use `pathlib` for path manipulation
- **No Absolute Paths**: Never use absolute paths in your code

### Code Standards

- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Include type hints for function parameters and return values
- Handle edge cases and invalid data gracefully
- Write tests for new functionality

### Commit Messages

- Use clear, descriptive commit messages
- Reference the specific exercise or feature being addressed
- Keep commits small and focused

## Dependencies

- **Package Manager**: uv
- **Current Dependencies**:
  - `csv` (standard library)
  - `matplotlib` (with Agg backend for non-interactive plotting)
- **New Dependencies**: Justify any additions for educational value

## Common Tasks

### For Instructors

1. Use `legacy_analysis.py` as a starting point for refactoring exercises
2. Demonstrate proper data handling with the CSV file
3. Show how to identify and fix code smells
4. Illustrate test-driven development approaches

### For Students

1. Analyze the legacy script to identify issues
2. Implement incremental improvements
3. Add proper error handling and data validation
4. Create modular, reusable functions
5. Document your code with docstrings and type hints

## Validation

- Verify that averages and plots match expected output
- Ensure scripts run without errors on a fresh clone
- Test with different data scenarios

## Additional Resources

- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pathlib Documentation](https://docs.python.org/3/library/pathlib.html)

## Learning Path

1. **Beginner**: Understand the existing code and data structure
2. **Intermediate**: Refactor the legacy script using best practices
3. **Advanced**: Add new features and comprehensive error handling
4. **Master**: Create your own analysis scripts in the `capstone/` directory

## Support

For questions or issues related to this educational material, please refer to your workshop instructor or teaching assistant.

---

*Designed for the AI-Assisted Programming Workshop at HSU*
*Maintain the educational intent and incremental learning approach*