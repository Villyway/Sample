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


class State(Enum):
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class CustomerType(Enum):
    DISTRIBUTOR = "DISTRIBUTOR"
    DEALER = "DEALER"
    RETAILER = "RETAILER"
    CONSUMER = "CONSUMER"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class StockTransection(Enum):
    CR = "CR"
    DR = "DR"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class ReportTimeLine(Enum):
    YEARLY = "YEARLY"
    MONTHLY = "MONTHLY"
    DAILY = "DAILY"
    TODAY = "TODAY"

    @classmethod
    def choices(cls):
        return tuple((i.name,i.value) for i in cls)
    

class InventryReportType(Enum):
    ISSUED_ITEM = "ISSUED ITEM"
    RECEIVED_ITEM = "RECEIVED ITEM"
    BOTH = "BOTH"
    CURRENT_STOCK = "CURRENT_STOCK"

    @classmethod
    def choices(cls):
        return tuple((i.name,i.value) for i in cls)
    

class OrderStatus(Enum):
    DELIVERED = "DELIVERED"
    PENDING = "PENDING"
    ON_THE_WAY = "ON THE WAY" 
    IN_TRANSPORT = "IN TRANSPORT"

    @classmethod
    def choices(cls):
        return tuple((i.name,i.value) for i in cls)
    

class PackingType(Enum):
    BOX = "BOX"
    LOOSE = "LOOSE"

    @classmethod
    def choices(cls):
        return tuple((i.name,i.value) for i in cls)


class OrderUOM(Enum):
    NOS = "NOS"
    SET = "SET"

    @classmethod
    def choices(cls):
        return tuple((i.name,i.value) for i in cls)