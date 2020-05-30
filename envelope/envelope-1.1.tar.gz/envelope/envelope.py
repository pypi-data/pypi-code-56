#!/usr/bin/env python3

import logging
import re
import smtplib
import subprocess
import sys
import tempfile
import warnings
from configparser import ConfigParser
from copy import copy, deepcopy
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import make_msgid, formatdate, getaddresses
from getpass import getpass
from pathlib import Path
from typing import Union

from .utils import AutoSubmittedHeader, SMTP, is_gpg_fingerprint, assure_list, assure_fetched

try:
    import gnupg
except ImportError:
    gnupg = None
import magic

__doc__ = """


Quick layer python-gnupg, smime, smtplib and email handling packages.
Their common usecases merged into a single function. Want to sign a text and tired of forgetting how to do it right?
You do not need to know everything about GPG or S/MIME, you do not have to bother with importing keys.
Do not hassle with reconnecting SMTP server. Do not study various headers meanings to let your users unsubscribe via a URL.
You insert a message and attachments and receive signed and/or encrypted output to the file or to your recipients' e-mail. 
Just single line of code. With the great help of the examples below.

Usage:
  * launch as application, see ./envelope.py --help
  * import as a module to your application, ex: `from envelope import Envelope` 

Example:

gpg(message="Hello world",
        output="/tmp/output_file",
        encrypt_file="/tmp/remote_key.asc",
        sender="me@email.com",
        to="remote_person@example.com")
"""

logger = logging.getLogger(__name__)
CRLF = '\r\n'
AUTO = "auto"


