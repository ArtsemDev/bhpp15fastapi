from sqlalchemy.orm import DeclarativeBase

__all__ = ("Base", )


class Base(DeclarativeBase):
    # metadata = MetaData(schema="app", quote_schema=True)
    ...
