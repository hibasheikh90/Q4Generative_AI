### Pydantic Examples Summary

1. **Basic Model Validation**:
   - Created a simple `Person` model using `BaseModel`.
   - Email field validated with `EmailStr`.
   - Demonstrated error handling when incorrect data types are passed (e.g. name as integer).

2. **Nested Model with List**:
   - Built a `UserWithAddress` model containing a list of `Address` models.
   - Validated structured data (nested JSON-like dictionaries).
   - Useful for real-world nested data like user profiles.

3. **Custom Field Validation**:
   - Used `@field_validator` (Pydantic V2) to apply rules to the `age` field.
   - Ensured age is always between 0 and 120.
   - Illustrated how to raise meaningful errors with invalid input.

All examples help understand the power of data validation using Pydantic.
