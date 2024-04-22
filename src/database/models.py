from sqlalchemy import Column, INT, VARCHAR, ForeignKey, CheckConstraint, TIMESTAMP, BOOLEAN, CHAR
from sqlalchemy.orm import relationship

from .base import Base
from .storage import FileSystemStorage
from .types import FileType

__all__ = (
    "Base",
    "Category",
    "ArticleTag",
    "Tag",
    "User",
    "Article",
)


# CategoryTag = Table(
#     "category_tags",
#     Base.metadata,
#     Column("tag_id", ForeignKey("tags.id"), nullable=False, primary_key=True),
#     Column("article_id", ForeignKey("articles.id"), nullable=False, primary_key=True)
# )


class ArticleTag(Base):
    __tablename__ = "article_tags"

    tag_id = Column(
        ForeignKey("tags.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )
    article_id = Column(
        ForeignKey("articles.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint(sqltext="length(name) >= 2"),
    )

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)

    articles = relationship(argument="Article", back_populates="category")

    def __str__(self) -> str:
        return self.name


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        CheckConstraint(sqltext="length(name) >= 2"),
    )

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)

    articles = relationship(argument="Article", secondary=ArticleTag.__table__, back_populates="tags")

    def __str__(self) -> str:
        return self.name


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = (
        CheckConstraint(sqltext="length(title) >= 2"),
        CheckConstraint(sqltext="length(body) >= 2"),
    )

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(length=128), nullable=False)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    body = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now", nullable=False)
    is_published = Column(BOOLEAN, server_default="false", nullable=False)
    picture = Column(FileType(storage=FileSystemStorage(upload_to="media")), nullable=True)
    category_id = Column(
        INT,
        ForeignKey(column=Category.id, ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    category = relationship(argument=Category, back_populates="articles")
    tags = relationship(argument=Tag, secondary=ArticleTag.__table__, back_populates="articles")

    def __str__(self) -> str:
        return self.title


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(sqltext="length(email) >= 5"),
    )

    id = Column(INT, primary_key=True)
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

    def __str__(self) -> str:
        return self.email
