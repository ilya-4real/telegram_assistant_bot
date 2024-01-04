from sqlalchemy.exc import IntegrityError

from .repository import SQLAlchemyRepository
from ..models import Image

from typing import Literal


class ImageRepository(SQLAlchemyRepository):
    model = Image

    async def set_image(
        self, image_id: str, title: Literal["weather", "currency", "info"]
    ):
        try:
            id = await self.add_one(
                tg_id=image_id, title=title
                )
        except IntegrityError:
            id = await self.update_field(
                self.model.title, title, self.model.tg_id, tg_id=image_id
                )
        return id
    
    async def get_image_id(
            self, title: Literal['weather', 'currency', 'info']
            ) -> str:
        image = await self.get_one(self.model.title, title)
        return image.tg_id