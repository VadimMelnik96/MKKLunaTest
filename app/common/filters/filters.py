from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderDirection(str, Enum):
    """Направление сортировки"""

    ASC = "asc"
    DESC = "desc"


class Condition(str, Enum):
    """И или Или"""

    AND = "and"
    OR = "or"


class OrderingFilter(BaseModel):
    """Фильтр для сортировки."""

    field: str
    direction: OrderDirection = OrderDirection.ASC


class PaginationFilter(BaseModel):
    """Фильтр для пагинации."""

    limit: Optional[int] = None
    offset: Optional[int] = None


class NestedFilter(BaseModel):
    """Вложенный фильтр для поддержки сложных условий."""

    condition: Optional[Condition] = None
    filters: list[Union["BaseFilter", "NestedFilter"]]

    def to_dict(self) -> dict[str, Any]:
        """Возвращает словарь с полями фильтра, исключая None значения."""
        return self.model_dump(exclude_none=True)


class BaseFilter(BaseModel):
    """Базовый класс для всех фильтров."""

    condition: Optional[Condition] = None
    nested_filters: Optional[list[Union[NestedFilter, "BaseFilter"]]] = None

    model_config = ConfigDict(extra="forbid")

    def to_dict(self) -> dict[str, Any]:
        """Возвращает словарь с полями фильтра, исключая None значения."""
        return self.model_dump(exclude_none=True)


class StringFilter(BaseFilter):
    """Фильтр для строковых полей."""

    eq: Optional[str] = None
    like: Optional[str] = None
    ilike: Optional[str] = None
    startswith: Optional[str] = None
    endswith: Optional[str] = None
    in_: Optional[list[str]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda x: "in" if x == "in_" else x,
    )


class UUIDFilter(BaseFilter):
    """Фильтр для полей типа UUID."""

    eq: Optional[UUID] = None
    in_: Optional[list[UUID]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda x: "in" if x == "in_" else x,
    )


class NumberFilter(BaseFilter):
    """Фильтр для числовых полей."""

    eq: Optional[int] = None
    gt: Optional[int] = None
    lt: Optional[int] = None
    ge: Optional[int] = None
    le: Optional[int] = None
    between: Optional[list[int]] = None
    in_: Optional[list[int]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda x: "in" if x == "in_" else x,
    )


class DateFilter(BaseFilter):
    """Фильтр для полей с датами."""

    eq: Optional[datetime] = None
    gt: Optional[datetime] = None
    lt: Optional[datetime] = None
    ge: Optional[datetime] = None
    le: Optional[datetime] = None
    between: Optional[list[datetime]] = None
    in_: Optional[list[datetime]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda x: "in" if x == "in_" else x,
    )


class BooleanFilter(BaseFilter):
    """Фильтр для булевых полей."""

    eq: Optional[bool] = None


class JSONBFilter(BaseFilter):
    """Фильтр для полей типа JSONB."""

    contains: Optional[dict[str, Any]] = None
    has_key: Optional[str] = None
    key_eq: Optional[dict[str, Any]] = None
    key_in: Optional[dict[str, list[Any]]] = None
