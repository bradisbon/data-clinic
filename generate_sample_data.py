import csv
import datetime
import random
import typing
from dataclasses import dataclass


COMPANIES = [
    "Costa Coffee",
    "Evian",
    "Dasani",
    "Heineken",
    "Gatorade",
    "Tetley's Brewery",
    "Batemans Brewery",
    "Jones Soda",
    "Grapette",
    "Jif (lemon juice)",
    "Royal Tru",
    "Oronamin",
    "Culligan",
    "Belvedere Vodka",
    "Wodka Gorbatschow",
    "White Horse (whisky)",
    "Grand Old Parr",
    "Finlandia (vodka)",
    "Colgate",
    "Fanta",
    "Pizza Hut",
    "Head & Shoulders",
    "Domino's Pizza",
    "Ben & Jerry's",
    "Heineken",
    "Gatorade",
    "Milo",
    "Starbucks",
    "Audi",
    "NIVEA",
    "Snickers",
    "Nescafe",
    "KFC(Kentucky Fried Chicken)",
    "Levi's Jeans",
    "Lipton",
    "Pampers",
    "Coca-Cola",
    "Beam Suntory",
    "Live+",
    "Tango (drink)",
    "Tizer",
    "Dr. Enuf",
    "ToniCol",
    "Campa Cola",
    "Mezzo Mix",
]


@dataclass
class Account:
    gl: str
    name: str

@dataclass
class Tactic:
    name: str
    li_description: str

ACCOUNTS_TACTICS = [
    [Account('4305', 'Google Ads'),Tactic('Search','Monthly Search Retainer')],
    [Account('4305', 'Google Ads'),Tactic('Retargeting','Monthly Retargeting Retainer')],
    [Account('4315', 'Facebook Ads'),Tactic('Traffic','Monthly Traffic Retainer')],
    [Account('4315', 'Facebook Ads'),Tactic('Retargeting','Monthly Retargeting Retainer')],
]

def create_parents(client_cos: typing.List[str], parent_cos: typing.List[str]) -> typing.List[str]:
    parents = []

    for client in client_cos:
        parents.append([random.choice(parent_cos),client])
    for parent in parent_cos:
        parents.append([parent,parent])

    return parents


def add_spaces(cos: typing.List[str], proportion: float):
    with_spaces = []

    for co in cos:
        if random.random() <= proportion:
            with_spaces.append(' ' + co)
        else:
            with_spaces.append(co)

    return with_spaces


def generate_line_item(company, account:Account, tactic:Tactic, spend_seed, date_within_start:datetime.date, date_within_end:datetime.date):

    return {'company': company + ' ' if random.random() < 0.05 else company,
            'gl':account.gl,
            'description':tactic.li_description,
            'date':str(date_within_start + datetime.timedelta(random.randint(0,(date_within_end-date_within_start).days))),
            'amount':random.randint(int(spend_seed*0.85),int(spend_seed*1.15))
            }


def generate_campaign(company, account:Account, tactic:Tactic, spend_seed, start_date:datetime.date, end_date:datetime.date):

    return {'company': company,
            'platform':account.name,
            'campaign':f'{tactic.name} campaign',
            'start_date':start_date,
            'end_date':end_date,
            'amount':random.randint(int(spend_seed*0.85),int(spend_seed*1.15))
            }


def generate_parents_csv():
    with open('parent_companies.csv','w') as f:
        writer = csv.DictWriter(f, fieldnames=['Parent','Client'])
        writer.writeheader()

        parents = create_parents(COMPANIES[:-10],COMPANIES[-10:])
        for parent,client in parents:
            writer.writerow({'Parent':parent, 'Client':client})


def generate_spend_seeds():
    spend_seeds = []
    for company in COMPANIES:
        for account_tactic in random.sample(ACCOUNTS_TACTICS,random.randint(0,len(ACCOUNTS_TACTICS))):
                spend_seeds.append([company,account_tactic,random.randrange(0,2000)])

    return spend_seeds


def generate_line_items(spend_seeds, date_within_start:datetime.date, date_within_end:datetime.date):
    return [generate_line_item(company, account, tactic, spend_seed, date_within_start, date_within_end)
            for company, (account, tactic), spend_seed in spend_seeds]


def generate_campaigns(spend_seeds, start_date:datetime.date, end_date:datetime.date):
    return [generate_campaign(company, account, tactic, spend_seed, start_date, end_date)
            for company, (account, tactic), spend_seed in spend_seeds]


if __name__ == '__main__':
    with open('line_items.csv','w') as li_f:
        li_writer = csv.DictWriter(li_f,['date','company','gl','description','amount'])
        li_writer.writeheader()
        with open('campaigns.csv','w') as c_f:
            campaign_writer = csv.DictWriter(c_f,['start_date','end_date','company','platform','campaign','amount'])
            campaign_writer.writeheader()
            
            for start_date, end_date in [(datetime.date(2022,3,1),datetime.date(2022,3,31)),
                                         (datetime.date(2022,4,1),datetime.date(2022,4,30)),
                                         (datetime.date(2022,5,1),datetime.date(2022,5,31)),]:
                spend_seeds = generate_spend_seeds()
                li_writer.writerows(generate_line_items(spend_seeds,start_date,end_date))
                campaign_writer.writerows(generate_campaigns(spend_seeds,start_date,end_date))
    generate_parents_csv()
