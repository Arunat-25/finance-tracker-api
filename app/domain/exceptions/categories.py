from app.domain.exceptions.domain_error import DomainError


class CategoryNameTooShort(DomainError):
    min_length = 1

    def __init__(self, name: str):
        message=f"Название категории не может быть короче {self.min_length}."
        details={
            "provided_name": name,
            "length_of_provided_name": len(name.split()),
            "min_required_length": self.min_length
        }
        super().__init__(message, details)


class CategoryNameTooLong(DomainError):
    max_length = 20

    def __init__(self, name: str):
        message=f"Название категории не может быть длиннее {self.max_length}."
        details={
            "provided_name": name,
            "length_of_provided_name": len(name),
            "max_required_length": self.max_length
        }
        super().__init__(message, details)