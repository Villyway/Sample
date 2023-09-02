from enum import Enum

class AddressType(Enum):
    PERMANENT = "PERMANENT"
    CURRENT = "CURRENT"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    

class Roles(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    MANAGER = "MANAGER"  # All privileges except delete
    OPERATOR = "OPERATOR"  # Can approve websites
    CUSTOMER = "CUSTOMER" #Customer
    STORE_EXECUTIVE = "STORE EXECUTIVE"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def staff_choices(cls):
        return tuple((i.name, i.value) for i in cls if i.value != Roles.BUSINESS_OWNER.value)

    @classmethod
    def business_choices(cls):
        return tuple((i.name, i.value) for i in cls if i.value == Roles.BUSINESS_OWNER.value)
    

class MobileNumberTypes(Enum):
    MOBILE = "MOBILE"
    LANDLINE = "LANDLINE"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Color(Enum):
    SUCCESS = "success"
    PRIMARY = "primary"
    DANGER = "danger"
    WARNING = "warning"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    

class FileCategories(Enum):
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"
    PDF   = "PDF"
    AUDIO = "AUDIO"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    

class FileProvider(Enum):
    OWN = "OWN"
    YOUTUBE = "YOUTUBE"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
