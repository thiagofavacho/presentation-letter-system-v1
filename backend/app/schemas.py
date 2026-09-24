from datetime import datetime
from typing import Optional
 
from pydantic import BaseModel, ConfigDict

 
class UserBase(BaseModel):
    name: str
    username: str
    cpf: str
 
 
class UserCreate(UserBase):
    password: str
    is_admin: bool = False
 
 
class UserOut(UserBase):
    id: int
    is_admin: bool
    active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    cpf: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    active: Optional[bool] = None
 
 
class PromoterBase(BaseModel):
    name: str
    employee_id: str
    cpf: str
    rg: str
    ctps: Optional[str] = None
    pis: Optional[str] = None

    address: str
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cep: Optional[str] = None

    admission_date: datetime
    position: str = "PROMOTOR"
    period: str = "INDETERMINADO"
    company: str = "SB SERVICOS TEMPORARIOS LTDA"
 
 
class PromoterCreate(PromoterBase):
    pass
 
 
class PromoterUpdate(BaseModel):
    name: Optional[str] = None
    employee_id: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    ctps: Optional[str] = None
    pis: Optional[str] = None

    address: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cep: Optional[str] = None

    admission_date: Optional[datetime] = None
    position: Optional[str] = None
    period: Optional[str] = None
    company: Optional[str] = None
    active: Optional[bool] = None
 
 
class PromoterOut(PromoterBase):
    id: int
    active: bool
 
    model_config = ConfigDict(from_attributes=True)
 
 
class StoreBase(BaseModel):
    code: str
    name: str
    address: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    client: Optional[str] = None

 
 
class StoreCreate(StoreBase):
    pass
 

class StoreUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    client: Optional[str] = None
    active: Optional[bool] = None
 
 
class StoreOut(StoreBase):
    id: int
    active: bool
 
    model_config = ConfigDict(from_attributes=True)


class LetterGenerateRequest(BaseModel):
    promoter_employee_id: str
    store_code: str
    letter_date: datetime


class LetterLogOut(BaseModel):
    id: int
    user_id: int
    user_name: str
    promoter_id: int
    promoter_name: str
    promoter_employee_id: str
    store_id: int
    store_code: str
    store_name: str
    letter_date: datetime
    generated_at: datetime
 
    model_config = ConfigDict(from_attributes=True)


class LetterReportOut(BaseModel):
    today: int
    this_week: int
    this_month: int
    
    
