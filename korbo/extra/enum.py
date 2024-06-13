from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def keys(cls):
        return [k.name for k in cls]

    @classmethod
    def values(cls):
        return [k.value for k in cls]

    @classmethod
    def items(cls):
        return [(k.value, k.name) for k in cls]


class GenderEnum(BaseEnum):
    male = "male"
    female = "female"
    other = "other"


class TokenTypeEnum(BaseEnum):
    consultant = 'consultant',
    freelance = 'freelance',
    startup = 'startup,'
    staff = 'staff',
    super_user = 'superuser',

