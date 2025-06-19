from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import Optional, List, Dict, Any, Annotated


# Making a simple Class with Pydantic
from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import Annotated, Optional, List, Dict, Any

class Address(BaseModel):
    street: Annotated[
        str,
        Field(..., max_length=100, title="Street Address", description="Street address of the patient", examples=["123 Main St"])
    ]
    
    city: Annotated[
        str,
        Field(..., max_length=50, title="City", description="City of the patient", examples=["Dhaka"])
    ]
    
    state: Annotated[
        str,
        Field(..., max_length=50, title="State", description="State of the patient", examples=["Dhaka"])
    ]
    
    zip_code: Annotated[
        str,
        Field(..., min_length=5, max_length=10, title="Zip Code", description="Zip code of the patient", examples=["1212"])
    ]


class Patient(BaseModel):
    profile_url: Optional[AnyUrl] = Field(default=None, description="URL to the patient's profile")
    
    name: Annotated[
        str,
        Field(..., max_length=100, title="Name of the Patient", description="Name of the patient, must be a string with max length 100", examples=["Adnan Abdullah Sadi"])
    ]
    
    address: Annotated[
        Optional[Address],
        Field(default=None, title="Address of Patient", description="Address of the patient, must be a valid address object")
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

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.upper()


    # mode parameter in field Validator : 
    # before -> pass the parameter before type changing
    # after -> pass the parameter after type changing


    # Multiple field validators can be used to validate different fields in the model.
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency_contact' not in model.test_dict:
            raise ValueError('Emergency contact is required for patients over 60 years old')
        return model

    # computed property
    @computed_field
    @property
    def is_adult(self) -> bool:
        """Check if the patient is an adult (age >= 18)"""
        return self.age >= 18
    
     
    



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



temp = patient_1.model_dump_json()
temp = patient_1.model_dump(mode='json')
# temp = patient_1.model_dump(mode='json', exclude_unset=True) # exclude unset fields
# temp = patient_1.model_dump(mode='json', exclude_defaults=True) ## exclude default fields
# temp = patient_1.model_dump(mode='json', exclude_none=True) ## exclude None fields
# temp = patient_1.model_dump(mode='json', by_alias=True) ## use alias for fields
# temp = patient_1.model_dump(mode='json', exclude={'phone'}) ## exclude specific fields
# temp = patient_1.model_dump(mode='json', include={'name', 'age'}) ## include specific fields

print(temp)



