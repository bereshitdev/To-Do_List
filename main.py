from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from crud import create_task, get_tasks, get_task, update_task, delete_task
from schemas import Task, Task_create, Task_update
from database import get_db, create_tables

# Inicializa o FastAPI
app = FastAPI()

# Cria as tabelas do banco de dados quando a aplicação inicia
@app.on_event("startup")
def on_startup():
    create_tables()

# Rota para criar uma nova tarefa
@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(task: Task_create, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

# Rota para listar todas as tarefas
@app.get("/tasks/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

# Rota para obter uma tarefa específica por ID
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

# Rota para atualizar uma tarefa
@app.put("/tasks/{task_id}", response_model=Task)
def update_existing_task(task_id: int, task: Task_update, db: Session = Depends(get_db)):
    db_task = update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

# Rota para deletar uma tarefa
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    if not delete_task(db, task_id=task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return  # Retorna nada com 204 No Content