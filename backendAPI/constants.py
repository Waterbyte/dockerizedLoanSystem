from enum import  Enum

class misc_webargs(Enum):
    USERNAME = 1
    PASSWORD = 2
    TOKEN = 3
    ROLE = 4
    REFERRER = 5

class response(Enum):
    VERDICT = 101

class collectionName(Enum):
    user = 1
    relation = 2
    loans = 3