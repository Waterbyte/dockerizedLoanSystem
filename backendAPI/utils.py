import random, string, datetime
from backendAPI import constants
from passlib.hash import pbkdf2_sha256


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_current_utc():
    return datetime.datetime.utcnow()

def generate_hashedPassword(password):
    return pbkdf2_sha256.hash(password)

def verify_hashedPassword(password,hash):
    return pbkdf2_sha256.verify(password,hash)

def generate_response(VERDICT="0", PAYLOAD=""):
    return {
        constants.response.VERDICT.name:VERDICT,
        constants.response.PAYLOAD.name:PAYLOAD
    }


def generateExactMatchPattern(inpStr):
    return "^" + inpStr + "$"





