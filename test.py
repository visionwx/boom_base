import abc
from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Tuple, TypeVar


class A1:
    name:str = None
    age:int  = None
    def __init__(self, name:str, age:int):
        self.name = name
        self.age  = age
    @classmethod
    def fromDict(cls, **dictData):
        cls.name = dictData.get("name", None)
        if cls.name is None:
            raise Exception("name not provide")
        cls.age  = dictData.get("age", None)
        if cls.age is None:
            raise Exception("age not provide")
        return cls
    def __str__(self):
        return self.name + ", " + str(self.age)

class A2(A1):
    home:str = None
    def __init__(self, name, age, home):
        super().__init__(name, age)
        self.home = home

A = TypeVar('A', A1, A2)

class B:
    a:A = None
    def __init__(self, a:A):
        self.a = a

aa = A1(111, "ASFA")
bb = B(aa)
