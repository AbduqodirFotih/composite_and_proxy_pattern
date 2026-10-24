from abc import ABC, abstractmethod

class AccessDeniedException(Exception):
    pass

class BankAccount(ABC):
    @abstractmethod
    def get_balance(self) -> float:
        pass

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

class RealBankAccount(BankAccount):
    def __init__(self, initial_balance: float):
        self._balance = initial_balance

    def get_balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if self._balance >= amount:
            self._balance -= amount
        else:
            raise ValueError("Hisobda yetarli mablag' mavjud emas.")

class BankAccountProxy(BankAccount):
    def __init__(self, real_account: BankAccount, permission: str):
        self._real_account = real_account
        self._permission = permission.upper()

    def get_balance(self) -> float:
        if self._permission in ("READ", "FULL"):
            return self._real_account.get_balance()
        raise AccessDeniedException("Balansni ko'rish uchun ruxsatingiz yetarli emas.")

    def deposit(self, amount: float) -> None:
        if self._permission == "FULL":
            self._real_account.deposit(amount)
        else:
            raise AccessDeniedException("Hisobni to'ldirish uchun to'liq ruxsat talab qilinadi.")

    def withdraw(self, amount: float) -> None:
        if self._permission == "FULL":
            self._real_account.withdraw(amount)
        else:
            raise AccessDeniedException("Hisobdan pul yechish uchun ruxsat berilmadi.")

if __name__ == "__main__":
    account = RealBankAccount(1000.0)

    read_only_proxy = BankAccountProxy(account, "READ")
    full_access_proxy = BankAccountProxy(account, "FULL")

    print(f"Mijoz hisob balansi: ${read_only_proxy.get_balance():.2f}")

    full_access_proxy.deposit(500.0)
    print(f"Hisob to'ldirildi, yangi balans: ${full_access_proxy.get_balance():.2f}")

    full_access_proxy.withdraw(200.0)
    print(f"Pul yechildi, qolgan balans: ${full_access_proxy.get_balance():.2f}")

    try:
        read_only_proxy.withdraw(100.0)
    except AccessDeniedException as error:
        print(f"Amal bajarilmadi: {error}")
