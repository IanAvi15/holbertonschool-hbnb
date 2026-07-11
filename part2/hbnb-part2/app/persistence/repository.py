"""Repository interface, in-memory implementation, and SQLAlchemy implementation."""
from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """Abstract base class defining the repository interface."""

    @abstractmethod
    def add(self, obj):
        """Add a new object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects from the repository."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object's attributes by its ID."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value."""
        pass


class InMemoryRepository(Repository):
    """In-memory repository implementation using a dictionary."""

    def __init__(self):
        """Initialize the in-memory storage."""
        self._storage = {}

    def add(self, obj):
        """Add a new object to the in-memory storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID from in-memory storage."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects from in-memory storage."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object's attributes in in-memory storage."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object by its ID from in-memory storage."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value from in-memory storage."""
        return next((obj for obj in self._storage.values()
                     if getattr(obj, attr_name) == attr_value), None)


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository implementation for database persistence."""

    def __init__(self, model):
        """Initialize the repository with a SQLAlchemy model class.

        Args:
            model: The SQLAlchemy model class to manage.
        """
        self.model = model

    def add(self, obj):
        """Add a new object to the database."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieve an object by its ID from the database."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all objects from the database."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object's attributes in the database."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Delete an object by its ID from the database."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value from the database."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
