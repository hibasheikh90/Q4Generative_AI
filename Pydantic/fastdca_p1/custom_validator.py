from pydantic import BaseModel, field_validator, ValidationError

#BaseModel: isse hamara custom model banta hai.
#ValidationError: agar koi validation fail ho jaaye to ye error uthta hai.


class User(BaseModel):
    name: str
    age: int

    @field_validator("age") #age field ke liye validation
    @classmethod      #age field ke liye validation
    def age_must_be_valid(cls, v):       #def age_must_be_valid(cls, v): v ka matlab hai wo value jo user input karega.
        if v < 0 or v > 120:
            raise ValueError("Age must be between 0 and 120")
        return v

# Test with invalid age
try:
    user = User(name="Ali", age=150)  # Invalid age
except ValidationError as e:
    print(e)
