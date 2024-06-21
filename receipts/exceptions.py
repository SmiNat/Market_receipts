class FileStructureError(Exception):
    def __init__(self, message: str, extra_info: str | None = None, *args):
        super().__init__(message)
        if extra_info:
            self.extra_info = extra_info
        super(FileStructureError, self).__init__(message, extra_info, *args)
