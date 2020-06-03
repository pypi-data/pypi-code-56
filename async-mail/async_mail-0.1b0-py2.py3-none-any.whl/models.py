from dataclasses import dataclass
from dataclasses import field
from email.message import EmailMessage
from typing import Optional
from typing import List

from pydantic import BaseModel, SecretStr

from async_mail.config import settings


@dataclass
class Message:

    recipients: List[str]  # Todo check for multiple aka list
    subject: str
    message_body: str
    sender: str = settings.EMAIL_SENDER
    _message: EmailMessage = field(init=False, repr=False)

    def __post_init__(self):
        self._message = EmailMessage()
        self._message["From"] = self.sender
        self._message["To"] = self.recipients
        self._message["Subject"] = self.subject
        self._message.set_content(self.message_body)


class Connection(BaseModel):
    hostname: str
    port: int
    username: Optional[SecretStr]
    password: Optional[SecretStr]
    use_tls: bool
    timeout: int
