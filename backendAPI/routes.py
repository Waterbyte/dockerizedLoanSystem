from flask_restful import Resource
from webargs.flaskparser import use_args
from backendAPI import utils,args,auth,db
from backendAPI.constants import misc_webargs,roles

# class Login(Resource):
#
#     @use_args(args.argsLogin)
#     def post(self, args):
#         password_retrieved = auth.general_auth_check_password_ci(args)
#         token = utils.id_generator()
#         # now create edit auth card to include new sessid
#         if(db.edit_single_doc(sym.all_coll_names.auth.name,
#                               {sym.auth_fields.AUTH_PCID.name: pcid},
#                               {'$set': {sym.auth_fields.SESSID.name: sessid}})):
#             # report back success with valid sessid and correct pcid, so that it can be saved there at the client
#             #return util.generate_client_response(1, sessid)
#             return utils.generate_login_response()
#         else:
#             return utils.generate_login_response(0)



#admins can create other admins and agents. customers can create themeselves but they need to have referring agent
#referrer token need to be set as dummy value for customers
class ADDUser(Resource):

    @use_args(args.argsAddUser)
    def post(self,args):
        if args[misc_webargs.ROLE.name] == roles.ADMIN.name:
            if auth.checkTokenRole(args[misc_webargs.REFERRER_USERNAME.name], roles.ADMIN.name, args[misc_webargs.REFERRER_TOKEN.name]):
                if auth.addUser(args[misc_webargs.USERNAME.name], args[misc_webargs.PASSWORD.name], args[misc_webargs.ROLE.name]):
                    return utils.generate_response(1,"SUCCESS")
        elif args[misc_webargs.ROLE.name] == roles.AGENT.name:
            if auth.checkTokenRole(args[misc_webargs.REFERRER_USERNAME.name], roles.ADMIN.name, args[misc_webargs.REFERRER_TOKEN.name]):
                if auth.addUser(args[misc_webargs.USERNAME.name], args[misc_webargs.PASSWORD.name], args[misc_webargs.ROLE.name]):
                    return utils.generate_response(1, "SUCCESS")
        elif args[misc_webargs.ROLE.name] == roles.CUSTOMER.name:
            if auth.checkRoles(args[misc_webargs.REFERRER_USERNAME.name], roles.AGENT.name):
                if auth.addUser(args[misc_webargs.USERNAME.name], args[misc_webargs.PASSWORD.name], args[misc_webargs.ROLE.name], args[misc_webargs.REFERRER_USERNAME.name]):
                    return utils.generate_response(1, "SUCCESS")

        return utils.generate_response(0,"FAILURE")



