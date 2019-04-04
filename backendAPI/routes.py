from flask_restful import Resource
from webargs.flaskparser import use_args


class Login(Resource):

    @use_args(args.argsRead)
    def post(self, args):
        pcid = auth.general_auth_check_password_ci(args)
        sessid = util.id_generator()
        # now create edit auth card to include new sessid
        if(db.edit_single_doc(sym.all_coll_names.auth.name,
                              {sym.auth_fields.AUTH_PCID.name: pcid},
                              {'$set': {sym.auth_fields.SESSID.name: sessid}})):
            # report back success with valid sessid and correct pcid, so that it can be saved there at the client
            #return util.generate_client_response(1, sessid)
            return util.generate_client_response(1, {sym.card_fields.PCID.name: pcid, sym.auth_fields.SESSID.name: sessid})
        else:
            return util.generate_client_response(0)