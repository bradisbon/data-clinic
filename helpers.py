import csv


def load_line_items():
    line_items = []
    with open('line_items.csv','r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            line_items.append(line)

    return line_items


def load_campaigns():
    campaigns = []
    with open('campaigns.csv','r') as file:
        reader = csv.DictReader(file)

        for line in reader:
            campaigns.append(line)

    return campaigns


def find_line_item_tactic(line_item):
    gl = line_item['gl']
    desc = line_item['description']
    if gl == '4305':
        if 'Search' in desc:
            return 'Search'
        if 'Retargeting' in desc:
            return 'Retargeting'
    if gl == '4315':
        if 'Traffic' in desc:
            return 'Facebook Traffic'
        if 'Retargeting' in desc:
            return 'Facebook Retargeting'


def find_campaign_tactic(campaign):
    platform = campaign['platform']
    name = campaign['campaign']
    if platform == 'Google Ads':
        if 'Search' in name:
            return 'Search'
        if 'Retargeting' in name:
            return 'Retargeting'
    if platform == 'Facebook Ads':
        if 'Traffic' in name:
            return 'Facebook Traffic'
        if 'Retargeting' in name:
            return 'Facebook Retargeting'


def dump_line_items(line_items):
    with open('line_items_with_tactics.csv', 'w') as file:
        fields = ['company', 'gl', 'description', 'date', 'amount', 'tactic']
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(line_items)


def dump_campaigns(line_items):
    with open('campaigns_with_tactics.csv', 'w') as file:
        fields = ['company', 'platform', 'campaign', 'start_date',  'end_date', 'amount', 'tactic']
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(line_items)
