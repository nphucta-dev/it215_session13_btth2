from datetime import datetime, timezone
from typing import Any, Optional


def build_response(
    status_code: int,
    message: str,
    data: Any = None,
    error: Optional[str] = None,
    path: str = "",
) -> dict:
    """
    Chuẩn hóa cấu trúc response theo quy định 6 trường:
    statusCode, message, error, data, path, timestamp
    """
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
