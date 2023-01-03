"""The :`base.constants.models` module contains
string constants referenced by other models in the application for the purpose of
establishing foreign key relationships between models.
"""

from dataclasses import dataclass


@dataclass
class AppModels:
    USER: str = "registration.AuthUser"
    ACCOUNT: str = "wallets.Account"
    TRANSACTION: str = "wallets.Transaction"
