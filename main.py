import helpers

if __name__ == '__main__':
    print('Welcome to the Threshold Data Clinic!')

    print('loading line items')
    line_items = helpers.load_line_items()

    print('loading campaigns')
    campaigns = helpers.load_campaigns()

    print('adding line item tactics')
    for line_item in line_items:
        line_item['tactic'] = helpers.find_line_item_tactic(line_item)

    print('adding campaign tactics')
    for campaign in campaigns:
        campaign['tactic'] = helpers.find_campaign_tactic(campaign)

    print('dumping line items to new csv')
    helpers.dump_line_items(line_items)

    print('dumping campaigns to new csv')
    helpers.dump_campaigns(campaigns)


