import logging

from datetime import timedelta

from zope.interface import implementer

from ...crypto import make_signature, SignatureError, validate_signature


logger = logging.getLogger(__name__)

try:
    # ICSRFStoragePolicy was not added to Pyramid until version 1.9
    from pyramid.interfaces import ICSRFStoragePolicy  # pylint: disable=no-name-in-module
except ImportError:
    logger.error(
        "baseplate.integration.pyramid.csrf requires that you use a version "
        "of pyramid >= 1.9"
    )
    raise


def _make_csrf_token_payload(version, account_id):
    version = str(version)
    payload = ".".join([version, account_id])
    return version, payload


@implementer(ICSRFStoragePolicy)
class TokenCSRFStoragePolicy(object):
    """ICSRFStoragePolicy implementation for Intranet Services.

    This implementation of Pyramid's ICSRFStoragePolicy interface takes
    advantage of intranet authentication being handled outside individual
    applications and validates CSRF tokens without storing anything at all.
    It works by using a secret value to make HMAC CSRF tokens that are
    scoped to individual users.

    This policy relies on Pyramid's built in Authentication Policies since it
    uses `request.authenticated_userid`.  For a simple, intranet app, you can
    rely on the HTTP "Authorized-User" header to pass you this value and you
    can configure Pyramid to use that with the following snippet:

        authn_policy = RemoteUserAuthenticationPolicy(environ_key="HTTP_AUTHENTICATED_USER")
        authz_policy = ACLAuthorizationPolicy()
        configurator.set_authentication_policy(authn_policy)
        configurator.set_authorization_policy(authz_policy)

    You can add this form of CSRF protection to your baseplate Pyramid app
    by adding the following code to your `make_wsgi_app` function:

        configurator.set_csrf_storage_policy(TokenCSRFStoragePolicy(
            secrets=secrets,
            secret_path='secret/path/to/csrf-secret',
        ))
        configurator.set_default_csrf_options(require_csrf=True)

    You will also need to pass a new CSRF token to your client each time you
    render a form for them.  You should not re-use CSRF tokens when using this
    StoragePolicy since these tokens expire and are difficult to selectively
    invalidate.

    :param baseplate.secrets.store.SecretsStore secrets: A SecretsStore
        that contains the secret you will use to sign the CSRF token.
    :param str secret_path: The key to the secret in the supplied
        SecretsStore
    :param string param: (Optional) The name of the parameter to get the
        CSRF token from on a request.  The default is 'csrf_token'.
    :param datetime.timedelta max_age: (Optional) The maximum age that the
        signature portion of the CSRF token is valid.  The default value is
        one hour.
    """

    VERSION = 1

    def __init__(self, secrets, secret_path, param="csrf_token",
                 max_age=timedelta(hours=1)):
        self._secrets = secrets
        self._secret_path = secret_path
        self._param = param
        self._max_age = max_age

    def _get_secret(self):
        return self._secrets.get_versioned(self._secret_path)

    def new_csrf_token(self, request):
        """Return a new CSRF token.

        You will need to call `pyramid.csrf.new_csrf_token` to get a new
        CSRF token when rendering forms, you should not re-use CSRF tokens
        when using this StoragePolicy since these tokens expire and are
        difficult to selectively invalidate.
        """
        prefix, payload = _make_csrf_token_payload(
            version=self.VERSION,
            account_id=request.authenticated_userid,
        )
        signature = make_signature(self._get_secret(), payload, self._max_age)
        return ".".join([prefix, signature.decode("utf-8")])

    def get_csrf_token(self, request):
        """Return the currently active CSRF token from the request params.

        This will not generate a new one if none is supplied like some of
        the default ones in Pyramid do.

        This is called automatically by Pyramid if you have configured it
        to require CSRF.
        """
        return request.params.get(self._param)

    def check_csrf_token(self, request, supplied_token):
        """Return True if the supplied_token is valid.

        This is called automatically by Pyramid if you have configured it
        to require CSRF.
        """
        try:
            token_version, sep, signature = supplied_token.partition(".")
        except Exception:
            return False

        if sep != ".":
            return False

        _, payload = _make_csrf_token_payload(
            version=token_version,
            account_id=request.authenticated_userid,
        )

        try:
            validate_signature(self._get_secret(), payload, signature)
        except SignatureError:
            return False

        return True
