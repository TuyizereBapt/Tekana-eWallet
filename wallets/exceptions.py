from rest_framework.exceptions import ValidationError

class InvalidTransactionException(ValidationError):
    def __init__(self, message: str):
        super().__init__(detail=message)
        self.message = message

    def __str__(self):
        return self.message