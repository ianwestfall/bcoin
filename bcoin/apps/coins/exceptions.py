from rest_framework.exceptions import APIException


class WalletNotFoundException(APIException):
    status_code = 404
    default_detail = "Wallet not found"
    defalt_code = "wallet_not_found"


class YouTooBrokeException(APIException):
    status_code = 409
    default_detail = "You too broke"
    default_code = "you_too_broke"


class InvalidAmountException(APIException):
    status_code = 400
    default_detail = "Oh you think you slick tryna send negative amounts tf outta here with that bullshit"
    default_code = "invalid_amount"
