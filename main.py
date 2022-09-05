#!/usr/bin/python3
"""
Script to calculate finances into the future

Change the state.yaml file to fit your needs
"""
import sys
import yaml


def print_status():
    """
    Prints the Status information and calulates growth
    """
    plus_bank = 0
    plus_invest = 0
    plus_kapital = 0
    perc_bank = 0
    perc_invest = 0
    perc_kapital = 0
    if bank != 0:
        plus_bank = bank - prev_bank
        perc_bank = round((plus_bank / bank) * 100, 2)
        if plus_bank < 0 < perc_bank:
            perc_bank *= -1
    if invest != 0:
        plus_invest = invest - prev_invest
        perc_invest = round((plus_invest / invest) * 100, 2)
        if plus_invest < 0 < perc_invest:
            perc_invest *= -1
    if kapital != 0:
        plus_kapital = kapital - prev_kapital
        perc_kapital = round((plus_kapital / kapital) * 100, 2)
        if plus_kapital < 0 < perc_kapital:
            perc_kapital *= -1
    print(f"Bank: {bank:+.2f}€ ({plus_bank:+.2f}€ {perc_bank:+.2f}%)")
    print(f"Inv.: {invest:+.2f}€ ({plus_invest:+.2f}€ {perc_invest:+.2f}%)")
    print(f"Ges.: {kapital:+.2f}€ ({plus_kapital:+.2f}€ {perc_kapital:+.2f}%)")
    print("Mon.:", months)


data = {}

with open("state.yaml", "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
data["gewinn"] = data["einkommen"] - data["unterhalt"]
data["investing"] = 0
if data["gewinn"] > 0:
    data["investing"] = round(data["gewinn"] * data["invest_perc"], 2)
data["gewinn"] = data["gewinn"] - data["investing"]

for key, value in data.items():
    if 0 < value < 1:
        print(f"{key}:\t{value*100}%")
    else:
        print(f"{key}:\t{value}€")

if (data["gewinn"] == 0 and data["investing"] == 0):
    print("Equilibrium you spend as much as you earn")
    sys.exit(0)

print()
print("--------------")
print()

bank = 0
invest = 0
kapital = data["kapital"] + bank + invest
months = 0

prev_bank = bank
prev_invest = invest
prev_kapital = kapital

MAX_MONTHS = 10000

while(kapital < data["ziel"] and months < MAX_MONTHS and kapital > 0):
    prev_kapital = kapital
    prev_bank = bank
    prev_invest = invest

    # Add einkommen
    bank += round(data["gewinn"], 2)
    invest += round(data["investing"], 2)
    # Calc interest
    invest = round(invest * (1 + (data["zins"] / 12)), 2)
    # Calc full capital
    kapital = data["kapital"] + bank + invest

    months += 1
    print_status()
    print("---")

if months >= MAX_MONTHS:
    print("Too long, will not work")
    sys.exit(0)
if kapital <= 0:
    print("#############################")
    print("You will run out of money in:")
    print("#############################")
else:
    print(f"If all goes to plan you have your {data['ziel']}€ in:")
years = int(months/12)
months = months % 12
print(f"--> {years} years and {months%12} months")
