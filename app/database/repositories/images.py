from sqlalchemy.exc import IntegrityError

from .repository import SQLAlchemyRepository
from ..models import Image

from typing import Literal


class ImageRepository(SQLAlchemyRepository):
    """controls image repository in database"""

    model = Image

    async def set_image(
        self, image_id: str, title: Literal["weather", "currency", "info"]
    ) -> int:
        """sets new image id if exists else creates new"""
        try:
            id = await self.add_one(tg_id=image_id, title=title)
        except IntegrityError:
            id = await self.update_field(
                self.model.title, title, self.model.tg_id, tg_id=image_id
            )
        return id

    async def get_image_id(self, title: Literal["weather", "currency", "info"]) -> str:
        """returns image id from database"""
        image = await self.get_one(self.model.title, title)
        return image.tg_id
