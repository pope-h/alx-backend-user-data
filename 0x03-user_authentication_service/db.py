#!/usr/bin/env python3
"""Data Base module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """Data Base class

    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a new user
        """
        new_user = User(email=email, hashed_password=hashed_password)

        session = self._session
        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ find user by specification
            which must be a key word arg
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except (NoResultFound, InvalidRequestError):
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user by *arg
           with attributes in **kwargs
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        attr = user.__table__.columns.keys()
        kargs = kwargs.items()

        for key, val in kargs:
            if key not in attr:
                raise ValueError
        setattr(user, key, val)

        session.add(user)
        session.commit()
