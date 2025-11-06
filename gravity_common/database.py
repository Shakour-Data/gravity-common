"""
Database utilities and base classes.

Provides reusable database components that each microservice can use
while maintaining complete independence.
"""

from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy import Column, Integer, DateTime, func


# Base class for SQLAlchemy models
Base = declarative_base()


class DatabaseConfig:
    """
    Database configuration class.
    
    Each microservice creates its own instance with its own database URL.
    """
    
    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        pool_size: int = 20,
        max_overflow: int = 10,
        pool_pre_ping: bool = True,
        pool_recycle: int = 3600,
    ):
        """
        Initialize database configuration.
        
        Args:
            database_url: Database connection URL
            echo: Whether to echo SQL statements
            pool_size: Number of connections to maintain
            max_overflow: Max overflow connections
            pool_pre_ping: Test connections before using
            pool_recycle: Recycle connections after N seconds
        """
        self.database_url = database_url
        self.echo = echo
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_pre_ping = pool_pre_ping
        self.pool_recycle = pool_recycle
        
        # Create async engine
        self.engine = create_async_engine(
            self.database_url,
            echo=self.echo,
            poolclass=NullPool,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_pre_ping=self.pool_pre_ping,
            pool_recycle=self.pool_recycle,
        )
        
        # Create session maker
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get async database session.
        
        Yields:
            AsyncSession: Database session
        """
        async with self.async_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def close(self) -> None:
        """Close database connection pool."""
        await self.engine.dispose()


class TimestampMixin:
    """Mixin to add timestamp columns to SQLAlchemy models."""
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)


class BaseDBModel(Base):
    """
    Base SQLAlchemy model with common fields.
    
    All microservice models can inherit from this.
    """
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)


async def check_database_connection(db_config: DatabaseConfig) -> bool:
    """
    Check if database connection is working.
    
    Args:
        db_config: Database configuration instance
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        async with db_config.engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False
