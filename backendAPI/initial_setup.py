from backendAPI import utils, db
from backendAPI.utils import generateExactMatchPattern
from backendAPI.constants import loanInv, DocumentType,collectionName,misc_webargs
import pymongo

def generateLoan1():
    loanTypeDoc = {
        loanInv.ID.name: "1",
        loanInv.NAME.name: "Eagle Premium Loan",
        loanInv.DESC.name: "Eagle premium loan service is designed by our bank for private sector individuals wanting quick loans without much hassle.",
        loanInv.MIN_AMT.name: "50000", # rs
        loanInv.MAX_AMT.name: "1000000",   # rs
        loanInv.MIN_DURATION.name: "12",    # months
        loanInv.MAX_DURATION.name: "60",    # months
        loanInv.INTERESTRATE.name: "15",
        loanInv.MANDATORY_REQUIREMENT1.name:DocumentType.PAN_CARD.name,
        loanInv.MANDATORY_REQUIREMENT2.name:DocumentType.SALARY_SLIP.name,
        loanInv.EMI_AVAILABLE.name: "yes",
        loanInv.PREPAYMENT_AVAILABLE.name: "yes",
        loanInv.PREPAYMENT_CHARGES.name: "0",
        loanInv.LOAN_PROCESSING_CHARGES.name: "2",  # percentage
        loanInv.EXTRA_ONE_TIME_CHARGES.name: "500",
        loanInv.MINIMUM_CREDIT_SCORE.name: "750",
        loanInv.MINIMUM_ANNUAL_INCOME_LOANEE.name: "240000",     # rs
        loanInv.MINIMUM_MONTHLY_INCOME_LOANEE.name: "20000",     # rs
        loanInv.IS_REDUCING_RATE_OF_INTEREST.name: "True",
        misc_webargs.TIMESTAMP.name:utils.generate_current_utc()  #for analytics purpose
    }
    return db.insert_one_doc(collectionName.loan_inventory.name,loanTypeDoc)

def generateLoanInventoryIndex():
    expr = [('ID',pymongo.ASCENDING)]
    uniqueKey = True
    return db.create_index(collectionName.loan_inventory.name,expr,uniqueKey)

def generateSuperadmin():
    superadmindoc = {

    }
    return db.insert_one_doc(collectionName.users.name,superadmindoc)