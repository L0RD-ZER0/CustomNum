# CustomNum
## A Better way to make Enumerations


CustomNum is a python module for defining Enumerations of a pre-defined format and customisable operations on each member upon creation. Works by using Python Meta-Classes.
#
## Features:
- Read-Only Enumerated Data
- Enumerated class of a Set Format
- Apply a callable format to values as Format
- Supports pre-defined operations on Mapping-Formatted Enumerations
- Supports iteration and contained-in operations
- Contains notes in module to help understanding Metaclasses in python
- Supports inheritance of members

**Note** : Notes and code is written using a rather non-conventional way of refering to objects for purpose of giving a different perspective on metaclasses

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Examples:

CustomNum can run on python 3.6+

```py
from CustomNum import CustomNum
```
#### Make an Enumeration
```py
from CustomNum import CustomNum

class Data(CustomNum):
    Item1 = ...
    Item2 = ...
    ...
    ItemN = ...
    
print(Data.Item1)
```
Values can be accessed by `class_name`.`member_name` or `class_name`[`member_name`]

#### Apply Format as a Dict
```py
from CustomNum import CustomNum

Employee_Format = {
    'Salary': int,
    'Department': str,
    'Age': int,
}

class Employees(CustomNum, format = Employee_Format):
    Joey = { 'Salary': 1000, 'Department': 'Management', 'Age': 23 }
    Kyle = { 'Salary': 2000, 'Department': 'Management', 'Age': 46 }
    ...
    Mike = { 'Salary': 1500, 'Department': 'Development', 'Age': 21 }
    
for employee in Employees:
    print(employee) # Prints Key name (Joey, Kyle ... Mike) depending on iteration
    print('Salary:',employee.Salary)
    print('Department:', employee.Department)
    print('Age': employee.age)
```
Values assigned to every member can be accessed as attributes.
**Note**: In case format entered doesn't matches with value of any of the members, `FormatNotMatched` will be raised with attributes `format_used` and `raw_member`

#### Use a callable as a format
```py
from CustomNum import CustomNum

def callable_format(raw_member): # This callable can be a function or class
    ... # Operations on raw_member's data
    member = ... # Processed Member Value
    return member # Processed Member is returned 

class Enumeration(CustomNum, format = callable_format):
    ...
```
This will assign value of member as returned by `callable_format`
**Note**: Async functions will return coroutine as member values.

```py
class Enumeration(CustomNum, format = callable_format):
    Item1 = value1
    Item2 = value2
    ...
    ItemN = ValueN
```
will be equivalent to
```py
class Enumeration(CustomNum, format = callable_format):
    Item1 = callable_format(value1)
    Item2 = callable_format(value2)
    ...
    ItemN = callable_format(ValueN)
```


## License

MIT License (MIT)

Copyright (c) 2021-Present L0RD-ZER0

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

(**Yes, it is a free software**)