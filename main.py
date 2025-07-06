#!/usr/bin/python3
"""
Script to calculate finances into the future

Change the state.yaml file to fit your needs
"""
import yaml

class Account(object):
    def __init__(self, name: str, start_balance: float = 0.0, yearly_interest: float = 0.0):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.balance = start_balance
        if not (0 <= yearly_interest <= 1):
            raise ValueError("Interest must be between 0 and 1")
        self.interest = ((yearly_interest + 1) ** (1/12)) - 1
        self.tracker_total_income = 0.0
        self.tracker_total_interest = 0.0
        self.tracker_monthly_income = 0.0
        self.tracker_monthly_interest = 0.0

    def deposit(self, amount):
        self.balance += amount
        self.tracker_total_income += amount
        self.tracker_monthly_income += amount

    def _interest(self):
        if not self.interest:
            return
        pre_balance = self.balance
        self.balance = self.balance * (1 + self.interest)
        self.tracker_total_interest += self.balance - pre_balance
        self.tracker_monthly_interest += self.balance - pre_balance

    def monthly(self):
        self._interest()
        self._print_full()
        self.tracker_monthly_income = 0.0
        self.tracker_monthly_interest = 0.0

    def _print_full(self):
        print(f"Monthly Report: {self.name}")
        if self.tracker_monthly_income:
            print(f" Income  : {self.tracker_monthly_income:+15_.2f}€")
        if self.tracker_monthly_interest:
            print(f" Interest: {self.tracker_monthly_interest:+15_.2f}€ ({self.interest * 100:-.4f}%)")
        print(f" Balance : {self.balance:-15_.2f}€")

    def __str__(self):
        output = ""
        output += f"Account Report: {self.name}\n"
        if self.tracker_total_income:
            output += f" Income  : {self.tracker_total_income:+15_.2f}€\n"
        if self.tracker_total_interest:
            output += f" Interest: {self.tracker_total_interest:+15_.2f}€\n"
        output += f" Balance : {self.balance:-15_.2f}€"
        return output

class Bank(object):
    def __init__(self, name: str):
        self.name = name
        self.accounts = []
        self.total = 0.0

    def import_dict(self, data: dict):
        for raw_account in data:
            account = Account(
                    name = raw_account["name"],
                    start_balance = raw_account["balance"],
                    yearly_interest = raw_account["interest"]
                    )
            self.accounts.append(account)
        self._calc_total()

    def deposit(self, account_name, amount):
        account = [account for account in self.accounts if account.name == account_name]
        if len(account) != 1:
            raise KeyError("No Account with that name found")
        account = account[0]
        account.deposit(amount)

    def register_account(self, account: Account):
        self.accounts.append(account)
        self._calc_total()

    def _calc_total(self):
        self.total = 0
        for account in self.accounts:
            self.total += account.balance

    def monthly(self):
        for account in self.accounts:
            account.monthly()
        self._calc_total()

    def __str__(self):
        output = ""
        output += f"Bank {self.name} ------------------------\n"
        for account in self.accounts:
            output += str(account) + "\n"
        output += f"-> Total: {self.total:-15_.2f}€\n"
        output += f"-----------------------------------------"
        return output

def load_settings():
    with open("state.yaml", "r", encoding="utf-8") as f:
        settings = yaml.load(f, Loader=yaml.SafeLoader)
        if settings.get("time_goal"):
            settings["money_goal"] = 1e15
        elif settings.get("money_goal"):
            settings["time_goal"] = 12 * 100
        else:
            settings["time_goal"] = 12 * 100
            settings["money_goal"] = 1e15

        settings["profit"] = settings["income"] - settings["upkeep"]
        return settings
    return {}

def main():
    settings = load_settings()
    if settings["profit"] == 0:
        print("Equilibrium you spend as much as you earn")
        return
    bank = Bank("Accounts")
    bank.import_dict(settings["accounts"])
    print(bank)
    month = 1
    while month < settings["time_goal"] and 0 <= bank.total <= settings["money_goal"]:
        print(f"################## Month: {month: 4d} #################")
        bank.deposit("Checking-Account", 750)
        bank.deposit("Investment-Account", 750)
        bank.monthly()
        print("")
        print(bank)
        month += 1

    if month >= settings["time_goal"]:
        print("Too long, will not work")
        return
    if bank.total <= 0:
        print("#############################")
        print("You will run out of money in:")
        print("#############################")
    else:
        print(f"If all goes to plan you have your {settings['money_goal']:-.2f}€ in:")
    years = int(month/12)
    month = month % 12
    print(f"--> {years} years and {month%12} months")
    return 0

if __name__ == '__main__':
    main()
    exit(0)
