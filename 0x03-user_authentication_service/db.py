#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from typing import Dict

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None
        self.attributes = ["id", "email", "hashed_password", "session_id", "reset_token"]

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        """creates new user"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user
    
    def find_user_by(self, **kwarg: Dict) -> User:
        """Finds user in a table with specified attributes"""        
        for attr, name_to_search in kwarg.items():
            if attr not in self.attributes:
                raise InvalidRequestError("Invalid attribute provided.")
        
        try:
            query = self._session.query(User)
            for attr, name_to_search in kwarg.items():
                query = query.filter(getattr(User, attr) == name_to_search)
            user = query.first()
            if user is None:
                raise NoResultFound("User not found.")
        except NoResultFound as e:
            raise NoResultFound("User not found.") from e
        
        return user
    
    def update_user(self, user_id: int, **kwarg: Dict) -> None:
        """updates user"""
        try:
            user = self.find_user_by(id=user_id)
            for attribute, replacement in kwarg.items():
                if attribute not in self.attributes:
                    raise ValueError
                setattr(user, attribute, replacement)
            self.__session.commit()
        
        except NoResultFound:
            pass

        except InvalidRequestError:
            pass
