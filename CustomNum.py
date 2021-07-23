"""
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
"""


from typing import Any, Iterable, Callable, Union, Mapping
from types import MappingProxyType
from collections.abc import Mapping as Map

__all__ = [
    'CustomNum',
    'CustomNumMeta',
    'FormatNotMatched'
]

class FormatNotMatched(Exception):
    def __init__(self, format_used, raw_member) -> None:
        self.format_used = format_used
        self.raw_member = raw_member
        self.message = "Format and Raw-Member Value does not match"
        super().__init__(self.message)
    
    def __repr__(self) -> str:
        return f"Format: {self.format_used} | Raw Member: {self.raw_member} -> {self.message}"

def __is_dunder__(name: str): return (len(name) > 5) and (name[:2] == name [-2:] == '__') and name[2] != "_" and name[-3] != '_'

def __is_sunder__(name: str): return (len(name) > 3) and (name[:1] == name [-1:] == '_') and name[1] != "_" and name[-2] != '_'

class CustomNumMeta(type):
    def __call__(self, value, *args: Any, create = False, format: dict = None, operator_field_field: str = None, **kwargs: Any):
        # Rough python equivalent of how type.__call__ would look as per my understanding
        # obj = self.__new__(*args, **kwargs) # Making instance of self by calling it's `__new__` method
        # if obj is not None and isinstance(obj, self) and hasattr(obj, '__init__'): # Checking if our returned instance isn't none and calling `__init__` on it if `__init__` exists
        #     init_return = obj.__init__(*args, **kwargs) # Calling `__init__` here
        #     if init_return is not None: # raising error if `__init__` returns something
        #         raise TypeError("__init__() should return None, not '{}'".format(type(init_return)))
        # return obj # Returning the object created
        pass

    def __new__(
        cls, # `__new__` is a static-method by default so it's value is equal to `CustomNumMeta` || This is usually refered-to as `metacls`
        name: str, # Name of the class which is formed by `CustomNumMeta`, here it's `'CustomNum'` (a string) || This is usually refered to `cls`
        bases: tuple, # Tuple of all the classes it 'inherits' from, is a tuple containing different classes to inherit from
        namespace: dict, # The stuff we defined inside the class, also refered to as `classdict` sometimes, is a dictionary
        format: Union[Mapping, Callable] = None, # Custom kwarg we can pass during creation of class
        operator_field: str = None, # Field for applying `greater-than', 'less-than', and 'equal-to' operations if format is given
        ignore: list = None, # Ignore to ignore given values so they function like they would do in any regular class 
        *args, **kwargs # To keep out the extra stuff from interfering, is not used anwhere
        ):
        # namespace.setdefault("__ignore__", []).append('__ignore__') # adding a key called ignore if it does not exists. After that, adding '__ignore__' to the list associated with __ignore__ key in the dict
        # ignore = namespace['__ignore__'] # Grabbing the ignore list and storing it in a variable
        # TODO: Add __ignore__ ; __format__ ; __operator_field__ implimentation

        if format and operator_field and (operator_field not in format.keys()): # Validation for operator-field being in format
            raise KeyError(f"'{operator_field}' was not found in format")

        new_namespace = namespace.copy()
        raw_members = {}
        for k in namespace:
            if not (__is_sunder__(k) or __is_dunder__(k) or callable(namespace[k]) or ((k in ignore) if ignore else None)):
                new_namespace.pop(k, None)
        # checking keys and removing all Qualified Names from namespace of new class

        for base in reversed(bases):
            if isinstance(base, cls):
                raw_members.update(dict(base.__members__))
                # Inheriting member values from parents if they are an instance of CustomNumMeta
        raw_members.update({k:namespace[k] for k in namespace if k not in new_namespace})
        # updating in raw_members for qualified values defined in class's namespace

        self = super().__new__(cls, name, bases, new_namespace) # Creating the CustomNum class
        # Making a new class of type `cls`, name `name`, which inherits from all classes in `bases`
        # and which contains all things defined in `new_namespace`

        member_map = {}

        for raw_member_key in raw_members:
            raw_member = raw_members[raw_member_key]
            if format is not None:
                if callable(format): # If callable, set value equal to returned value from format
                    member = format(raw_member)
                elif isinstance(format, Map) and isinstance(raw_member, Map):
                    try:
                        assert format.keys() == raw_member.keys()
                        member = object.__new__(self)
                        super(self, member).__setattr__('__name__', raw_member_key)
                        for k in format:
                            assert isinstance(raw_member[k], format[k]) # Checking here is only on first level
                            super(self, member).__setattr__(k, raw_member[k])
                    except AssertionError:
                        raise FormatNotMatched(format, raw_member)
                else:
                    raise FormatNotMatched(format, raw_member)
            else: # If format not none, add as is
                member = raw_member
            
            member_map[raw_member_key] = member
            super().__setattr__(self, raw_member_key, member)
        # Format matching and applying before setting it as a class attribute

        super().__setattr__(self, '__members__', MappingProxyType(member_map))
        super().__setattr__(self, '__raw_members__', MappingProxyType(raw_members))
        super().__setattr__(self, '__format_used__', format if format else None)
        super().__setattr__(self, '__operator_field__', operator_field if format and operator_field else None)

        if self is not None and isinstance(self, cls) and hasattr(self, '__init__'): # Checking if our returned instance isn't none and calling `__init__` on it if `__init__` exists
            init_return = self.__init__(name, bases, namespace, format=format, ignore=ignore, *args, **kwargs) # Calling `__init__` here
            if init_return is not None: # raising error if `__init__` returns something
                raise TypeError("__init__() should return `None`, not '{}'".format(init_return.__class__))
        return self # Returning the object created


    # def __init__(self, name, bases, namespace, *args, **kwargs) -> None:
    #     pass

    def __bool__(self): # Defines how it's conversion to a boolean will work and whether it'll be `True` or `False`
        """
        Classes always return `True`
        """
        return True

    def __contains__(self, obj) -> bool: # Determine if an object is contained inside this bj using `in` or similar methods
        """
        Check if an object is in member-values
        """
        return (obj in self.__members__.values())

    def __getattr__(self, name: str) -> Any: # Get an attribute from the CustomNum Class
        """
        Returns the member with a matching name
        """
        if __is_dunder__(name):
            raise AttributeError(name)
        try:
            return self.__members__[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None: # Method called for setting an attribute
        """
        Block attempts to reassign members
        """
        if name in self.__members__:
            raise AttributeError("Can not re-assign members.")
        return super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None: # Method called for deleting an attribute
        """
        Block attempts to delete members
        """
        if name in self.__members__:
            raise AttributeError("Can not detele members.")
        return super().__delattr__(name)

    def __dir__(self) -> Iterable[str]: # Returns all available attributes of an object
        return ['__class__', '__doc__', '__members__', '__raw_members__', '__module__', '__qualname__', '__format_used__', '__operator_field__', *self.__members__.keys()]

    def __getitem__(self, name): # method used for item lookup of an object by `obj[name]`
        """
        Returns a member associated with name, else raises `KeyError`
        """
        return self.__members__[name]

    def __setitem__(self, name, value): # Method defining reassignment of an item
        """
        Blocks and raises error for reassigning items
        """
        raise ValueError("Can not reassign items")

    def __delitem__(self, name): # Method defining how deletion of an item works
        """
        Blocks and raises error for deleting items
        """
        raise ValueError("Can not delete items")

    def __iter__(self): # Fefines how iteration of this object world work, returns a generator object
        """
        Returns an iterator of member names for iteration,
        similar to how a dict would work
        """
        return (key for key in self.__members__.keys())

    def __len__(self) -> int: # Defines the result of `len(obj)`
        return len(self.__members__)

    def __repr__(self) -> str: # Defines how an object would be represented
        return f"<CustomNum: '{self.__name__}'>"

    def __str__(self) -> str: # Defines how string conversion of an object (`str(obj)`) would work
        return repr(self)

    def __reversed__(self): # Defines the reverse iterator for class using `reversed`
        """
        Return member names in a reversed order
        """
        return reversed(self.__members__.keys())





class CustomNum(metaclass=CustomNumMeta):

    def __repr__(self) -> str:
        return "<{self.__class__.__name__}: '{self.__name__}'>"

    def __dir__(self) -> Iterable[str]:
        return ['__class__', '__doc__', '__module__'] + (list(self.__class__.__format_used__.keys()) if self.__class__.__format_used__ else [])
    
    def __str__(self) -> str:
        return self.__name__

    def __hash__(self) -> int: # Result of hashing the object
        return hash(self.__name__)

    def __gt__(self, other): # Defining Greater-Than
        if isinstance(other, self.__class__) and self.__class__.__format_used__ and self.__class__.__operator_field__: # Both have same class, class has non-None format_used and operator_field
            return getattr(self, self.__class__.__operator_field__) > getattr(other, self.__class__.__operator_field__)
        raise NotImplementedError(f"Operation is not supported between operands of type '{type(self)}' and '{type(other)}'")
    
    def __gt__(self, other): # Defining Less-Than
        if isinstance(other, self.__class__) and self.__class__.__format_used__ and self.__class__.__operator_field__:
            return getattr(self, self.__class__.__operator_field__) < getattr(other, self.__class__.__operator_field__)
        raise NotImplementedError(f"Operation is not supported between operands of type '{type(self)}' and '{type(other)}'")

    def __gt__(self, other): # Defining Equal-To
        if isinstance(other, self.__class__) and self.__class__.__format_used__ and self.__class__.__operator_field__:
            return getattr(self, self.__class__.__operator_field__) == getattr(other, self.__class__.__operator_field__)
        raise NotImplementedError(f"Operation is not supported between operands of type '{type(self)}' and '{type(other)}'")