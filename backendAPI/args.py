from webargs import fields, validate, ValidationError

import backendAPI.auth
from backendAPI import constants, utils

argsLogin = {

    ############### mandatory ######################

    constants.misc_webargs.USERNAME.name: fields.Str(
        required=True, validate=validate.Length(min=1)
    ),

    constants.misc_webargs.PASSWORD.name: fields.Str(
        required=True, validate=validate.Length(min=8)
    )
}


argsAddUser = {

    constants.misc_webargs.USERNAME.name: fields.Str(
        required=True,validate=backendAPI.auth.username_must_not_exist_in_db
    ),
    constants.misc_webargs.PASSWORD.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.ROLE.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.REFERRER_TOKEN.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.REFERRER_USERNAME.name: fields.Str(
        required=True
    )



}