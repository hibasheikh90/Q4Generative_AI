from pydantic import BaseModel, EmailStr

# Define a nested model


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr  # Built-in validator for email format
    addresses: list[Address]  # List of nested Address models


# Valid data with nested structure
user_data = {
    "id": 2,
    "name": "Ali",
    "email": "ali@example.com",
    "addresses": [
        {"street": "123 abs", "city": "Karachi", "zip_code": "100012"},
        {"street": "678 ghk", "city": "Quetta", "zip_code": "90008"},
    ],
}


