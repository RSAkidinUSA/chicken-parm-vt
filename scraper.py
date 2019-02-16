#!/usr/bin/python3
"""Simple script for scraping the MITRE eCTF leaderboard."""

# to install required packages, run:
# pip install beautifulsoup4 requests schedule

import requests
import schedule
import time

from bs4 import BeautifulSoup
from collections import namedtuple


DINING_URL = 'http://foodpro.dsa.vt.edu'
# Headers to treat as web browser
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
#SLACK_WEBHOOK_URL = ('https://hooks.slack.com/services/'
#                     'T8VMEGMF1/B9SQ7L42G/iLI9UV1GKoQWLjNHfdzkdHS4')



mem_db = {}
last_msg = ''
Team = namedtuple('Team', ['name', 'score'])


def send_slack_msg(msg):
    """Send a message to the enabled slack channel channel."""
    requests.post(SLACK_WEBHOOK_URL, json={'text': msg})


def check_for_updates():
    """Check the eCTF scoreboard for updates in scores."""
    try:
        msg = ''
        get_menu()
        # for team in get_teams():
        #     old_score = mem_db[team.name]
        #     if team.score != old_score:
        #         msg += '{}\'s score changed from {} to {}\n'.format(
        #             team.name, old_score, team.score)
        #         mem_db[team.name] = team.score

        # if msg != '':
        #     updates = get_messages(last_msg)
        #     msg += 'Here\'s why:\n'
        #     msg += updates + '\n'
        #     send_slack_msg(msg)
    except Exception as e:
        print('Caught exception:')
        print(e)


def init_db():
    """Initialize the in-memory db."""
    msg = 'Scraper restarted. Current standings:\n'
    for i, team in enumerate(get_teams()):
        mem_db[team.name] = team.score
        msg += '{}. {} ({} points)\n'.format(i + 1, team.name, team.score)
    
    msg += 'Last feed update was:\n'
    msg += get_messages() + '\n'
    send_slack_msg(msg)


def get_menu():
    """Get a list of dates."""
    dates = []
    html_doc = requests.get(DINING_URL + '/menus/search.aspx?Action=SEARCH&strCurKeywords=chicken+parm', headers=HEADERS).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    menu_items = soup.find_all('li', class_='list-group-item menu_item')
    for item in menu_items:
        recipe_title =  list(item.find('a', class_='recipe_title'))[0]
        if 'Chicken Parmesan (no pasta)' in recipe_title:
            menu_date = list(item.find('div', class_='col-lg-12 recipe_date_container'))[0].strip()
            return menu_date
    return None

# def get_messages(Start=None):
#     """Get a list of all messages since an optional start message"""
#     global last_msg
#     msgs = []
#     html_doc = requests.get(LEADERBOARD_URL, headers=HEADERS).text
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     table = soup.find_all('table')[1]
#     table_body = table.find('tbody')
#     rows = table_body.find_all('tr')
#     for row in rows:
#         cells = row.find_all('td')
#         team = cells[1].text
#         event = cells[2].text
#         if ('Solved' in event):
#             msgs.append('%s %s' % (team, event))
#         else:
#             team += '\'' if team.endswith('s') else '\'s'
#             msgs.append('%s score updated' % (team,))
#         # break if last message reached
#         if (Start == None): 
#             break
#         elif (msgs[-1] == last_msg):
#             msgs = msgs[:-1]
#             break
#     if len(msgs) > 0:
#         last_msg = msgs[0]
#         return '\n'.join(msgs)
#     else:
#         return 'Retroactive updates to the scoreboard.\n'
    


if __name__ == '__main__':
    #init_db()
    # check_for_updates()
    cp_date = get_menu()
    if cp_date != None:
        print(cp_date)
    # schedule.every(3).minutes.do(check_for_updates)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
