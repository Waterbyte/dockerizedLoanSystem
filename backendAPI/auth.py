from marshmallow import ValidationError

from backendAPI import utils,db,constants
from backendAPI.utils import generateExactMatchPattern


def checkToken(username,token):
    query = {constants.misc_webargs.USERNAME.name:username, constants.misc_webargs.TOKEN.name:token}
    val = db.find_docs_count(constants.collectionName.users.name,query)
    if val == 1:
        return True
    else:
        return False

def checkRoles(username,role):
    query = {constants.misc_webargs.USERNAME.name: username, constants.misc_webargs.ROLE.name: role}
    val = db.find_docs_count(constants.collectionName.users.name, query)
    if val == 1:
        return True
    else:
        return False

def checkTokenRole(username,role,token):
    query = {constants.misc_webargs.USERNAME.name: username, constants.misc_webargs.ROLE.name: role, constants.misc_webargs.TOKEN.name:token}
    val = db.find_docs_count(constants.collectionName.users.name, query)
    if val == 1:
        return True
    else:
        return False

def addUser(username,password,role,referrer_username=""):
    try:
        current_time = utils.generate_current_utc()
        doc = {
            constants.misc_webargs.USERNAME.name:username,
            constants.misc_webargs.PASSWORD.name:utils.generate_hashedPassword(password),
            constants.misc_webargs.ROLE.name:role,
            constants.misc_webargs.TIMESTAMP.name:current_time
        }
        db.insert_one_doc(constants.collectionName.users.name,doc)

        #need to make this atomic but for sake of simplicity, lets see it later
        if role == constants.roles.CUSTOMER.name:
            relDoc = {
                constants.misc_webargs.AGENT_NAME:referrer_username,
                constants.misc_webargs.CUSTOMER_NAME:username,
                constants.misc_webargs.TIMESTAMP.name:current_time
            }
            db.insert_one_doc(constants.collectionName.relations.name,relDoc)
    except Exception as e:
        print(e)
        return False
    return True


def username_must_not_exist_in_db(val):
    num_res = db.count_doc(constants.collectionName.users.name, {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(val), '$options': 'i'}})
    if num_res != 0:
        raise ValidationError('Username is already taken.')
    else:
        return None