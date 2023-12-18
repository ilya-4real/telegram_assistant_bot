from .repository import SQLAlchemyRepository
from ..models import CurrencySymbol

class CurrencyRepository(SQLAlchemyRepository):
    model = CurrencySymbol