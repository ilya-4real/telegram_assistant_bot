from .repository import SQLAlchemyRepository
from ..models import Image


class ImageRepository(SQLAlchemyRepository):
    model = Image