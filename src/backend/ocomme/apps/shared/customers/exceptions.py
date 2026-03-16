class ServiceException(Exception):
    """Base class cho các lỗi ở tầng Service"""

    pass


class UserDoesNotExistError(ServiceException):
    pass


class TenantCreationError(ServiceException):
    """Lỗi khi không thể khởi tạo Tenant hoặc Schema"""

    pass


class DomainAlreadyExists(ServiceException):
    """Lỗi khi domain đã có người khác đăng ký"""

    pass
