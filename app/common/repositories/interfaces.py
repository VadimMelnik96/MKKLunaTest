from abc import ABC, abstractmethod
from typing import TypeVar

from app.common.filters.filters import BaseFilter

Entity = TypeVar("Entity")
CreateDTO = TypeVar("CreateDTO")
UpdateDTO = TypeVar("UpdateDTO")
Filters = TypeVar("Filters")
OrderFilters = TypeVar("OrderFilters")
FilterSet = TypeVar("FilterSet")


class IRepository(ABC):
    """Абстрактный CRUD - репозиторий"""

    @abstractmethod
    async def create(self, create_dto: CreateDTO) -> Entity:
        """Интерфейс создания объектов"""
        pass

    @abstractmethod
    async def get_list(
        self, filters: Filters | None = None, order_filters: OrderFilters | None = None
    ) -> list[Entity]:
        """Интерфейс получения списка объектов"""
        pass

    @abstractmethod
    async def get_one(self, filters: Filters | None) -> Entity:
        """Интерфейс получения одного объекта"""
        pass

    @abstractmethod
    async def update(self, update_dto: UpdateDTO, filters: Filters) -> Entity:
        """Интерфейс обновления одного объекта"""
        pass

    @abstractmethod
    async def delete(self, filters: Filters) -> None:
        """Интерфейс удаления одного объекта"""
        pass

    @abstractmethod
    async def count(self, filters: BaseFilter | None = None) -> int:
        """Подсчет количества объектов"""

    @abstractmethod
    async def list_and_count(
            self,
            response_dto: type[Entity] | None = None,
            filters: BaseFilter | None = None,
    ) -> tuple[list[Entity], int]:
        """Получение списка объектов и их общего количества"""

    @abstractmethod
    async def bulk_create(self, bulk_create_dto: list[CreateDTO]) -> list[Entity]:
        """Интерфейс массового создания объектов"""
        pass

    @abstractmethod
    async def filter(self, filters: FilterSet) -> list[Entity]:
        """Фильтрация объектов на основе фильтра с поддержкой сортировки и пагинации."""
