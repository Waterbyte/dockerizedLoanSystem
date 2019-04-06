from enum import  Enum

class misc_webargs(Enum):
    USERNAME = 1
    PASSWORD = 2
    TOKEN = 3
    ROLE = 4
    REFERRER_USERNAME = 5
    REFERRER_TOKEN = 6
    TIMESTAMP=7
    AGENT_NAME = 8
    CUSTOMER_NAME = 9

class response(Enum):
    VERDICT = 101
    PAYLOAD = 102

class collectionName(Enum):
    users = 201
    relations = 202
    loans = 203

class roles(Enum):
    ADMIN = 301
    AGENT = 302
    CUSTOMER = 303