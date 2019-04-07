from backendAPI import utils, db, constants
from backendAPI.utils import generateExactMatchPattern

def generateLoan1():
    loanTypeDoc = {
        "Id":"",
        "Name":""


    }
    db.insert_one_doc(constants.collectionName.loan_inventory.name,loanTypeDoc)