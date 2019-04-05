from webargs import fields, validate, ValidationError
from backendAPI import constants

argsLogin = {

    ############### mandatory ######################

    constants.misc_webargs.USERNAME.name: fields.Str(
        required=True, validate=validate.Length(min=3)
    ),

    constants.misc_webargs.PASSWORD.name: fields.Str(
        required=True, validate=validate.Length(min=8)
    )
}


argsAddUser = {


    constants.misc_webargs.TOKEN.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.REFERRER.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.USERNAME.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.PASSWORD.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.ROLE.name:fields.Str(
        required=True
    )


}