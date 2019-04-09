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


argsRegisterUser = {
    constants.misc_webargs.USERNAME.name: fields.Str(
        required=True, validate=backendAPI.auth.username_must_not_exist_in_db
    ),
    constants.misc_webargs.PASSWORD.name: fields.Str(
        required=True, validate=validate.Length(min=8)
    ),
    constants.misc_webargs.ROLE.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.REFERRER_TOKEN.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.REFERRER_USERNAME.name: fields.Str(
        required=True
    ),
    constants.misc_webargs.TIMEZONE.name: fields.Str(
        required=True,validate=utils.validate_timezone
    )
}

argsListUser = {
constants.misc_webargs.USERNAME.name: fields.Str(
        required=True, validate=validate.Length(min=1)
    ),
    constants.misc_webargs.TOKEN.name: fields.Str(
        required=True
    )
}

argsCreateLoanRequest = {
    constants.misc_webargs.REFERRER_USERNAME.name:fields.Str(
        required = True, validate=validate.Length(min=1)
    ),
    constants.misc_webargs.REFERRER_TOKEN.name:fields.Str(
        required = True
    ),
    constants.misc_webargs.CUSTOMER_NAME.name:fields.Str(
        required = True
    ),
    constants.loanCust.LOAN_INVT_ID.name:fields.Str(
        required = True
    ),
    constants.loanCust.AMT.name:fields.Str(
        required = True
    ),
    constants.loanCust.DURATION.name:fields.Str(
        required = True
    ),
    constants.loanCust.MANDATORY_REQUIREMENT1_LOC.name:fields.Str(
        required = True
    ),
    constants.loanCust.MANDATORY_REQUIREMENT2_LOC.name:fields.Str(
        required = True
    ),
    constants.loanCust.EMI_CHOSEN.name:fields.Bool(
        required = True
    )

}

argsViewLoanRequest = argsLogin