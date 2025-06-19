from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import Optional, List, Dict, Any, Annotated


# Making a simple Class with Pydantic
from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import Annotated, Optional, List, Dict, Any

class Patient(BaseModel):
    profile_url: Optional[AnyUrl] = Field(default=None, description="URL to the patient's profile")
    
    name: Annotated[
        str,
        Field(..., max_length=100, title="Name of the Patient", description="Name of the patient, must be a string with max length 100", examples=["Adnan Abdullah Sadi"])
    ]
    
    age: Annotated[
        int,
        Field(default=20, ge=0, le=120, description="Age of the patient, must be between 0 and 120")
    ]
    
    weight: Annotated[
        Optional[float],
        Field(default=None, ge=0, description="Weight of the patient in kg, must be a non-negative float", strict=True)
    ]
    
    email: EmailStr
    phone: int
    
    test_list: Optional[List[str]] = Field(default=None, description="List of tests taken by the patient")
    test_dict: Optional[Dict[str, Any]] = Field(default=None, description="Dictionary of test results for the patient")



    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, value: EmailStr) -> EmailStr:
        if not value.endswith('@NorthSouth.edu'):
            raise ValueError('Email must be a NorthSouth.edu email address')
        return value



# Example usage
patient_info = { # type: ignore
    "name": "John Doe",
    "age": 30,
    "email": "yourEmail@NorthSouth.edu",
    "phone": 1234567890
}


patient_1 = Patient(**patient_info)

def print_patient_info(patient: Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Patient Age: {patient.age}")
    print(f"Patient Email: {patient.email}")
    print(f"Patient Phone: {patient.phone}")


# Print patient information
print_patient_info(patient_1)