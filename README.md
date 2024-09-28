# GS Onboarding Challenge
Welcome to Orbital's Ground Station Onboarding Challenge! Please visit this [Notion doc](https://www.notion.so/uworbital/Ground-Station-Onboarding-10f8a26d767780d7ae8de921d9782b77) for the challenge instructions. Remember to follow our style guide which is written below.

## Python Style Guide

- We will be following the Python language style guide [PEP8](https://peps.python.org/pep-0008/)
- If there are any discrepancies between this style guide and PEP8, this style guide takes precedence.

### Type Hinting Convention

All function and method parameters (except for the `self` and `cls` parameters) and return signatures should be type hinted.

```python
def my_add(num1: int, num2: int) -> int:
	"""
	@brief Adds two numbers together

	@param num1 - The first number to add.
	@param num2 - The second number to add.
	@return Returns the sum of the two numbers.
	"""
	return num1 + num2
```

### Comments

### Naming Conventions

- `variable_names`, `field_names` and `function_constants` in snake_case
- `_private_field_names`, and `_private_method_names()` in \_snake_case
- `function_names()` and `method_names()` in snake_case
- `CONSTANT_NAMES: Final` and `ENUM_OPTIONS` in CAPITAL_SNAKE_CASE for module and class constants (not for local constant)
- `file_names` in snake_case
- `ClassName` in PascalCase
    ```python
    # For brevity, the class comments were removed but they should be in real code
    import dataclasses

    @dataclasses.dataclass
    class PointTwoDimension:
    	x: int
    	y: int

    class PointTwoDimension:
    	def __init__(x: int, y: int):
    		self.x = x
    		self.y = y
    ```

- `EnumName` in PascalCase

    ```python
    import enum

    class ErrorCode(enum.Enum):
    	SUCCESS = 0
    	INVALID_ARG = 1

    # Accessing:
    ErrorCode.SUCCESS  # <ErrorCode.SUCCESS: 0>
    ErrorCode.INVALID_ARG  # <ErrorCode.INVALID_ARG: 1>
    ```

#### Single Line Comments

Variable and function names should be descriptive enough to understand even without comments. Comments are needed to describe any complicated logic. Use `#` for single-line comments.

#### Function and Method Comments

Function and method comments using `""" """` should exist below the function declaration. For methods, the `self` or `cls` parameter does not require a description.

```python
def my_add(num1: int, num2: int) -> int:
	"""
	@brief Adds two numbers together

	@param num1 - The first number to add.
	@param num2 - The second number to add.
	@return Returns the sum of the two numbers.
	"""
	return num1 + num2
```

```python
def increase_x(self, count: int) -> None:
	"""
	@brief Increases the x attribute by the count.

	@param count - Count to increase the x attribute by.
	"""
	self.x += count
```

#### File Header Comments

File comments are not required

#### Class Comments

- Class comments should exist after the class definition
- Provide a brief description given class purpose
- Provide a section in the class comment listing the attributes, their type and purpose
- Enum class comments do not require listing the attributes

```python
class PointTwoDimension:
	"""
	@brief Class for storing a 2D point
	@attribute x (int) - x coordinate of the point
	@attribute y (int) - y coordinate of the point
	"""

	def __init__(x: int, y: int):
		self.x = x
		self.y = y

@dataclasses.dataclass
class PointTwoDimension:
	"""
	@brief Class for storing a 2D point
	@attribute x (int) - x coordinate of the point
	@attribute y (int) - y coordinate of the point
	"""

	x: int
	y: int
```
 ```python
import enum

# No comments required
class ErrorCode(enum.Enum):
    """
    @brief Enum for the error codes
    """

    SUCCESS = 0
    INVALID_ARG = 1
```

### Imports

#### Grouping Imports

Handled by pre-commit

#### Notes about imports

- Imports should only be used at the top of the file (no function or scoped imports)
- Only modules should be imported

```python
# module1 contains very_long_module_name and function foo and variable var.
#   very_long_module_name contains bar

# Yes:
from module1 import very_long_module_name as module2  # Casting to shorter name
import module1

module1.foo()
module1.var
module2.bar()

# No:
from module1.very_long_module_name import bar
from module1 import foo, var

foo()
var
bar()
```

### Other Style Guide Points

- Only imports, function, class, and constants declarations and the `if __name__ == '__main__'` should be in module scope
- Entry point to a script or program should be through the `main` function
- Add a trailing comma after elements of a list, if you wish to make/preserve each element on a separate line
