from flask_restful import Resource
from webargs.flaskparser import use_args
from backendAPI import utils,args,auth,db,initial_setup
from backendAPI.constants import misc_webargs,roles

class Login(Resource):
    @use_args(args.argsLogin)
    def post(self, args):
        if auth.checkPassword(args[misc_webargs.USERNAME.name],args[misc_webargs.PASSWORD.name]):
            token = utils.id_generator()
            if auth.addToken(args[misc_webargs.USERNAME.name],token):
                return utils.generate_response(1,{"TOKEN":token})
        return utils.generate_response(0,"FAILURE")


#admins can create other admins and agents. customers can create themeselves but they need to have referring agent
#referrer token need to be set as dummy value for customers
class RegisterUser(Resource):
    @use_args(args.argsRegisterUser)
    def post(self,args):
        if args[misc_webargs.ROLE.name] == roles.ADMIN.name:
            if auth.checkTokenRole(args[misc_webargs.REFERRER_USERNAME.name], roles.ADMIN.name, args[misc_webargs.REFERRER_TOKEN.name]):
                if auth.addUser(args[misc_webargs.USERNAME.name], args[misc_webargs.PASSWORD.name], args[misc_webargs.ROLE.name],"",args[misc_webargs.TIMEZONE.name]):
                    return utils.generate_response(1,"SUCCESS")
        elif args[misc_webargs.ROLE.name] == roles.AGENT.name:
            if auth.checkTokenRole(args[misc_webargs.REFERRER_USERNAME.name], roles.ADMIN.name, args[misc_webargs.REFERRER_TOKEN.name]):
                if auth.addUser(args[misc_webargs.USERNAME.name], args[misc_webargs.PASSWORD.name], args[misc_webargs.ROLE.name],"",args[misc_webargs.TIMEZONE.name]):
                    return utils.generate_response(1, "SUCCESS")
        elif args[misc_webargs.ROLE.name] == roles.CUSTOMER.name:
            if auth.checkRoles(args[misc_webargs.REFERRER_USERNAME.name], roles.AGENT.name):
                if auth.addUser(args[misc_webargs.USERNAME.name], args[misc_webargs.PASSWORD.name], args[misc_webargs.ROLE.name], args[misc_webargs.REFERRER_USERNAME.name],args[misc_webargs.TIMEZONE.name]):
                    return utils.generate_response(1, "SUCCESS")

        return utils.generate_response(0, "FAILURE")


class ListUser(Resource):
    @use_args(args.argsListUser)
    def post(self, args):
        if auth.checkToken(args[misc_webargs.USERNAME.name], args[misc_webargs.TOKEN.name]):
            response = auth.getListOfUsers(args[misc_webargs.USERNAME.name])
            return response
        return utils.generate_response(0, "FAILURE")


class OneTimeSetup(Resource):
    def post(self):
        try:
            initial_setup.generateUsersUniqueIndex()
            initial_setup.generateSuperadmin()
            initial_setup.generateLoan1()
            initial_setup.generateLoanInventoryIndex()
            initial_setup.insertInitialCounterValue()
        except Exception as e:
            print(e)
            return utils.generate_response(0, "FAILURE")

        return utils.generate_response(0, "SUCCESS")


class ListLoans(Resource):
    def post(self):
        try:
            val = auth.listLoans()
        except:
            return utils.generate_response(0, "FAILURE")
        return utils.generate_response(1, val)


class CreateLoanRequest(Resource):

    @use_args(args.argsCreateLoanRequest)
    def post(self, args):
        try:
            if auth.checkTokenRole(args[misc_webargs.REFERRER_USERNAME.name], roles.AGENT.name,
                                   args[misc_webargs.REFERRER_TOKEN.name]):
                if auth.isCustomerAgentRelated(args[misc_webargs.REFERRER_USERNAME.name],
                                               args[misc_webargs.CUSTOMER_NAME.name]):
                    if auth.addLoan(args):
                        return utils.generate_response(1, "SUCCESS")
        except:
            return utils.generate_response(0, "FAILURE")
        return utils.generate_response(0, "FAILURE")


class ViewLoanRequest(Resource):

    @use_args(args.argsViewLoanRequest)
    def post(self, args):
        try:
            if auth.checkPassword(args[misc_webargs.USERNAME.name], args[misc_webargs.PASSWORD.name]):
                val = auth.viewLoansRequest(args[misc_webargs.USERNAME.name])
                return val
        except:
            return utils.generate_response(0, "FAILURE")
        return utils.generate_response(0, "FAILURE")


class EditLoanRequest(Resource):
    pass



