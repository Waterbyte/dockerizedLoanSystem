from flask_restful import Resource
from webargs.flaskparser import use_args
from backendAPI import utils,args,auth,db
from backendAPI.constants import misc_webargs,roles

class Login(Resource):
    @use_args(args.argsLogin)
    def post(self, args):
        if auth.checkPassword(args[misc_webargs.USERNAME.name],args[misc_webargs.PASSWORD.name]):
            token = utils.id_generator()
            if auth.addToken(args[misc_webargs.USERNAME.name],token):
                return utils.generate_response(1,token)
        return utils.generate_response(0,"FAILURE")


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



