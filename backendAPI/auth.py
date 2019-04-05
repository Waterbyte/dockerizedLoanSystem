
from backendAPI import utils,db,constants

def general_auth_check_password(args):
    username = args[constants.misc_webargs.USERNAME]
    num_docs = db.count_doc(constants.collectionName.user,
                            {sym.auth_fields.AUTH_PCID.name: {'$regex': util.generateExactMatchPattern(pcid), '$options': 'i'},
                             sym.auth_fields.PASSWORD.name: args[sym.misc_webargs.PASSKEY.name]
                            })
    if num_docs == 0:
        return
    else:
        return pcid
