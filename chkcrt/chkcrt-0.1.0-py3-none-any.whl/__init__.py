"""Check for (soon to be) expired certificates."""

import argparse
import concurrent.futures
import datetime
import logging
import os
import socket
import ssl
import time
import typing

import slack
from cryptography import x509
from cryptography.hazmat.backends import default_backend

__version__ = "0.1.0"
_logger = logging.getLogger(__name__)


# Adapted from https://stackoverflow.com/a/34073559
class GeneratorWithReturn:
    def __init__(self, gen):
        self.gen = gen
        self.value = None

    def __iter__(self):
        self.value = yield from self.gen


class Netloc(typing.NamedTuple):
    host: str
    port: int

    def __str__(self):
        return f"{self.host:s}:{self.port:d}"

    @classmethod
    def from_str(cls, s: str) -> "Netloc":
        host, _, port_str = s.partition(":")
        port = int(port_str) if port_str else 443
        return cls(host, port)


class NetlocCert(typing.NamedTuple):
    netloc: Netloc
    cert: x509.Certificate

    def __lt__(self, other):
        return self.cert.not_valid_after < other.cert.not_valid_after


NotifyFunc = typing.Callable[
    [typing.Iterable[NetlocCert], typing.Iterable[NetlocCert], datetime.datetime], None
]
CertGetterFunc = typing.Callable[[Netloc, float], typing.Optional[x509.Certificate]]


def _get_md_text(
    expired: typing.Iterable[NetlocCert],
    expires_soon: typing.Iterable[NetlocCert],
    now: datetime.datetime,
) -> str:
    lines = []
    if expired:
        lines.extend(["Certificates for the following domains have expired:", ""])
        for nl, crt in expired:
            lines.append(
                f"- `{nl!s}` (expired {(now - crt.not_valid_after).days:d} day(s) ago)"
            )

    if expires_soon:
        if lines:
            lines.append("")
        lines.extend(["Certificates for the following domains will expire soon:", ""])
        for nl, crt in expires_soon:
            lines.append(
                f"- `{nl!s}` (expires in {(crt.not_valid_after - now).days:d} day(s))"
            )

    return "\n".join(lines)


def make_cert_getter() -> CertGetterFunc:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    crypto_backend = default_backend()

    def cert_getter(
        netloc: Netloc, timeout: float
    ) -> typing.Optional[x509.Certificate]:
        _logger.debug("Getting certificate for: %s", netloc)
        sock = socket.create_connection(netloc, timeout=timeout)
        ssl_sock = ssl_context.wrap_socket(sock, server_hostname=netloc.host)
        with sock, ssl_sock:
            cert_der = ssl_sock.getpeercert(binary_form=True)
            return (
                None
                if cert_der is None
                else x509.load_der_x509_certificate(cert_der, crypto_backend)
            )

    return cert_getter


def make_slack_notifier(api_token: str, channel: str) -> NotifyFunc:
    client = slack.WebClient(token=api_token)

    def notify(expired, expires_soon, now):
        text = _get_md_text(expired, expires_soon, now)
        try:
            _logger.debug("Posting message to Slack channel: %s", channel)
            client.chat_postMessage(channel=channel, text=text)
        except slack.errors.SlackApiError:
            _logger.exception("Failed to post message to Slack")

    return notify


def iter_certs(
    netlocs: typing.Iterable[Netloc],
    cert_getter: CertGetterFunc,
    num_workers: int,
    timeout: float,
) -> typing.Generator[NetlocCert, None, bool]:
    success = True
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as pool:
        future_map = {
            pool.submit(cert_getter, netloc, timeout): netloc for netloc in netlocs
        }
        for future in concurrent.futures.as_completed(future_map):
            netloc = future_map[future]
            try:
                cert = future.result()
            except Exception:
                _logger.exception("Error while checking: %s", netloc)
                success = False
            else:
                if cert is None:
                    _logger.warning("No certificate for: %s", netloc)
                    success = False
                else:
                    yield NetlocCert(netloc, cert)

    return success


def check_certs(
    g: GeneratorWithReturn,
    now: datetime.datetime,
    soon: datetime.datetime,
    notify: typing.Optional[NotifyFunc] = None,
) -> bool:
    expired, expires_soon = [], []
    success = True
    cnt, t0 = 0, time.time()
    for nlc in g:
        status = "."
        if nlc.cert.not_valid_after <= now:
            status, success = "E", False
            expired.append(nlc)
        elif nlc.cert.not_valid_after < soon:
            status, success = "W", False
            expires_soon.append(nlc)

        print(
            "\t".join(
                str(v)
                for v in (
                    status,
                    nlc.cert.not_valid_after,
                    (nlc.cert.not_valid_after - now).days,
                    nlc.netloc,
                )
            )
        )

        cnt += 1

    _logger.info("Checked %d certificates in %.2f second(s)", cnt, time.time() - t0)

    if callable(notify) and (expired or expires_soon):
        notify(sorted(expired), sorted(expires_soon), now)

    return success and g.value


def main():
    parser = argparse.ArgumentParser(
        description="Check for (soon to be) expired certificates"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--debug",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO,
        dest="loglevel",
        help="enable debug message logging",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="min. number of days to consider the certificate as valid. "
        "Default: %(default)d",
        metavar="N",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=os.cpu_count() * 5,
        help="max. number of workers. Default: %(default)d",
        metavar="N",
    )
    parser.add_argument(
        "--slack-api-token",
        default=os.environ.get("SLACK_API_TOKEN"),
        help="Slack API token. Can be set using SLACK_API_TOKEN environment variable",
        metavar="TOKEN",
    )
    parser.add_argument(
        "--slack-channel",
        default=os.environ.get("SLACK_CHANNEL"),
        help="Slack channel to post to. "
        "Can be set using SLACK_CHANNEL environment variable",
        metavar="CHANNEL",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="network timeout (in seconds) when connecting to fetch the certificate. "
        "Default: %(default).02f",
        metavar="SECONDS",
    )
    parser.add_argument(
        "netlocs",
        nargs="*",
        metavar="HOST[:PORT]",
        default=os.environ.get("CHKCRT_NETLOCS").split()
        if os.environ.get("CHKCRT_NETLOCS")
        else None,
        help="host (and, optionally, port) provided in form HOST[:PORT]. "
        "If port is not provided it defaults to 443. "
        "Can be set using CHKCRT_NETLOCS environment variable",
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    notify = None
    if args.slack_api_token and args.slack_channel:
        notify = make_slack_notifier(args.slack_api_token, args.slack_channel)

    now = datetime.datetime.utcnow()
    soon = now + datetime.timedelta(days=args.days)
    success = check_certs(
        GeneratorWithReturn(
            iter_certs(
                (Netloc.from_str(s) for s in args.netlocs),
                make_cert_getter(),
                num_workers=args.num_workers,
                timeout=args.timeout,
            )
        ),
        now=now,
        soon=soon,
        notify=notify,
    )
    parser.exit(not success)
