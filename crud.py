
from sqlalchemy.orm import Session
from schemas import Task_create, Task_update
from database import Task  # Importando diretamente o modelo Task do database

# Criar task
def create_task(db: Session, task: Task_create):
    db_task = Task(**task.model_dump())  # Cria uma instância do modelo Task
    db.add(db_task)  # Adiciona a tarefa na sessão do BD
    db.commit()  # Confirma as alterações no BD
    db.refresh(db_task)  # Atualiza a instância com os dados do BD
    return db_task

# Get task by id
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

# Get all tasks
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

# Update task
def update_task(db: Session, task_id: int, task: Task_update):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        # Atualiza os campos que foram passados
        update_data = task.model_dump(exclude_unset=True)
        # Atribui os novos valores aos campos
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

# Excluir task
def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False



