from sqlmodel import SQLModel, Field
from sqlmodel import select
from typing import Optional
from pydantic import validator
from statistics import mean
from datetime import datetime


class Beer(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, index=True)
    name: str
    style: str
    flavor: int
    image: int
    cost: int
    rate: int = 0
    date: datetime = Field(default_factory=datetime.now)

    
    @validator("flavor", "image", "cost")
    def validate_ratings(cls, v, field):
        # recebe a classe, o valor para validar e o campo para validação- Pydantic
        # garantir que não haverá entra de dados contrário a essa regra.
        if v < 1 or v > 10:
            raise RuntimeError(f"{field.name} must be between 1 and 10.")
        return v


    @validator("rate", always=True)
    def calculate_rate(cls, v, values):
        # para calcular a média dos 3 valores (flavor, image e cost)
        # passa no decorator o que está calculando...
        rate = mean([values["flavor"], values["image"], values["cost"]])
        return int(rate)



brewdog = Beer(name="Bredog", style="Neipa", flavor=6, image=8, cost=8)
