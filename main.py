from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from schemas import BoardingSlotCreate, BoardingSlotUpdate, BoardingSlotResponse
from exception import DataExistException, NotFoundException
from utils import build_response
import boardingSlot_service as service

app = FastAPI(title="API Hệ thống Đặt chỗ Dịch vụ Chăm sóc Thú cưng")


# region Exception Handlers
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=build_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message=exc.message,
            error="Not Found",
            data=None,
            path=str(request.url.path),
        ),
    )


@app.exception_handler(DataExistException)
async def data_exist_exception_handler(request: Request, exc: DataExistException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=build_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=exc.message,
            error="Bad Request",
            data=None,
            path=str(request.url.path),
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    message = errors[0]["msg"] if errors else "Dữ liệu đầu vào không hợp lệ"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=build_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error="Unprocessable Entity",
            data=None,
            path=str(request.url.path),
        ),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=build_response(
            status_code=exc.status_code,
            message=str(exc.detail),
            error="HTTP Error",
            data=None,
            path=str(request.url.path),
        ),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Không lộ Stack Trace / lỗi thô của MySQL ra ngoài, chỉ log nội bộ
    print(f"[Unhandled Exception] {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống, vui lòng thử lại sau",
            error="Internal Server Error",
            data=None,
            path=str(request.url.path),
        ),
    )
# endregion


# region Health
@app.get('/health', tags=['Health'], status_code=status.HTTP_200_OK)
def get_health():
    return {
        "message": "FastAPI is running..."
    }
# endregion


# region Database
@app.get("/database/health", tags=["Database"], status_code=status.HTTP_200_OK)
def get_database_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Kết nối với Database thất bại!"
        )
    else:
        return {
            "message": "Kết nối vơi Database thành công!"
        }
# endregion


# region BoardingSlot CRUD

@app.post("/boarding-slots", tags=["BoardingSlot"], status_code=status.HTTP_201_CREATED)
def create_boarding_slot(payload: BoardingSlotCreate, request: Request, db: Session = Depends(get_db)):
    new_slot = service.create_boarding_slot_service(db, payload.model_dump())

    return build_response(
        status_code=status.HTTP_201_CREATED,
        message="Thêm khoang lưu trú thành công",
        data=BoardingSlotResponse.model_validate(new_slot).model_dump(),
        error=None,
        path=str(request.url.path),
    )


@app.get("/boarding-slots", tags=["BoardingSlot"], status_code=status.HTTP_200_OK)
def get_all_boarding_slots(request: Request, db: Session = Depends(get_db)):
    slots = service.get_all_boarding_slots_service(db)
    data = [BoardingSlotResponse.model_validate(slot).model_dump() for slot in slots]

    return build_response(
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách thành công",
        data=data,
        error=None,
        path=str(request.url.path),
    )


@app.get("/boarding-slots/{slot_id}", tags=["BoardingSlot"], status_code=status.HTTP_200_OK)
def get_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = service.get_boarding_slot_by_id(db, slot_id)

    return build_response(
        status_code=status.HTTP_200_OK,
        message="Lấy thông tin khoang lưu trú thành công",
        data=BoardingSlotResponse.model_validate(slot).model_dump(),
        error=None,
        path=str(request.url.path),
    )


@app.put("/boarding-slots/{slot_id}", tags=["BoardingSlot"], status_code=status.HTTP_200_OK)
def update_boarding_slot(
    slot_id: int,
    payload: BoardingSlotUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    update_data = payload.model_dump(exclude_unset=True)
    updated_slot = service.update_boarding_slot_service(db, slot_id, update_data)

    return build_response(
        status_code=status.HTTP_200_OK,
        message="Cập nhật khoang lưu trú thành công",
        data=BoardingSlotResponse.model_validate(updated_slot).model_dump(),
        error=None,
        path=str(request.url.path),
    )


@app.delete("/boarding-slots/{slot_id}", tags=["BoardingSlot"], status_code=status.HTTP_200_OK)
def delete_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    service.delete_boarding_slot_service(db, slot_id)

    return build_response(
        status_code=status.HTTP_200_OK,
        message="Xóa khoang lưu trú thành công",
        data=None,
        error=None,
        path=str(request.url.path),
    )
# endregion
