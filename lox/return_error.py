class ReturnError(Exception):
    def __init__(self, value: object):
        super().__init__(None)  # No message for the exception
        self.value: object = value
