from flask_restful import Resource
from webargs.flaskparser import use_args
from backendAPI import utils,args,auth,db

class Login(Resource):

    @use_args(args.argsLogin)
    def post(self, args):
        password_retrieved = auth.general_auth_check_password_ci(args)
        token = utils.id_generator()
        # now create edit auth card to include new sessid
        if(db.edit_single_doc(sym.all_coll_names.auth.name,
                              {sym.auth_fields.AUTH_PCID.name: pcid},
                              {'$set': {sym.auth_fields.SESSID.name: sessid}})):
            # report back success with valid sessid and correct pcid, so that it can be saved there at the client
            #return util.generate_client_response(1, sessid)
            return utils.generate_login_response()
        else:
            return utils.generate_login_response(0)


class ADDUser(Resource):

    @use_args(args.argsAddUser)
    def post(self,args):
