import argparse
import select
import sys
from pathlib import Path

from jsonpickle import decode

from .envelope import Envelope


class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # noinspection PyProtectedMember
        return argparse.HelpFormatter._split_lines(self, text, width)


class BlankTrue(argparse.Action):
    """ When left blank, this flag produces True. (Normal behaviour is to produce None which I use for not being set."""

    def __call__(self, _, namespace, values, option_string=None):
        if values in [None, []]:  # blank argument with nargs="?" produces None, with ="*" produces []
            values = True
        setattr(namespace, self.dest, values)


def _get_envelope(instance: Envelope, args):
    """ Internal method. If loaded from STDIN, Envelope object exists already otherwise new object is created.  """
    # noinspection PyProtectedMember
    return Envelope(**args) if instance is None else instance._populate(args)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=SmartFormatter)
    group_io = parser.add_argument_group("Input/Output")
    group_io.add_argument('--message', help='Plain text message.', metavar="TEXT", nargs="?", action=BlankTrue)
    group_io.add_argument('--input', help='Path to message file. (Alternative to `message` parameter.)', metavar="FILE")
    group_io.add_argument('--output',
                        help='Path to file to be written to (else the contents is returned if ciphering or True if sending).',
                        metavar="FILE")

    group_ciph = parser.add_argument_group("Ciphering")
    group_ciph.add_argument('--gpg', help='Home path to GNUPG rings else default ~/.gnupg is used.'
                                      'Leave blank for prefer GPG over S/MIME.', nargs="?", action=BlankTrue, metavar="PATH")
    group_ciph.add_argument('--smime', action="store_true", help='Leave blank for prefer S/MIME over GPG.')
    group_ciph.add_argument('--sign', help='R|Sign the message.'
                                       '\n * "auto" for turning on signing if there is a key matching to the "from" header'
                                       '\n * GPG: Blank for user default key or key ID/fingerprint.'
                                       '\n * S/MIME: Key data.', nargs="?",
                        action=BlankTrue, metavar="FINGERPRINT|CONTENTS")
    group_ciph.add_argument('--cert', help='S/MIME: Certificate contents if not included in the key.',
                        action=BlankTrue, metavar="CONTENTS")
    group_ciph.add_argument('--passphrase', help='If signing key needs passphrase.')
    group_ciph.add_argument('--sign-path', help='Filename with the sender\'s private key. (Alternative to `sign` parameter.)',
                        metavar="KEY-PATH")
    group_ciph.add_argument('--cert-path', help='S/MIME: Filename with the sender\'s S/MIME private cert'
                                            ' if cert not included in the key. (Alternative to `cert` parameter.)',
                        metavar="CERT-PATH")

    group_ciph.add_argument('--encrypt', help='R|* GPG:'
                                          "\n  * Blank for user default key"
                                          "\n  * key ID/fingerprint"
                                          "\n  * Any attainable contents with the key to be signed with"
                                          " (will be imported into keyring)"
                                          "\n  * \"auto\" for turning on encrypting if there is a matching key for every recipient"
                                          "\n* S/MIME any attainable contents with certificate to be encrypted with or their list",
                        nargs="*", action=BlankTrue, metavar="GPG-KEY/SMIME-CERTIFICATE-CONTENTS")
    group_ciph.add_argument('--encrypt-path', help='Filename(s) with the recipient\'s public key.'
                                               ' (Alternative to `encrypt` parameter.)',
                        nargs="*", metavar="PATH")
    group_ciph.add_argument('--attach-key', help="Appending public key to the attachments when sending.", action="store_true")

    group_send = parser.add_argument_group("Sending")
    group_send.add_argument('-s', '--subject', help="E-mail subject", nargs="?", action=BlankTrue)
    group_send.add_argument('-t', '--to', help="E-mail – needed to choose their key if encrypting", nargs="+", metavar="E-MAIL")
    group_send.add_argument('--cc', help="E-mail or list", nargs="+", metavar="E-MAIL")
    group_send.add_argument('--bcc', help="E-mail or list", nargs="+", metavar="E-MAIL")
    group_send.add_argument('--reply-to', help="Header that states e-mail to be replied to. The field is not encrypted.",
                        metavar="E-MAIL")
    group_send.add_argument('-f', '--from', help="Alias of --sender", metavar="E-MAIL")
    group_send.add_argument('--sender', help="E-mail – needed to choose our key if encrypting", metavar="E-MAIL")
    group_send.add_argument('--no-sender', action="store_true",
                        help="We explicitly say we do not want to decipher later if encrypting.")
    group_send.add_argument('-a', '--attachment',
                        help="Path to the attachment, followed by optional file name to be used and/or mimetype."
                             " This parameter may be used multiple times.",
                        nargs="+", action="append")
    group_send.add_argument('--header',
                        help="Any e-mail header in the form `name value`. Flag may be used multiple times.",
                        nargs=2, action="append", metavar=("NAME", "VALUE"))
    group_send.add_argument('--mime', help="Set contents mime subtype: 'html' (default) or 'plain' for plain text",
                        metavar="SUBTYPE")
    group_send.add_argument('--smtp', help="SMTP server. List `host, [port, [username, password, [security]]]` or dict.\n"
                                       "Ex: '--smtp {\"host\": \"localhost\", \"port\": 25}'."
                                       " Security may be explicitly set to 'starttls', 'tls' or automatically determined by port.",
                        nargs="*", action=BlankTrue, metavar=("HOST", "PORT"))
    group_send.add_argument('--send', help="Send e-mail. Blank to send now.", nargs="?", action=BlankTrue)

    group_supp = parser.add_argument_group("Supportive")
    group_supp.add_argument('--check', action="store_true", help='Check SMTP server connection')
    group_supp.add_argument('--load', help="Path to the file to build an Envelope object from.", metavar="FILE")
    group_supp.add_argument('-q', '--quiet', help="Quiet output", action="store_true")

    args = vars(parser.parse_args())

    # cli arguments
    quiet = args.pop("quiet")

    # build instance
    # determine if we have to load the instance from a file or string

    if args["load"]:
        instance = Envelope.load(Path(args["load"]))
    elif select.select([sys.stdin, ], [], [], 0.0)[0] \
            or len(sys.argv) == 1 \
            or args["subject"] is True or args["message"] is True:
        # XXX check if using `select` to detect STDIN does not mess up Windows
        instance = Envelope.load(sys.stdin.read())
    else:
        instance = None
    del args["load"]

    # in command line, we may specify input message by path (in module we would rather call message=Path("path"))
    if args["input"]:
        if args["message"]:
            raise RuntimeError("Cannot define both input and message.")
        args["message"] = Path(args["input"])
    del args["input"]

    # we explicitly say we do not want to decipher later if encrypting
    if args["no_sender"]:
        args["sender"] = False
    del args["no_sender"]

    # user is saying that encryption key has been already imported
    enc = args["encrypt"]
    if enc and enc is not True:
        if enc.lower() in ["1", "true", "yes"]:
            args["encrypt"] = True
        elif enc.lower() in ["0", "false", "no"]:
            args["encrypt"] = False

    # user specified encrypt key in a path. And did not disabled encryption
    if args["encrypt_path"] and args["encrypt"] is not False:
        if args["encrypt"] not in [True, None]:  # user has specified both path and the key
            raise RuntimeError("Cannot define both encrypt key data and encrypt key path.")
        if type(args["encrypt_path"]) is list:
            args["encrypt"] = [Path(p) for p in args["encrypt_path"]]
        else:
            args["encrypt"] = Path(args["encrypt_path"])
    del args["encrypt_path"]

    # user specified sign key in a path. And did not disabled signing
    if args["sign_path"] and args["sign"] is not False:
        if args["sign"] not in [True, None]:  # user has specified both path and the key
            raise RuntimeError("Cannot define both sign key data and sign key path.")
        args["sign"] = Path(args["sign_path"])
    del args["sign_path"]

    if args["cert_path"]:
        if args["cert"] is not None:
            raise RuntimeError("Cannot define both cert and cert-path.")
        args["cert"] = Path(args["cert_path"])
    del args["cert_path"]

    # smtp can be a dict
    if args["smtp"] and args["smtp"][0].startswith("{"):
        args["smtp"] = decode(" ".join(args["smtp"]))

    # send = False turns on debugging
    if args["send"] and type(args["send"]) is not bool:
        if args["send"].lower() in ["0", "false", "no"]:
            args["send"] = False
        elif args["send"].lower() in ["1", "true", "yes"]:
            args["send"] = True

    # convert to the module-style attachments `/tmp/file.txt text/plain` → (Path("/tmp/file.txt"), "text/plain")
    args["attachments"] = []
    if args["attachment"]:
        for attachment in args["attachment"]:
            attachment[0] = Path(attachment[0])  # path-only (no direct content) allowed in CLI
            # we cast to tuple so that single attachment is not mistaken for list of attachments
            args["attachments"].append(tuple(attachment))
    del args["attachment"]

    args["headers"] = args["header"]
    del args["header"]

    if args["from"]:
        args["sender"] = args["from"]
    del args["from"]

    if args["check"]:
        del args["sign"]
        del args["encrypt"]
        del args["send"]
        del args["check"]
        o = _get_envelope(instance, args)
        if o.check():
            print("Check succeeded.")
            sys.exit(0)
        else:
            print("Check failed.")
            sys.exit(1)
    else:
        del args["check"]

        # XX allow any header to be displayed, ex: `--header Received` will display all Received headers
        read_method = None
        if args["subject"] is True:
            read_method = "subject"
            del args["subject"]
        if args["message"] is True:
            read_method = "message"
            del args["message"]

        res = _get_envelope(instance, args)
        if read_method:
            print(getattr(res, read_method)())
        elif not any([read_method, args["sign"], args["encrypt"], args["send"]]):
            # if there is anything to do, pretend the input parameters are a bone of a message
            print(str(res))
            sys.exit(0)
        elif res:
            if not quiet:
                print(res)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
