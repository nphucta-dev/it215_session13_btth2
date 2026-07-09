class DataExistException(Exception):
    """Raised when a record that must be unique (e.g. slot_number) already exists."""

    def __init__(self, message: str = "Dữ liệu đã tồn tại trong hệ thống"):
        self.message = message
        super().__init__(message)


class NotFoundException(Exception):
    """Raised when a requested record cannot be found."""

    def __init__(self, message: str = "Không tìm thấy dữ liệu"):
        self.message = message
        super().__init__(message)
