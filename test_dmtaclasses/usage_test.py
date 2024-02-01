from typing import Literal
from datetime import date
from dmtaclasses.dmtaclasses import dataclass


@dataclass()
class Myclass:
    x:int
    y:float
    date:Literal["2022-01-01"]|date
    temps:Literal["0.1"]|None

@dataclass()
class Myclass2:
    variabl1:int
    variabl2:int
    variadl3:int|Literal["2023u01u03"]
    variabl4:float
    variabts:float|Literal["1"]



c = Myclass(1,1.0,1,1)
c = Myclass2(1,1.0,1,1,1)