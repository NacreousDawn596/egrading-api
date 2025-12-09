# Egrading API

A Python wrapper for the ENSAM egrading platform.

## Installation

```bash
pip install egrading_api
```

## Usage

```python
from egrading_api import Student

# Initialize client
student = Student("email@ensam.ac.ma", "password")

# List exams
exams = student.listExams()
print(exams)
```
