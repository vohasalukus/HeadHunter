from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app.database import async_session
from app.exceptions import ModelNotFoundException


class BaseRepository:
    model = None

    @classmethod
    def build_joinedload(cls, include: str):
        parts = include.split('.')
        option = joinedload(getattr(cls, parts[0]))
        current_class = cls
        for i in range(len(parts)-1):
            current_class = getattr(current_class, parts[i]).property.mapper.class_
            option = option.joinedload(getattr(current_class, parts[i+1]))
        return option

    @classmethod
    async def create(cls, **data):
        async with async_session() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            return instance

    @classmethod
    async def get_or_create(cls, includes: List[str] = None, defaults: dict = None, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                return instance, False
            else:
                if defaults is None:
                    defaults = {}
                instance = cls.model(**filters, **defaults)
                session.add(instance)
                await session.commit()
                return instance, True

    @classmethod
    async def update_or_create(cls, defaults: dict = None, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                for key, value in defaults.items():
                    setattr(instance, key, value)
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance, False
            else:
                instance = cls.model(**filters, **defaults)
                session.add(instance)
                await session.commit()
                return instance, True

    @classmethod
    async def update_by_filter(cls, filter, **data):
        async with async_session() as session:
            query = select(cls).filter(filter)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise ModelNotFoundException
            for key, value in data.items():
                setattr(result, key, value)
            await session.commit()
            return result

    @classmethod
    async def update(cls, id, data):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if not instance:
                return {'message': 'Post not found'}
            for key, value in data.dict().items():
                setattr(instance, key, value)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    @classmethod
    async def destroy(cls, id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            instance = result.scalar()
            session.delete(instance)
            await session.commit()
            return {'message': f'Post {id} deleted'}

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id, raise_exception: bool = False, includes: List[str] = None):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance is None and raise_exception:
                raise ModelNotFoundException(f"{cls.model.__name__} with id {id} not found")
            return instance

    @classmethod
    async def get_by(cls, raise_exception: bool = False, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance is None and raise_exception:
                raise ModelNotFoundException(f"{cls.model.__name__} not found")
            return instance

    @classmethod
    async def filter(cls, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def paginate(cls, page: int, limit: int, filter=None, includes: List[str] = None, order_by=None, **filters):
        async with async_session() as session:
            query = select(cls.model).limit(limit).offset((page - 1) * limit)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            if filters:
                query = query.filter_by(**filters)
            if filter is not None:
                query = query.filter(filter)
            if order_by is not None:
                query = query.order_by(order_by)
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def count(cls, filter=None):
        async with async_session() as session:
            if filter is not None:
                query = select(func.count(cls.id)).filter(filter)
            else:
                query = select(func.count(cls.id))
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def bulk_create(cls, instances: List[dict]):
        async with async_session() as session:
            objects = [cls.model(**data) for data in instances]
            session.add_all(objects)
            await session.commit()
            return objects

    @classmethod
    async def bulk_update(cls, updates: List[dict], id_field: str = "id"):
        async with async_session() as session:
            for data in updates:
                instance_id = data.pop(id_field, None)
                if instance_id:
                    query = select(cls.model).filter_by(**{id_field: instance_id})
                    result = await session.execute(query)
                    instance = result.scalar_one_or_none()
                    if instance:
                        for key, value in data.items():
                            setattr(instance, key, value)
                        session.add(instance)
            await session.commit()

    @classmethod
    async def exists(cls, **filters):
        async with async_session() as session:
            query = select(func.count()).filter_by(**filters)
            result = await session.execute(query)
            count = result.scalar()
            return count > 0
