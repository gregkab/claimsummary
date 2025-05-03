class BaseAPIException(Exception):
    """Base exception for API errors"""
    pass

class AIServiceError(BaseAPIException):
    """Exception raised for errors in AI service interactions"""
    pass

class DatabaseError(BaseAPIException):
    """Exception raised for database related errors"""
    pass

class EmailParsingError(BaseAPIException):
    """Exception raised for errors in email parsing"""
    pass 