from pydantic import BaseModel,EmailStr
class person(BaseModel):
    name: str
    age: int
    address: str
    email:EmailStr


try:
    P1=person(name="Ali",age=20,address="abc",email="ali1122@gmail.com")
    print(P1)
except Exception as e:
    print(e)

#error will raise if i will give wrong name type

try:
    P1=person(name= 123,age=20,address="abc",email="ali1122@gmail.com")
    print(P1)
except Exception as e:
    print(e)