from src.core.schemas import APIException


class InvalidSeedData(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=400, detail="The seed data you have provided are invalid"
        )


class InvalidIBAN(APIException):
    def __init__(self, iban: str) -> None:
        super().__init__(
            status_code=400, detail=f"The IBAN ({iban}) you have provided is invalid"
        )
