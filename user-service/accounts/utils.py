class Result:
    def __init__(self, success: bool, data=None, error=None):
        self._success = success
        self._data = data
        self._error = error

    def is_success(self) -> bool:
        return self._success

    def get_error_message(self):
        return self._error

    def get_data(self):
        return self._data if self._success else None
    
    @staticmethod
    def success(data=None):
        return Result(success=True, data=data)

    @staticmethod
    def error(error_message):
        return Result(success=False, error=error_message)

    def to_dict(self):
        return {"success": self._success, "data": self._data, "error": self._error}

    def __repr__(self):
        return f"Result(success={self._success}, data={self._data}, error={self._error})"
    