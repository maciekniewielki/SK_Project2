class ValidationException(Exception):
    def __init__(self, value):
        self.value = value


class NameTaken(Exception):
    def __init__(self, value):
        self.value = value