class Envelope:
    default: 'Envelope'

    _gnupg: gnupg.GPG

    def __bool__(self):
        return self._status

    def __str__(self):
        if self._result_cache_hash and self._result_cache_hash != self._param_hash():
            # ex: if we change Subject, we have to regenerate self._result
            self._result.clear()
        if not self._result:
            if self._encrypt or self._sign:
                # if subject is not set, we suppose this is just a data blob to be encrypted, no an e-mail message
                # and a ciphered blob will get output. However if subject is set, we put send="test"
                # in order to display all e-mail headers etc.
                is_email = "test" if bool(self._subject) else False
                self._start(send=is_email)
            else:
                # nothing to do, let's assume this is a bone of an e-mail by appending `--send False` flag to produce an output
                self._start(send="test")
        return self._get_result()

    def __repr__(self):
        """
        :return: Prints out basic representation.
            However this is not serialization, you cannot reconstruct any complicated objects having attachments or custom headers.
        """
        l = []
        quote = lambda x: '"' + x.replace('"', r'\"') + '"' if type(x) is str else x
        [l.append(f'{k}={quote(v)}') for k, v in {"subject": self._subject,
                                                  "from_": self._from,
                                                  "to": self._to,
                                                  "cc": self._cc,
                                                  "bcc": self._bcc,
                                                  "reply-to": self._reply_to,
                                                  "message": self._message}.items() if v]

        if not l:
            return super().__repr__()
        return f"Envelope({', '.join(l)})"

    def __bytes__(self):
        if not self._result:
            str(self)
        return assure_fetched(self._get_result(), bytes)

    def __eq__(self, other):
        if not self._result:
            str(self)
        if type(other) in [str, bytes]:
            return assure_fetched(self._get_result(), bytes) == assure_fetched(other, bytes)

    def preview(self):
        """ Returns the string of the message or data with the readable text.
            Bcc and attachments are mentioned.
            Ex: whilst we have to use quoted-printable (as seen in __str__), here the output will be plain text.

        # XX is ciphering info seen?
        # XX might be available from CLI too
        """
        if not self._result:
            str(self)
        result = []

        for a in self._attachments:  # include attachments info as they are removed with the payload later
            result.append("Attachment: " + ", ".join(str(s) for s in a))

        if self._bcc:  # as bcc is not included as an e-mail header, we explicitly states it here
            result.append("Bcc: " + ", ".join(self._bcc))

        for i, r in enumerate(self._result):
            if isinstance(r, EmailMessage):
                # remove body from the message because it may have become unreadable
                # I cannot use r.set_payload(""), since it would change the headers like Content-Transfer-Encoding
                for line in r.as_string().splitlines():
                    result.append(line)
                    if not line.strip():
                        break
                continue
            result.append(r)

        result.append(self._message)

        return "\n".join(result)

    def _get_result(self):
        """ concatenate output string """
        if not self._result_cache:
            s = "\n".join(str(r) for r in self._result)
            self._result_cache = s  # slightly quicker next time if ever containing a huge amount of lines
        return self._result_cache

    @staticmethod
    def load(message, *, path=None):
        """ This is still an experimental function.
        XX make it capable to decrypt and verify signatures?
        XX make it capable to read an "attachment" - now it's a mere part of the body
        XX Allow message decoding so that you can write `envelope --load mail.eml  --message` to read message contents
            that is garbled normally in BASE64 etc.
        XX should be able to load Subject even if it is on a multiline.
            Envelope.load("Subject: Very long text Very long text Very long text Very long text Very long text") will print out
                Subject:
                    Very long text Very long text Very long text Very long text Very long text

        Note that if you will send this reconstructed message, you might not probably receive it due to the Message-ID duplication.
        Delete at least Message-ID header prior to re-sending.

        :param message: Any attainable contents to build an Envelope object from.
        :param path: Path to the file that should be loaded.
        """
        if path:
            message = Path(path)

        header_row = re.compile(r"([^\t:]+):(.*)")
        text = assure_fetched(message)
        is_header = True
        header = []
        body = []
        for line in text.splitlines():
            if is_header:  # we are parsing e-mail template header first
                # are we still parsing the header?
                m = header_row.match(line)
                if m:
                    header.append([line, m.group(1).strip(), m.group(2).strip()])
                    continue
                else:
                    if line.startswith("\t") and header:  # this is not end of header, just line continuation
                        header[-1][0] += " " + line.strip()
                        header[-1][2] += " " + line.strip()
                        continue
                    is_header = False
                    if line.strip() == "":  # next line will be body
                        continue
                    else:  # header is missing or incorrect, there is body only
                        body = [l[0] for l in header]
                        header = []
            if not is_header:
                body.append(line)

        e = Envelope().message(CRLF.join(body))
        for _, key, val in header:
            e.header(key, val)
        return e

    def __init__(self, message=None, from_=None, to=None, subject=None, headers=None,
                 gpg=None, smime=None,
                 encrypt=None, sign=None, passphrase=None, attach_key=None, cert=None,
                 sender=None, cc=None, bcc=None, reply_to=None, mime=None, attachments=None,
                 smtp=None, output=None, send=None):
        """
        :rtype: object If output not set, return output bytes, else True/False if output file was correctly written to.

        Any attainable contents means plain text, bytes or stream (ex: from open()).
        In *module interface*, you may use Path object to the file.
        In *CLI interface*, additional flags are provided.

        Output
        :param message: Any attainable contents.
        :param output: Path to file to be written to (else the contents is returned).
        :param gpg: Home folder of GNUPG rings else default ~/.gnupg is used. Put True for prefer GPG over S/MIME.
        :param smime: Prefer S/MIME over GPG.

        Signing
        :param sign: True or key id if the message is to be signed. S/MIME certificate key or Path or stream (ex: from open()).
        :param passphrase: If signing key needs passphrase.
        :param attach_key: If True, public key is appended as an attachment.
        :param cert: S/MIME certificate contents or Path or stream (ex: from open()) if certificate not included in the key.

        Encrypting
        :param encrypt: Recipients public key string or Path or stream (ex: from open()).
        :param to: E-mail or list. If encrypting used so that we choose the key they will be able to decipher with.
        :param from_: E-mail of the sender. If encrypting used so that we choose our key to be still able
                        to decipher the message later with.
                        If False, we explicitly declare to give up on deciphering later.

        Input / Sending
        :param subject: E-mail subject
        :param reply_to: Reply to header
        :param mime: Set contents mime subtype: "html" (default) or "plain" for plain text
        :param smtp: tuple or dict of these optional parameters: host, port, username, password, security ("tlsstart").
            Or link to existing INI file with the SMTP section.
        :param send: True for sending the mail. False will just print the output.
        :param cc: E-mail or their list.
        :param bcc: E-mail or their list.
        :param attachments: Attachment or their list. Attachment is defined by file path or stream (ex: from open()),
            optionally in tuple with the file name in the e-mail and/or mimetype.
        :param headers: List of headers which are tuples of name, value. Ex: [("X-Mailer", "my-cool-application"), ...]
        :param sender: Alias for "from" if not set. Otherwise appends header "Sender".
        """
        # user defined variables
        self._message = None  # bytes
        self._output = None
        self._gpg: Union[str, bool] = None
        self._sign = None
        self._passphrase = None
        self._attach_key = None
        self._cert = None
        self._encrypt = None
        self._from = self.__from = None
        self._sender = self.__sender = None
        self._to = []
        self._cc = []
        self._bcc = []
        self._reply_to = []
        self._subject = None  # string
        self._smtp = None
        self._attachments = []
        self._mime = AUTO
        self._nl2br = AUTO
        self._headers = EmailMessage()  # object for storing headers the most standard way possible
        self._ignore_date = False

        # variables defined while processing
        self._status = False  # whether we successfully encrypted/signed/send
        self._processed = False  # prevent the user from mistakenly call .sign().send() instead of .signature().send()
        self._result = []  # text output for str() conversion
        self._result_cache = None
        self._result_cache_hash = None
        self._smtp = SMTP()
        self.auto_submitted = AutoSubmittedHeader(self)  # allows fluent interface to set header

        # if a parameter is not set, use class defaults, else init with parameter
        self._populate(locals())

        if sign or encrypt or send is not None:
            self._start(send=send)

    @staticmethod
    def _get_private_var(k):
        """ Gets internal specific interface var name from its method name. """
        if k == "from_":
            k = "from"
        return "_" + k

    def _populate(self, params):
        for k, v in params.items():
            if k in ["self", "send"]:
                continue
            elif k == "smime":  # smime uses _gpg, not _smime because it needs no parameter
                if v is True:
                    self.smime()
                continue
            elif v is None:
                if not hasattr(self, "default"):
                    continue
                v = copy(getattr(self.default, self._get_private_var(k)))  # ex `v = copy(self.default._message)`
                if v is None:
                    continue

            if k == "passphrase":
                self.signature(passphrase=v)
            elif k == "attach_key":
                if v is True:
                    self.signature(attach_key=v)
            elif k == "cert":
                self.signature(None, cert=v)
            elif k == "to":
                self.to(v)
            elif k == "attachments":
                self.attach(v)
            elif k == "headers":  # [(header-name, val), ...]
                for it in v:
                    self.header(*it)
            elif k == "sign":
                self.signature(v)
            elif k == "encrypt":
                self.encryption(v)
            elif v is not None:
                getattr(self, k)(v)  # ex: self.message(message)

        self._prepare_from()
        return self

    def copy(self):
        """ Returns deep copy of the object. """
        return deepcopy(self)

    def cc(self, email_or_list=None):
        if email_or_list is None:
            return self._cc
        self._cc += assure_list(email_or_list)
        return self

    def bcc(self, email_or_list=None):
        if email_or_list is None:
            return self._bcc
        self._bcc += assure_list(email_or_list)
        return self

    def reply_to(self, email_or_list=None):
        if email_or_list is None:
            return self._reply_to
        self._reply_to += assure_list(email_or_list)
        return self

    def body(self, text=None, *, path=None):
        """ An alias of .message """
        return self.message(text=text, path=path)

    def text(self, text=None, *, path=None):
        """ An alias of .message """
        return self.message(text=text, path=path)

    def message(self, text=None, *, path=None):
        """ Message to be ciphered / e-mail body text. """
        if text is path is None:
            return self._message
        if path:
            text = Path(path)
        self._message = text
        return self

    def date(self, date):
        """
        Specify Date header. If not used, Date will be added automatically.
        :param date: str|False If False, the Date header will not be added automatically.
        """
        if date is False:
            if "Date" in self._headers:  # removes date header
                del self._headers["Date"]
            self._ignore_date = True
        else:
            self._ignore_date = False
            self.header("Date", date)
        return self

    def sender(self, email=None):
        """  Alias for "from" if not set. Otherwise appends header "Sender". """
        if email is None:  # XX doc me
            return self.__sender
        self._sender = email
        self._prepare_from()
        return self

    def from_(self, email=None):
        if email is None:
            return self.__from
        self._from = email
        self._prepare_from()
        return self

    def output(self, output_file):
        self._output = output_file
        return self

    def gpg(self, gnugp_home=True):
        """
        :param gnugp_home: String for GnuPG home or True.
        """
        self._gpg = gnugp_home
        return self

    def smime(self):
        self._gpg = False
        return self

    def subject(self, subject=None):
        if subject is None:
            return self._subject
        self._subject = subject
        return self

    def mime(self, subtype=AUTO, nl2br=AUTO):
        """
        Ignored if `Content-Type` header put to the message.
        @type subtype: str Set contents mime subtype: "auto" (default), "html" or "plain" for plain text.
        @param nl2br: True: envelope will append `<br>` to every line break in the HTML message.
                      "auto": line breaks are changed only if there is no `<br` or `<p` in the HTML message,
        """
        self._mime = subtype
        self._nl2br = nl2br
        return self

    def list_unsubscribe(self, uri=None, one_click=False, *, web=None, email=None):
        """ The header will not be encrypted with GPG nor S/MIME.
        :param uri: Web or e-mail address.
            We try to determine whether this is e-mail and prepend brackets and 'https:'/'mailto:' if needed
            Ex: "me@example.com?subject=unsubscribe", "example.com/unsubscribe", "<https://example.com/unsubscribe>"
        :param one_click: If True, rfc8058 List-Unsubscribe-Post header is added.
            This says user can unsubscribe with a single click that is realized by a POST request
            in order to prevent e-mail scanner to access the unsubscribe page by mistake. A 'https' url must be present.
        :param web: URL. Ex: "example.com/unsubscribe", "http://example.com/unsubscribe"
        :param email: E-mail address. Ex: "me@example.com", "mailto:me@example.com"
        :return: self
        """

        elements = []
        if "List-Unsubscribe" in self._headers:
            elements.extend(self._headers["List-Unsubscribe"].split(","))

        if one_click:
            self.header("List-Unsubscribe-Post", "List-Unsubscribe=One-Click")
            if uri and not web:  # we are sure this is web because one-click header does not go with an e-mail
                web = uri
                uri = None

        if uri.startswith("<"):
            elements.append(uri)
        elif uri.startswith(("http:", "https:", "mailto:", "//")):
            elements.append(f"<{uri}>")
        elif "@" in uri:
            elements.append(f"<mailto:{uri}>")
        else:
            elements.append(f"<https://{uri}>")

        if web:
            if uri.startswith(("http:", "https:", "//")):
                elements.append(f"<{web}>")
            else:
                elements.append(f"<https://{web}>")

        if email:
            if uri.startswith("mailto:"):
                elements.append(f"<{email}>")
            else:
                elements.append(f"<mailto:{email}>")

        self.header("List-Unsubscribe", ", ".join(elements), replace=True)
        return self

    auto_submitted: AutoSubmittedHeader

    def header(self, key, val=None, replace=False):
        """ Add a generic header.
        The header will not be encrypted with GPG nor S/MIME.
        :param key: str Header name
        :param val: str Header value. If None, currently used value is returned.
        :param replace: bool If True, any header of the `key` name are removed first and if `val` is None, the header is deleted.
                        Otherwise another header of the same name is appended.
        :return: Envelope|str|list Returned self if `val` is not None or replace=True, else returns value of the header
                 or its list if the header was used multiple times. (Note that cc and bcc headers always return list.)
        """

        # lowercase header to its method name
        specific_interface = {"to": self.to, "cc": self.cc, "bcc": self.bcc, "reply_to": self.reply_to,
                              "from": self.from_, "sender": self.sender,
                              "subject": self.subject
                              }

        k = key.lower()
        if k in specific_interface:
            if replace:
                attr = getattr(self, self._get_private_var(k))
                setattr(self, self._get_private_var(k), None if type(attr) is str else [])
                if k in ("sender", "from"):
                    self._prepare_from()
                return self
            return specific_interface[k](val)

        if replace:
            del self._headers[key]
        if val is None and not replace:
            h = self._headers.get_all(key)
            if h and len(h) == 1:
                return h[0]
            return h
        elif val:
            self._headers[key] = val
        return self

    def smtp(self, host="localhost", port=25, user=None, password=None, security=None):
        """
        Obtain SMTP server connection.
        Note that you may safely call this in a loop,
            envelope will remember the settings and connect only once (without reconnecting every iteration).
        :param host: hostname, smtplib.SMTP or INI file path.
        :param port:
        :param user:
        :param password:
        :param security: Ex: tlsstart
        :return:
        """
        # CLI interface returns always a list or dict, ex: host=["localhost"] or host=["ini file"] or host={}
        # module one-liner interface fills host param, ex: host="localhost", host="ini file", host={"port": 123}, ["localhost", 123]
        # fluent interface fills all locals, ex: {"host": "ini file", "port": default 25}
        # check for the presence of an INI file
        ini = None
        if type(host) is str:
            ini = host
        elif type(host) is list and len(host) > 0:
            ini = host[0]
        elif type(host) is dict and "host" in host:
            ini = host["host"]

        if ini and ini.endswith("ini"):
            if not Path(ini).exists() and not Path(ini).is_absolute():
                # when imported as a library, the relative path to the ini file might point to the main program directory
                ini = Path(Path(sys.argv[0]).parent, ini)

            if Path(ini).exists():  # existing INI file
                config = ConfigParser()
                config.read(ini)
                try:
                    host = {k: v for k, v in config["SMTP"].items()}
                except KeyError as e:
                    raise FileNotFoundError(f"INI file {ini} exists but section [SMTP] is missing") from e

        if type(host) is dict:  # ex: {"host": "localhost", "port": 1234}
            self._smtp = SMTP(**host)
        elif type(host) is list:  # ex: ["localhost", 1234]
            self._smtp = SMTP(*host)
        elif isinstance(host, smtplib.SMTP):
            self._smtp = SMTP(host)
        else:
            self._smtp = SMTP(host, port, user, password, security)
        return self

    def to(self, email_or_list=None):
        if email_or_list is None:
            return self._to
        self._to += assure_list(email_or_list)
        return self

    def attach(self, attachment=None, mimetype=None, filename=None, *, path=None):
        """

        :type attachment: Any attainable contents that should be added as an attachment or their list.
                The list may contain tuples: `any_attainable_contents [,mime type] [,file name]`.
        :param mimetype: Mime type OR file name of the attachment.
        :param filename: Mime type OR file name of the attachment.
        :param path: Path to the file that should be attached.
        """
        if type(attachment) is list:
            if path or mimetype or filename:
                raise ValueError("Cannot specify both path, mimetype or filename and put list in attachment_or_list.")
        else:
            if path:
                attachment = Path(path)
            attachment = attachment, mimetype, filename
        self._attachments += assure_list(attachment)
        return self

    def signature(self, key=True, passphrase=None, attach_key=None, cert=None, *, key_path=None):
        """
        Turn signing on.
        :param key: Signing key
            * GPG:
                * True (blank) for user default key
                * key ID/fingerprint
                * Any attainable contents with the key to be signed with (will be imported into keyring)
                * "auto" for turning on signing if there is a key matching to the "from" header
            * S/MIME: Any attainable contents with key to be signed with. May contain signing certificate as well.
        :param passphrase: Passphrase to the key if needed.
        :param attach_key: GPG: Append public key to the attachments when sending.
        :param cert: S/MIME: Any attainable contents with certificate to be signed with.
        :param key_path: Path to a file with the `key`.
        """
        if key_path:
            key = Path(key_path)
        if key is True and self._sign not in [None, False]:
            # usecase envelope().signature(key=fingerprint).send(sign=True) should still have fingerprint in self._sign
            # (and not just "True")
            pass
        elif key is not None:
            # GPG: True, AUTO, fingerprint, or attainable contents, S/MIME: attainable bytes
            self._sign = key
        if passphrase is not None:
            self._passphrase = passphrase
        if attach_key is not None:
            self._attach_key = attach_key
        if cert is not None:
            if self._gpg is None:  # since cert is only for S/MIME, set S/MIME signing
                self.smime()
                self._gpg = False
            self._cert = assure_fetched(cert, bytes)
        return self

    def sign(self, key=True, passphrase=None, attach_key=False, cert=None, *, key_path=None):
        """
        Sign now.
        :param key: Signing key
            * GPG:
                * True (blank) for user default key
                * key ID/fingerprint
                * Any attainable contents with the key to be signed with (will be imported into keyring)
                * "auto" for turning on signing if there is a key matching to the "from" header
            * S/MIME: Any attainable contents with key to be signed with. May contain signing certificate as well.
        :param passphrase: Passphrase to the key if needed.
        :param attach_key: GPG: Append public key to the attachments when sending.
        :param cert: S/MIME: Any attainable contents with certificate to be signed with.
        :param key_path: Path to a file with the `key`.
        """
        self._processed = True
        self.signature(key=key, passphrase=passphrase, attach_key=attach_key, cert=cert, key_path=key_path)
        self._start()
        return self

    def encryption(self, key=True, *, key_path=None):
        """
        Turn encrypting on.
        :param key:
            * GPG:
                * True (blank) for user default key
                * key ID/fingerprint
                * Any attainable contents with the key to be signed with (will be imported into keyring)
                * "auto" for turning on encrypting if there is a matching key for every recipient
            * S/MIME any attainable contents with certificate to be encrypted with or their list
        :param key_path: Path to a file with the `key` or their list.
        """
        if key_path:
            if type(key_path) is list:
                key = [Path(k) for k in key_path]
            else:
                key = Path(key_path)
        if key is True and self._encrypt not in [None, False]:
            # usecase envelope().encrypt(key="keystring").send(encrypt=True) should still have key in self._encrypt
            # (and not just "True")
            pass
        elif key is not None:
            self._encrypt = key
        return self

    def encrypt(self, key=True, sign=None, *, key_path=None):
        """
        Encrypt now.
        :param key:
            * GPG:
                * True (blank) for user default key
                * key ID/fingerprint
                * Any attainable contents with the key to be signed with (will be imported into keyring)
                * "auto" for turning on encrypting if there is a matching key for every recipient
            * S/MIME any attainable contents with certificate to be encrypted with or their list
        :param sign: Turn signing on.
            * GPG: True or default signing key ID/fingerprint.
            * S/MIME: Any attainable contents having the key + signing certificate combined in a single file.
              (If not in a single file, use .signature() method.)
        :param key_path: Path to a file with the `key` or their list.
        """
        self._processed = True
        self.encryption(key=key, key_path=key_path)
        self._start(sign=sign)
        return self

    def send(self, send=True, sign=None, encrypt=None):
        """
        Send e-mail contents. To check e-mail was successfully sent, cast the returned object to bool.
        :param send: True to send now, False to print debug information.
        :param sign: Turn signing on.
            * GPG: True or default signing key ID/fingerprint.
            * S/MIME: Any attainable contents having the key + signing certificate combined in a single file.
              (If not in a single file, use .signature() method.)
        :param encrypt: Any attainable contents with recipient GPG public key or S/MIME certificate to be encrypted with.
        :return:
        """
        if self._processed:
            raise RuntimeError("Cannot call .send() after .sign()/.encrypt()."
                               " You probably wanted to use .signature()/.encryption() instead.")
        self._start(sign=sign, encrypt=encrypt, send=send)
        return self

    def _prepare_from(self):
        """ Prepare private variables. Resolve "from" and "sender" headers.

        Due to a keyword clash we cannot use "from" as a method name and it seems convenient then to allow users
        to use sender instead. However we do not want to block setting "Sender" header too – since sender is a real header,
        we should somehow distinguish 'sender' from 'from'.
        Pity that 'from' is a reserved keyword, "from_" looks bad.
        """
        if self._from is None and self._sender is not None:
            self.__from = self._sender
            self.__sender = None
        else:
            self.__from = self._from
            self.__sender = self._sender

    def _start(self, sign=None, encrypt=None, send=None):
        """ Start processing. Either sign, encrypt or send the message and possibly set bool status of the object to True.
        * send == "test" is the same as send == False but the message "have not been sent" will not be produced
        """
        self._status = False
        if sign is not None:
            self.signature(sign)
        if encrypt is not None:
            self.encryption(encrypt)

        # sign:
        #   GPG: (True, key contents, fingerprint, AUTO, None) → will be converted to key fingerprint or None,
        #   SMIME: certificate contents
        sign = self._sign
        # encrypt:
        #   GPG: (True, key contents, fingerprint, None)
        #   SMIME: certificate contents
        encrypt = self._encrypt
        if sign is None and encrypt is None and send is None:  # check if there is something to do
            logger.warning("There is nothing to do – no signing, no encrypting, no sending.")
            return

        # assure streams are fetched and files are read from their paths
        data = assure_fetched(self._message, bytes)
        # we need a message
        if data is None:
            logger.error("Missing message")
            return

        # determine if we are using gpg or smime
        gpg_on = None
        if encrypt or sign:
            if self._gpg is not None:
                gpg_on = bool(self._gpg)
            else:
                gpg_on = True

            if gpg_on:
                self._gnupg = gnupg.GPG(gnupghome=self._get_gnupg_home(), options=["--trust-model=always"],
                                        # XX trust model might be optional
                                        verbose=False) if sign or encrypt else None
                # assure `sign` become either fingerprint of an imported key or None
                if sign:
                    if sign in [True, AUTO]:  # try to determine sign based on the "From" header
                        fallback_sign = sign = None
                        try:
                            address_searched = getaddresses([self.__from])[0][1]
                        except (TypeError, IndexError):
                            # there is no "From" header and no default key is given, pick the first secret as a default
                            for key in self._gnupg.list_keys(True):
                                fallback_sign = key["keyid"]
                                break
                        else:
                            # sign = first available private keyid (fingerprint) or False
                            sign = next((key["keyid"] for key, address in self._gpg_list_keys(True)
                                         if address_searched == address), False)
                        if not sign and self._sign != AUTO:
                            if fallback_sign:
                                sign = fallback_sign
                            else:
                                raise RuntimeError("No GPG sign key found")
                    elif not is_gpg_fingerprint(sign):  # sign is Path or key contents, import it and get its fingerprint
                        result = self._gnupg.import_keys(assure_fetched(sign, bytes))
                        sign = result.fingerprints[0]

                if encrypt:
                    if encrypt == AUTO:
                        # encrypt = True only if there exist a key for every neeeded address
                        addresses_searched = self._get_decipherers()
                        [addresses_searched.discard(address) for _, address in self._gpg_list_keys(False)]
                        if addresses_searched:
                            encrypt = False
                    elif encrypt is not True and not is_gpg_fingerprint(encrypt):
                        # XX multiple keys in list may be allowed
                        self._gnupg.import_keys(assure_fetched(encrypt, bytes))

        # if we plan to send later, convert text message to the email message object
        email = None
        if send is not None:
            email = self._prepare_email(data, encrypt and gpg_on, sign and gpg_on, sign)
            if not email:
                return
            data = email.as_bytes()

        # with GPG, encrypt or sign either text message or email message object
        micalg = None
        if encrypt or sign:
            if gpg_on:
                if encrypt:
                    data = self._encrypt_gpg_now(data, sign)
                elif sign:
                    data, micalg = self._sign_gpg_now(data, sign, send)
            else:
                d = self._encrypt_smime_now(data, sign, encrypt)
                email = BytesParser().parsebytes(d.strip())  # smime always produces a Message object, not raw data
            if (gpg_on and not data) or (not gpg_on and not email):
                logger.error("Signing/encrypting failed.")
                return

        # sending email message object
        self._result.clear()
        self._result_cache = None
        if send is not None:
            if gpg_on:
                if encrypt:
                    email = self._compose_gpg_encrypted(data)
                elif sign:  # gpg
                    email = self._compose_gpg_signed(email, data, micalg)
            elif encrypt or sign:  # smime
                # smime does not need additional EmailMessage to be included in, just restore Subject that has been
                # consumed in _encrypt_smime_now. It's interesting that I.E. "Reply-To" is not consumed there.
                email["Subject"] = self._subject
            email = self._send_now(email, encrypt, gpg_on, send)
            if not email:
                return

        # output to file or display
        if email or data:
            self._result.append(email if email else assure_fetched(data, str))
            if self._output:
                with open(self._output, "wb") as f:
                    f.write(email.as_bytes() if email else data)
            self._status = True

    def _get_gnupg_home(self, readable=False):
        return self._gpg if type(self._gpg) is str else ("default" if readable else None)

    def _send_now(self, email, encrypt, encrypted_subject, send):
        try:
            if not self.__from and send is True:
                logger.error("You have to specify sender e-mail.")
                return False
            if self.__from:
                email["From"] = self.__from
            if self._to:
                email["To"] = ",".join(self._to)
            if self._cc:
                email["Cc"] = ",".join(self._cc)
            if self._reply_to:
                email["Reply-To"] = ",".join(self._reply_to)
        except IndexError as e:
            s = set(self._to + self._cc + self._bcc)
            if self._reply_to:
                s.add(self._reply_to)
            if self.__from:
                s.add(self.__from)
            logger.error(f"An e-mail address seem to be malformed.\nAll addresses: {s}\n{e}")
            return

        # insert arbitrary headers
        # XX do not we want to encrypt these headers with GPG/SMIME?
        for k, v in self._headers.items():
            if k in ["Content-Type", "Content-Transfer-Encoding", "MIME-Version"]:
                # skip headers already inserted in _prepare_email
                continue
            try:
                email[k] = v
            except TypeError:
                # ex: Using random string with header Date
                raise TypeError(f"Wrong header {k} value: {v}")
        if self.__sender:
            email["Sender"] = self.__sender
        if "Date" not in email and not self._ignore_date:
            email["Date"] = formatdate(localtime=True)
        if "Message-ID" not in email and send != "test":  # we omit this field when testing
            email["Message-ID"] = make_msgid()

        if send and send != "test":
            failures = self._smtp.send_message(email, to_addrs=list(set(self._to + self._cc + self._bcc)))
            if failures:
                logger.warning(f"Unable to send to all recipients: {repr(failures)}.")
            elif failures is False:
                return False
        else:
            if send != "test":
                self._result.append(f"{'*' * 100}\nHave not been sent from {(self.__from or '')}"
                                    f" to {', '.join(set(self._to + self._cc + self._bcc))}")
            if encrypt:
                if encrypted_subject:
                    self._result.append(f"Encrypted subject: {self._subject}")
                self._result.append(f"Encrypted message: {self._message}")
            if len(self._result):  # put an empty line only if some important content was already placed
                self._result.append("")

        self._result_cache_hash = self._param_hash()
        return email

    def _param_hash(self):
        """ Check if headers changed from last _start call."""
        return hash(frozenset(self._headers.items())) + hash("".join(self.recipients())) + hash(self._subject) + hash(self.__from)

    def _sign_gpg_now(self, message, sign, send):
        status = self._gnupg.sign(
            message,
            extra_args=["--textmode"],
            # textmode: Enigmail had troubles to validate even though signature worked in CLI https://superuser.com/questions/933333
            keyid=sign,
            passphrase=self._passphrase if self._passphrase else None,
            detach=True if send is not None else None,
        )
        try:  # micalg according to rfc4880
            micalg = "pgp-" + {1: "MD5",
                               2: "SHA1",
                               3: "RIPEMD160",
                               8: "SHA256",
                               9: "SHA384",
                               10: "SHA512",
                               11: "SHA224"}[int(status.hash_algo)].lower()
        except KeyError:  # alright, just unknown algorithm
            micalg = None
        except TypeError:  # signature failed
            logger.error(status.stderr)
            return False, None
        return status.data, micalg

    def _encrypt_gpg_now(self, message, sign_fingerprint):
        exc = []
        if not self._to and not self._cc and not self._bcc:
            exc.append("No recipient e-mail specified")
        if self.__from is None:
            exc.append("No sender e-mail specified. If not planning to decipher later, put sender=False or --no-sender flag.")
        if exc:
            raise RuntimeError("Encrypt key present. " + ", ".join(exc))
        status = self._gnupg.encrypt(
            data=message,
            recipients=self._get_decipherers(),
            sign=sign_fingerprint if sign_fingerprint else None,
            passphrase=self._passphrase if self._passphrase else None
        )
        if status.ok:
            return status.data
        else:
            logger.warning(status.stderr)
            if "No secret key" in status.stderr:
                logger.warning(f"Secret key not found in {self._get_gnupg_home()} home folder. Create one.")
            if "Bad passphrase" in status.stderr:
                logger.warning(f"Bad passphrase for key.")
            if "Operation cancelled" in status.stderr:
                logger.info(f"You cancelled the key prompt.")
            if "Syntax error in URI" in status.stderr:
                logger.info(f"Unable to download missing key.")
            if any(s in status.stderr for s in ["No name", "No data", "General error", "Syntax error in URI"]):
                keys = [uid["uids"] for uid in self._gnupg.list_keys()]
                found = False
                for identity in self._get_decipherers():
                    if not [k for k in keys if [x for x in k if identity in x]]:
                        found = True
                        logger.warning(f"Key for {identity} seems missing.")
                if found:
                    s = self._get_gnupg_home()
                    s = f"GNUPGHOME={s} " if s else ""
                    logger.warning(f"See {s} gpg --list-keys")
            return False

    def _gpg_list_keys(self, secret=False):
        return ((key, address) for key in self._gnupg.list_keys(secret) for _, address in getaddresses(key["uids"]))

    def _get_decipherers(self):
        return set(self._to + self._cc + self._bcc + ([self.__from] if self.__from else []))

    def _encrypt_smime_now(self, email, sign, encrypt):
        with warnings.catch_warnings():
            # m2crypto.py:13: DeprecationWarning: the imp module is deprecated in favour of importlib;
            # see the module's documentation for alternative uses import imp
            warnings.simplefilter("ignore", category=DeprecationWarning)
            try:
                from M2Crypto import BIO, Rand, SMIME, X509, EVP  # we save up to 30 - 120 ms to load it here
            except ImportError:
                raise ImportError("Cannot import M2Crypto. Run: `sudo apt install swig && pip3 install M2Crypto`")
        output_buffer = BIO.MemoryBuffer()
        signed_buffer = BIO.MemoryBuffer()
        content_buffer = BIO.MemoryBuffer(email)

        # Seed the PRNG.
        temp = str(Path(tempfile.gettempdir(), 'envelope-randpool.dat'))
        Rand.load_file(temp, -1)

        # Instantiate an SMIME object.
        smime = SMIME.SMIME()

        if sign:
            # Since s.load_key shall not accept file contents, we have to set the variables manually
            sign = assure_fetched(sign, bytes)
            # XX remove getpass conversion to bytes callback when https://gitlab.com/m2crypto/m2crypto/issues/260 is resolved
            cb = (lambda x: bytes(self._passphrase, 'ascii')) if self._passphrase else (lambda x: bytes(getpass(), 'ascii'))
            try:
                smime.pkey = EVP.load_key_string(sign, callback=cb)
            except TypeError:
                raise TypeError("Invalid key")
            if self._cert:
                cert = self._cert
            else:
                cert = sign
            smime.x509 = X509.load_cert_string(cert)
            if not encrypt:
                p7 = smime.sign(content_buffer, SMIME.PKCS7_DETACHED)
                content_buffer = BIO.MemoryBuffer(email)  # we have to recreate it because it was sucked out
                smime.write(output_buffer, p7, content_buffer)
            else:
                p7 = smime.sign(content_buffer)
                smime.write(signed_buffer, p7)
                content_buffer = signed_buffer
        if encrypt:
            sk = X509.X509_Stack()
            if type(encrypt) is not list:
                encrypt = [encrypt]
            [sk.push(X509.load_cert_string(assure_fetched(e, bytes))) for e in encrypt]
            # XX certificates might be loaded from a directory by from, to, sender:
            # X509.load_cert_string(assure_fetched(e, bytes)).get_subject() ->
            # 'C=CZ, ST=State, L=City, O=Organisation, OU=Unit, CN=my-name/emailAddress=email@example.com'
            # X509.load_cert_string can take 7 µs, so the directory should be cached somewhere.
            smime.set_x509_stack(sk)
            smime.set_cipher(SMIME.Cipher('des_ede3_cbc'))  # Set cipher: 3-key triple-DES in CBC mode.

            # Encrypt the buffer.
            p7 = smime.encrypt(content_buffer)
            smime.write(output_buffer, p7)

        Rand.save_file(temp)
        return output_buffer.read()

    def _compose_gpg_signed(self, email, text, micalg=None):
        msg_payload = email
        email = EmailMessage()
        email["Subject"] = self._subject
        email.set_type("multipart/signed")
        email.set_param("protocol", "application/pgp-signature")
        if micalg:
            email.set_param("micalg", micalg)
        email.attach(msg_payload)
        msg_signature = EmailMessage()
        msg_signature['Content-Type'] = 'application/pgp-signature; name="signature.asc"'
        msg_signature['Content-Description'] = 'OpenPGP digital signature'
        msg_signature['Content-Disposition'] = 'attachment; filename="signature.asc"'
        msg_signature.set_payload(text)
        email.attach(msg_signature)
        return email

    @staticmethod
    def _compose_gpg_encrypted(text):
        # encrypted message structure according to RFC3156
        email = EmailMessage()
        email["Subject"] = "Encrypted message"  # real subject should be revealed when decrypted
        email.set_type("multipart/encrypted")
        email.set_param("protocol", "application/pgp-encrypted")
        msg_version = EmailMessage()
        msg_version["Content-Type"] = "application/pgp-encrypted"
        msg_version.set_payload("Version: 1")
        msg_text = EmailMessage()
        msg_text["Content-Type"] = 'application/octet-stream; name="encrypted.asc"'
        msg_text["Content-Description"] = "OpenPGP encrypted message"
        msg_text["Content-Disposition"] = 'inline; filename="encrypted.asc"'
        msg_text.set_payload(text)  # text was replaced by a GPG stream
        email.attach(msg_version)
        email.attach(msg_text)
        return email

    def _prepare_email(self, text: bytes, encrypt_gpg, sign_gpg, sign):
        """
        :type sign: If GPG, this should be the key fingerprint.
        """
        # we'll send it later, transform the text to the e-mail first
        msg_text = EmailMessage()
        # XX make it possible to be "plain" here + to have "plain" as the automatically generated html for older browsers
        # XX Should we assure it ends on CRLF? b"\r\n".join(text.splitlines()).decode("utf-8")
        if "MIME-Version" in self._headers:
            msg_text["MIME-Version"] = self._headers["MIME-Version"]
        if "Content-Type" not in self._headers:
            t = text.decode("utf-8")
            # determine mime subtype and maybe do nl2br
            mime, nl2br = self._mime, self._nl2br
            if mime == AUTO:
                tags = [x for x in ("<br", "<b>", "<i>", "<p", "<img") if x in t]
                if magic.Magic(mime=True).from_buffer(t) == "text/html" or len(tags):
                    # magic will determine a short text is HTML if there is '<a href=' but a mere '<br>' is not sufficient.
                    mime = "html"
                else:
                    mime = "plain"
            if mime == "html":
                if nl2br == AUTO and not len([x for x in ("<br", "<p") if x in t]):
                    nl2br = True
                if nl2br is True:
                    t = f"<br>{CRLF}".join(t.splitlines())
            msg_text.set_content(t, subtype=mime)
        else:
            msg_text["Content-Type"] = self._headers["Content-Type"]
            if "Content-Transfer-Encoding" in self._headers:
                msg_text["Content-Transfer-Encoding"] = self._headers["Content-Transfer-Encoding"]
            msg_text.set_payload(text, "utf-8")

        if self._attach_key:
            # send your public key as an attachment (so that it can be imported before it propagates on the server)
            contents = self._gnupg.export_keys(sign)
            if not contents:
                raise RuntimeError("Cannot attach GPG sign key, not found.")
            self.attach(contents, "public-key.asc")

        failed = False
        for contents in self._attachments:
            # get contents, user defined name and user defined mimetype
            # "path"/Path, [mimetype/filename], [mimetype/filename]
            name = mimetype = None
            if type(contents) is tuple:
                for s in contents[1:]:
                    if not s:
                        continue
                    elif "/" in s:
                        mimetype = s
                    else:
                        name = s
                contents = contents[0]
            if not name and isinstance(contents, Path):
                name = contents.name
            try:
                data = assure_fetched(contents, bytes)
            except FileNotFoundError:
                logger.error(f"Could not fetch file {contents.absolute()}")
                failed = True
                continue
            if not mimetype:
                mimetype = getattr(magic.Magic(mime=True), "from_file" if isinstance(contents, Path) else "from_buffer")(
                    str(contents))
            msg_text.add_attachment(data,
                                    maintype=mimetype.split("/")[0],
                                    subtype=mimetype.split("/")[1],
                                    filename=name or "attachment.txt")
        if failed:
            return False
        if encrypt_gpg:  # GPG inner message definition
            # in order to encrypt subject field → encapsulate the message into multipart having rfc822-headers submessage
            email = EmailMessage()
            email.set_type("multipart/mixed")
            email.set_param("protected-headers", "v1")

            msg_headers = EmailMessage()
            msg_headers.set_param("protected-headers", "v1")
            msg_headers.set_content(f"Subject: {self._subject}")
            msg_headers.set_type("text/rfc822-headers")  # must be set after set_content, otherwise reset to text/plain

            email.attach(msg_headers)
            email.attach(msg_text)
        else:  # plain message, smime or gpg-signed message
            email = msg_text
            if not sign_gpg:
                # due to an EmailMessage error (at least at Python3.7)
                # I cannot put diacritics strings like "Test =?utf-8?b?xZnFocW+xZnEjQ==?=" in subject
                # in inner message when GPG signing
                email["Subject"] = self._subject
        return email

    def recipients(self, *, clear=False):
        """ Return set of all recipients – To, Cc, Bcc
            :param: clear If true, all To, Cc and Bcc recipients are removed and the object is returned.
        """
        if clear:
            self._to.clear()
            self._cc.clear()
            self._bcc.clear()
            return self
        return set(self._to + self._cc + self._bcc)

    def check(self) -> bool:
        """
        If sender specified, check if DMARC DNS records exist and prints out the information.
        :rtype: bool SMTP connection worked
        """
        if self.__from:
            try:
                email = getaddresses([self.__from])[0][1]
                domain = email.split("@")[1]
            except IndexError:
                logger.warning(f"Could not parse domain from the sender address '{self.__from}'")
            else:
                def dig(query_or_list, rr="TXT", search_start=None):
                    if type(query_or_list) is not list:
                        query_or_list = [query_or_list]
                    for query in query_or_list:
                        try:
                            text = subprocess.check_output(["dig", "-t", rr, query]).decode("utf-8")
                            text = text[text.find("ANSWER SECTION:"):]
                            text = text[:text.find(";;")].split("\n")[1:-2]
                            res = []
                            for line in text:
                                # Strip tabs and quotes `_dmarc.gmail.com.\t600\tIN\tTXT\t"v=DMARC1;"` → `v=DMARC1;`
                                res.append(line.split("\t")[-1][1:-1])  #
                        except IndexError:
                            return []
                        else:
                            if res:
                                return res

                def search_start(list_, needle):
                    if list_:
                        for line in list_:
                            if line.startswith(needle):
                                return line

                spf = search_start(dig(domain), "v=spf")
                if not spf:
                    spf = search_start(dig(domain, "SPF"), "v=spf")
                if spf:
                    print(f"SPF found on the domain {domain}: {spf}")
                else:
                    logger.warning(f"SPF not found on the domain {domain}")
                print(f"See: dig -t SPF {domain} && dig -t TXT {domain}")

                dkim = dig(["mx1._domainkey." + domain, "mx._domainkey." + domain, "default._domainkey." + domain])
                if dkim:
                    print(f"DKIM found: {dkim}")
                else:
                    print("Could not spot DKIM. (But I do not know the selector.)")

                dmarc = dig("_dmarc." + domain)
                if dmarc:
                    print(f"DMARC found: {dmarc}")
                else:
                    print("Could not spot DMARC.")
        print("Trying to connect to the SMTP...")
        return bool(self._smtp.connect())  # check SMTP
