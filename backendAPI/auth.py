from marshmallow import ValidationError

from backendAPI import utils, db, constants
from backendAPI.utils import generateExactMatchPattern


def checkToken(username, token):
    query = {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'},
             constants.misc_webargs.TOKEN.name: token}
    val = db.find_docs_count(constants.collectionName.users.name, query)
    if val == 1:
        return True
    else:
        return False


def checkRoles(username, role):
    query = {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'},
             constants.misc_webargs.ROLE.name: role}
    val = db.find_docs_count(constants.collectionName.users.name, query)
    if val == 1:
        return True
    else:
        return False


def checkTokenRole(username, role, token):
    query = {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'},
             constants.misc_webargs.ROLE.name: role, constants.misc_webargs.TOKEN.name: token}
    val = db.find_docs_count(constants.collectionName.users.name, query)
    if val == 1:
        return True
    else:
        return False


def addUser(username, password, role, referrer_username=""):
    try:
        current_time = utils.generate_current_utc()
        doc = {
            constants.misc_webargs.USERNAME.name: username,
            constants.misc_webargs.PASSWORD.name: utils.generate_hashedPassword(password),
            constants.misc_webargs.ROLE.name: role,
            constants.misc_webargs.TIMESTAMP.name: current_time
        }
        db.insert_one_doc(constants.collectionName.users.name, doc)

        # need to make this atomic but for sake of simplicity, lets see it later
        if role == constants.roles.CUSTOMER.name:
            relDoc = {
                constants.misc_webargs.AGENT_NAME.name: referrer_username,
                constants.misc_webargs.CUSTOMER_NAME.name: username,
                constants.misc_webargs.TIMESTAMP.name: current_time
            }
            db.insert_one_doc(constants.collectionName.relations.name, relDoc)
    except Exception as e:
        print(e)
        return False
    return True


def username_must_not_exist_in_db(val):
    num_res = db.count_doc(constants.collectionName.users.name, {
        constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(val), '$options': 'i'}})
    if num_res != 0:
        raise ValidationError('Username is already taken.')
    else:
        return None


def checkPassword(username, password):
    expr = {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'}}
    cursor = db.find_docs(constants.collectionName.users.name, expr)
    for val in cursor:  # first object and return
        hash = val[constants.misc_webargs.PASSWORD.name]
        return utils.verify_hashedPassword(password, hash)
    return False


def addToken(username, token):
    filter = {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'}}
    update = {'$set': {constants.misc_webargs.TOKEN.name: token}}
    if db.edit_single_doc(constants.collectionName.users.name, filter, update) > 0:
        return True
    return False


# this function list other users of a particular role excluding requesting user
def listOtherUsers(role, username):
    notcontainingUsername = "^(?!" + username + "$)"  # to learn this, find negative lookahead in regex
    expr = {constants.misc_webargs.USERNAME.name: {"$regex": notcontainingUsername},
            constants.misc_webargs.ROLE.name: role}
    projection = {constants.misc_webargs.USERNAME.name: 1, "_id": 0}
    cursor = db.find_docs_projection(constants.collectionName.users.name, expr, projection)
    list = []
    for val in cursor:
        username = val[constants.misc_webargs.USERNAME.name]
        list.append(username)
    return list


def listCustomers(username):
    expr = {constants.misc_webargs.AGENT_NAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'}}
    cursor = db.find_docs(constants.collectionName.relations.name, expr)
    list = []
    for val in cursor:
        customer = val[constants.misc_webargs.CUSTOMER_NAME.name]
        list.append(customer)
    return list


# admin can see everybody, agents can see all admins, other agents and customers under them, finally customers can't see anybody
def getListOfUsers(username):
    expr = {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'}}
    cursor = db.find_docs(constants.collectionName.users.name, expr)
    role = None
    for val in cursor:
        role = val[constants.misc_webargs.ROLE.name]
    if role == constants.roles.ADMIN.name:
        adminList = listOtherUsers(constants.roles.ADMIN.name, username)
        agentList = listOtherUsers(constants.roles.AGENT.name, username)
        customerList = listOtherUsers(constants.roles.CUSTOMER.name, username)
        return utils.generate_response(1, {constants.roles.ADMIN.name: adminList, constants.roles.AGENT.name: agentList,
                                           constants.roles.CUSTOMER.name: customerList})
    elif role == constants.roles.AGENT.name:
        adminList = listOtherUsers(constants.roles.ADMIN.name, username)
        agentList = listOtherUsers(constants.roles.AGENT.name, username)
        customerList = listCustomers(username)
        return utils.generate_response(1, {constants.roles.ADMIN.name: adminList, constants.roles.AGENT.name: agentList,
                                           constants.roles.CUSTOMER.name: customerList})
    else:
        return utils.generate_response(0, "FAILURE")


def listLoans():
    projection = {"_id": 0}
    cursor = db.find_docs_projection(constants.collectionName.loan_inventory.name,{},projection)
    list = []
    for val in cursor:
        print(val)
        list.append(val)
    return list