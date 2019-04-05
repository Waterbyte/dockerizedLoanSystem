import random,string
from backendAPI import constants

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_login_response(VERDICT="0",TOKEN=""):
    return {
        constants.response.VERDICT:VERDICT,
        constants.misc_webargs.TOKEN:TOKEN
    }