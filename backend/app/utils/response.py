"""统一响应格式"""

from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None

    @classmethod
    def ok(cls, data: Any = None, message: str = "success") -> dict:
        return cls(code=200, message=message, data=data).model_dump()

    @classmethod
    def created(cls, data: Any = None, message: str = "创建成功") -> dict:
        return cls(code=201, message=message, data=data).model_dump()

    @classmethod
    def fail(cls, code: int = 400, message: str = "请求失败", data: Any = None) -> dict:
        return cls(code=code, message=message, data=data).model_dump()

    @classmethod
    def paginated(cls, items: list, total: int, page: int, page_size: int) -> dict:
        return cls(code=200, message="success", data={
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 0,
        }).model_dump()
