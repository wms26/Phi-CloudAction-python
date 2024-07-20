class SessionTokenInvalid(Exception):
    def __init__(self, message, sessionToken: str | None):
        super().__init__(message)
        self.message = message
        self.sessionToken = sessionToken

    def __str__(self):
        return f'SessionToken不合法喵！{self.message}："{self.sessionToken}"'


class SaveFileChecksumError(Exception):
    def __init__(self, expected_checksum, actual_checksum):
        super().__init__()
        self.expected_checksum = expected_checksum
        self.actual_checksum = actual_checksum

    def __str__(self):
        return f'存档checksum错误喵！应为："{self.expected_checksum}"，而不是："{self.actual_checksum}"'
