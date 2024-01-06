from app.database.repositories.images import ImageRepository
from typing import Literal

class ImageService:
    """Service that manages work with images in Telegram"""
    repository = ImageRepository()

    @classmethod
    async def set_image(
        cls, image_id: str, title: Literal['weather', 'currency', 'info']
        ) -> str:
        """sets new telegram image id for concrete type of image and returns it"""
        new_id = await cls.repository.set_image(image_id, title)
        return new_id
    
    @classmethod
    async def get_image_id(self, title: Literal['weather', 'currency', 'info']) -> str:
        """returns image id that compitable with telegram from database"""
        image_id = await self.repository.get_image_id(title)
        return image_id
    