from typing import Optional

from pydantic import BaseModel, field_validator

VALID_ROOM_SIZE = {"SMALL", "MEDIUM", "LARGE"}
VALID_STATUS = {"VACANT", "OCCUPIED"}


class BoardingSlotCreate(BaseModel):
    slot_number: str
    room_size: str
    price_per_day: float
    status: Optional[str] = "VACANT"

    @field_validator("slot_number")
    @classmethod
    def validate_slot_number(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("slot_number không được để rỗng")
        return v.strip()

    @field_validator("room_size")
    @classmethod
    def validate_room_size(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("room_size không được để rỗng")
        if v not in VALID_ROOM_SIZE:
            raise ValueError(f"room_size chỉ được phép nhận một trong các giá trị: {sorted(VALID_ROOM_SIZE)}")
        return v

    @field_validator("price_per_day")
    @classmethod
    def validate_price_per_day(cls, v: float) -> float:
        if v is None or v <= 0:
            raise ValueError("price_per_day phải là số thực lớn hơn 0")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_STATUS:
            raise ValueError(f"status chỉ được phép nhận một trong các giá trị: {sorted(VALID_STATUS)}")
        return v


class BoardingSlotUpdate(BaseModel):
    slot_number: Optional[str] = None
    room_size: Optional[str] = None
    price_per_day: Optional[float] = None
    status: Optional[str] = None

    @field_validator("slot_number")
    @classmethod
    def validate_slot_number(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("slot_number không được để rỗng")
            return v.strip()
        return v

    @field_validator("room_size")
    @classmethod
    def validate_room_size(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("room_size không được để rỗng")
            if v not in VALID_ROOM_SIZE:
                raise ValueError(f"room_size chỉ được phép nhận một trong các giá trị: {sorted(VALID_ROOM_SIZE)}")
        return v

    @field_validator("price_per_day")
    @classmethod
    def validate_price_per_day(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("price_per_day phải là số thực lớn hơn 0")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_STATUS:
            raise ValueError(f"status chỉ được phép nhận một trong các giá trị: {sorted(VALID_STATUS)}")
        return v


class BoardingSlotResponse(BaseModel):
    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str

    class Config:
        from_attributes = True
