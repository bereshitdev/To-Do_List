
from pydantic import BaseModel,Field
from typing import Optional


# Schema base para criacao/atualizacao de tarefas
class Task_Base(BaseModel):
    title: str = Field(...,min_length=1,max_length=100)
    description: Optional[str] = Field(None,max_length=200)
    completed: bool = False

# Shema para criacao de tarefas (inclui apenas os campos que podem ser enviados
class Task_create(Task_Base):
    pass 

# Shemas para atualizacao de tarefas (inclui todos os campos opicionais para atualizacao parcial)
class Task_update(Task_Base):
    title:Optional[str] =Field(None,min_length=1,max_length=100)
    description:Optional[str]=Field(None,max_length=200)
    completed: Optional[bool]= None

# schema para leitura de tarefas (inclui o ID e todos os campos do BD
class Task(Task_Base):
    id : int

    class config:
        from_attributes = True # ou orm_mode = True em vercoes mais antigas
        # Permite que o pydantic converta os dados do SQLALCHEMY para o modelo pydantic