from pydantic import BaseModel


class Account(BaseModel):
    floating_ip_limit: int
    droplet_limit: int
    volume_limit: int
    email: str
    uuid: str
    email_verified: bool
    status: str
    status_message: str
