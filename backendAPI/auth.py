import pymongo
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


def addUser(username, password, role, referrer_username="", timezone_x="UTC"):
    try:
        current_time = utils.generate_current_utc()
        doc = {
            constants.misc_webargs.USERNAME.name: username,
            constants.misc_webargs.PASSWORD.name: utils.generate_hashedPassword(password),
            constants.misc_webargs.ROLE.name: role,
            constants.misc_webargs.TIMESTAMP.name: current_time,
            constants.misc_webargs.TIMEZONE.name: timezone_x
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
    projection = {"_id": 0, constants.misc_webargs.TIMESTAMP.name: 0}
    try:
        cursor = db.find_docs_projection(constants.collectionName.loan_inventory.name, {}, projection)
    except:
        return utils.generate_db_error()
    list = []
    for val in cursor:
        list.append(val)
    return list


def isCustomerAgentRelated(agentName, customerName):
    expr = {constants.misc_webargs.AGENT_NAME.name: agentName, constants.misc_webargs.CUSTOMER_NAME.name: customerName}
    count = db.find_docs_count(constants.collectionName.relations.name, expr)
    if count == 1:
        return True
    else:
        return False


def addLoan(args):
    expr = {constants.loanInv.ID.name: args[constants.loanCust.LOAN_INVT_ID.name]}
    loan_object = db.find_docs(constants.collectionName.loan_inventory.name, expr).limit(1)
    minimum_Dur = minimum_Amt = maximum_Dur = maximum_Amt = is_Emi_Avail = None
    for loan_item in loan_object:
        minimum_Amt = loan_item[constants.loanInv.MIN_AMT.name]
        maximum_Amt = loan_item[constants.loanInv.MAX_AMT.name]
        minimum_Dur = loan_item[constants.loanInv.MIN_DURATION.name]
        maximum_Dur = loan_item[constants.loanInv.MAX_DURATION.name]
        is_Emi_Avail = loan_item[constants.loanInv.EMI_AVAILABLE.name]

    cust_amt = args[constants.loanCust.AMT.name]
    cust_dur = args[constants.loanCust.DURATION.name]
    cust_emi_status = args[constants.loanCust.EMI_CHOSEN.name]

    if not (cust_amt <= maximum_Amt and cust_amt >= minimum_Amt):
        return False
    if not (cust_dur <= maximum_Dur and cust_dur >= minimum_Dur):
        return False
    if cust_emi_status == True:
        if is_Emi_Avail != True:
            return False

    loan_doc = {
        constants.loanCust.LOAN_CUST_ID.name: str(getCustomerLoanId()),
        constants.misc_webargs.CUSTOMER_NAME.name: args[constants.misc_webargs.CUSTOMER_NAME.name],
        constants.misc_webargs.REFERRER_USERNAME.name: args[constants.misc_webargs.REFERRER_USERNAME.name],
        constants.loanCust.LOAN_INVT_ID.name: args[constants.loanCust.LOAN_INVT_ID.name],
        constants.loanCust.AMT.name: cust_amt,
        constants.loanCust.DURATION.name: args[constants.loanCust.DURATION.name],
        constants.loanCust.MANDATORY_REQUIREMENT1_LOC.name: args[constants.loanCust.MANDATORY_REQUIREMENT1_LOC.name],
        constants.loanCust.MANDATORY_REQUIREMENT2_LOC.name: args[constants.loanCust.MANDATORY_REQUIREMENT2_LOC.name],
        constants.loanCust.EMI_CHOSEN.name: cust_emi_status,
        constants.loanCust.LOAN_STATE.name: constants.loanState.NEW.name,
        constants.misc_webargs.TIMESTAMP.name: utils.generate_current_utc()
    }
    try:
        db.insert_one_doc(constants.collectionName.loan_customer.name, loan_doc)
    except Exception as e:
        print(e)
        return False
    return True


def viewLoansRequest(username):
    expr = {constants.misc_webargs.USERNAME.name: {'$regex': generateExactMatchPattern(username), '$options': 'i'}}
    cursor = db.find_docs(constants.collectionName.users.name, expr)
    role = None
    for val in cursor:
        role = val[constants.misc_webargs.ROLE.name]

    if role == constants.roles.ADMIN.name:
        expr = {}
    elif role == constants.roles.AGENT.name:
        expr = {constants.misc_webargs.REFERRER_USERNAME.name: username}
    else:
        expr = {constants.misc_webargs.CUSTOMER_NAME.name: username}

    list = []
    projection = {"_id": 0}
    try:
        cursor = db.find_docs_projection(constants.collectionName.loan_inventory.name, expr, projection)
    except:
        return utils.generate_db_error()

    for val in cursor:
        list.append(val)

    return utils.generate_response(1, val)


def getCustomerLoanId():
    val = db.find_and_modify(constants.collectionName.counters.name, {"_id": constants.loanCust.LOAN_CUST_ID.name},
                             {"$inc": {constants.misc_webargs.SEQ_VAL.name: 1}}, {})
    return val['SEQ_VAL']


def editLoanRequest(args):
    val = None
    proj = {"_id": 0}
    expr = {constants.loanCust.LOAN_CUST_ID.name:args[constants.loanCust.LOAN_CUST_ID.name]}
    sortExpr = [(constants.misc_webargs.TIMESTAMP.name,pymongo.DESCENDING)]
    loanRequest = db.find_single_doc_with_desc_sort(constants.collectionName.loan_customer.name, expr, proj, sortExpr)
    for val in loanRequest:
        print(val)
    if constants.loanCust.LOAN_STATE.name in val and  val[constants.loanCust.LOAN_STATE.name] == constants.loanState.ACCEPTED.name:
        return False
    pass

def approveLoanRequest(args):
    proj = {"_id": 0}
    expr = {constants.loanCust.LOAN_CUST_ID.name: args[constants.loanCust.LOAN_CUST_ID.name]}
    sortExpr = {constants.misc_webargs.TIMESTAMP.name: pymongo.DESCENDING}
    loanRequest=db.find_single_doc_with_desc_sort(constants.collectionName.loan_customer.name,expr,proj,sortExpr)
    print(loanRequest)


def editUserInfo(args):
    expr = {constants.misc_webargs.USERNAME.name: {
        '$regex': generateExactMatchPattern(args[constants.misc_webargs.REFERRER_USERNAME.name]), '$options': 'i'}}
    cursor = db.find_docs(constants.collectionName.users.name, expr)
    updt = {}
    role = None
    for val in cursor:
        role = val[constants.misc_webargs.ROLE.name]

    if role == constants.roles.ADMIN.name:
        if constants.misc_webargs.CREDIT_SCORE.name in args and \
                args[constants.misc_webargs.CREDIT_SCORE.name] is not None:
            updt["constants.misc_webargs.CREDIT_SCORE.name"] = args[constants.misc_webargs.CREDIT_SCORE.name]
        if constants.misc_webargs.DOCUMENT1_VER_STATUS.name in args and \
                args[constants.misc_webargs.DOCUMENT1_VER_STATUS.name] is not None:
            updt["constants.misc_webargs.DOCUMENT1_VER_STATUS.name"] = args[
                constants.misc_webargs.DOCUMENT1_VER_STATUS.name]
        if constants.misc_webargs.DOCUMENT2_VER_STATUS.name in args and \
                args[constants.misc_webargs.DOCUMENT2_VER_STATUS.name] is not None:
            updt["constants.misc_webargs.DOCUMENT2_VER_STATUS.name"] = args[
                constants.misc_webargs.DOCUMENT2_VER_STATUS.name]
    elif role == constants.roles.AGENT.name:
        if constants.misc_webargs.TIMEZONE.name in args and args[constants.misc_webargs.TIMEZONE.name] is not None:
            updt["constants.misc_webargs.TIMEZONE.name"] = args[constants.misc_webargs.TIMEZONE.name]
    else:
        return False
    try:
        db.find_and_modify(constants.collectionName.users.name, expr, updt, False)
    except:
        return False
    return True
