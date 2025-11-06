# Gravity Common Library

Shared components and utilities for all Gravity microservices.

## Features

- ✅ Base Models (Pydantic schemas)
- ✅ Custom Exceptions
- ✅ Database utilities
- ✅ Security utilities (JWT, Password hashing)
- ✅ Redis utilities
- ✅ Logging configuration
- ✅ Common response models
- ✅ Monitoring helpers

## Installation

```bash
poetry add ../common-library
```

## Usage

```python
from gravity_common.models import BaseModel
from gravity_common.exceptions import NotFoundException
from gravity_common.security import create_access_token
from gravity_common.database import get_db
```
