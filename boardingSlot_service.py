from sqlalchemy.orm import Session

from database import engine, Base
from models import BoardingSlot
from exception import DataExistException, NotFoundException

Base.metadata.create_all(bind=engine)


def get_boarding_slot_by_id(db: Session, slot_id: int) -> BoardingSlot:
    """Lấy thông tin chi tiết một khoang lưu trú theo id. Raise 404 nếu không tồn tại."""
    boarding_slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()

    if not boarding_slot:
        raise NotFoundException("Boarding slot not found")

    return boarding_slot


def get_all_boarding_slots_service(db: Session):
    """Lấy danh sách toàn bộ khoang lưu trú."""
    return db.query(BoardingSlot).all()


def create_boarding_slot_service(db: Session, slot_data: dict) -> BoardingSlot:
    """Thêm khoang lưu trú mới. Kiểm tra trùng slot_number trước khi thêm."""
    existed = db.query(BoardingSlot).filter(
        BoardingSlot.slot_number == slot_data["slot_number"]
    ).first()

    if existed:
        raise DataExistException("Slot number already exists")

    try:
        new_slot = BoardingSlot(**slot_data)
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return new_slot

    except Exception:
        db.rollback()
        raise


def update_boarding_slot_service(db: Session, slot_id: int, slot_data: dict) -> BoardingSlot:
    """
    Cập nhật thông tin khoang lưu trú.
    - Kiểm tra tồn tại theo id (raise 404 nếu không có).
    - Ghi đè trực tiếp các thuộc tính được truyền lên (exclude_unset đã xử lý ở route).
    - Giữ nguyên khóa chính id gốc.
    """
    boarding_slot = get_boarding_slot_by_id(db, slot_id)

    new_slot_number = slot_data.get("slot_number")
    if new_slot_number and new_slot_number != boarding_slot.slot_number:
        existed = db.query(BoardingSlot).filter(
            BoardingSlot.slot_number == new_slot_number,
            BoardingSlot.id != slot_id,
        ).first()
        if existed:
            raise DataExistException("Slot number already exists")

    try:
        slot_data.pop("id", None)

        for key, value in slot_data.items():
            setattr(boarding_slot, key, value)

        db.commit()
        db.refresh(boarding_slot)

        return boarding_slot

    except Exception:
        db.rollback()
        raise


def delete_boarding_slot_service(db: Session, slot_id: int) -> None:
    """Xóa khoang lưu trú khỏi hệ thống. Raise 404 nếu không tồn tại."""
    boarding_slot = get_boarding_slot_by_id(db, slot_id)

    try:
        db.delete(boarding_slot)
        db.commit()

    except Exception:
        db.rollback()
        raise
