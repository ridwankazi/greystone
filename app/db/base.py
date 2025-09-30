from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models here to register them with SQLAlchemy metadata
# When adding new models, import them below
from app.models.user import User  # noqa: F401,E402
from app.models.loan import Loan  # noqa: F401,E402
