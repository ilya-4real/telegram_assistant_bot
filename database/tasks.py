from .utils.repository import SQLAlchemyRepository
from .models import Task

class TasksRepository(SQLAlchemyRepository):
    model = Task