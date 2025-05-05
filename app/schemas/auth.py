from typing import Optional
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="JWT-токен для аутентификации",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx"
    )
    token_type: str = Field(
        "bearer",
        description="Тип токена (по умолчанию 'bearer')",
        example="bearer"
    )
    expires_in: Optional[int] = Field(
        None,
        description="Время жизни токена в секундах (опционально)"
    )
