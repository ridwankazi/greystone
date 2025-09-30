from __future__ import annotations

from typing import Generic, Iterable, Optional, Sequence, TypeVar
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseService(Generic[ModelT]):
    def __init__(self, db: Session, model_type: type[ModelT]):
        self.db = db
        self.model_type = model_type

    def get(self, id_: int) -> Optional[ModelT]:
        return self.db.get(self.model_type, id_)

    def list(self, *, skip: int = 0, limit: int = 100) -> Sequence[ModelT]:
        return (
            self.db.query(self.model_type)  # type: ignore[attr-defined]
            .offset(skip)
            .limit(limit)
            .all()
        )

    def add(self, instance: ModelT) -> ModelT:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def add_many(self, instances: Iterable[ModelT]) -> None:
        self.db.add_all(list(instances))
        self.db.commit()

    def delete(self, instance: ModelT) -> None:
        self.db.delete(instance)
        self.db.commit()
