import enum


class AuthenticationMethod(enum.Enum):
    acceptance = 'acceptance'
    device = 'device'
    facial = 'facial'


AUTHENTICATION_METHODS = [e for e in AuthenticationMethod]