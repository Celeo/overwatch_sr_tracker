import csv
from datetime import datetime
import json
import logging
from typing import List

import requests
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-10s %(levelname)-6s %(message)s')
logger = logging.getLogger(__name__)


def get_levels(name: str) -> List[int]:
    logger.info(f'Fetching data for {name}')
    r = requests.get(f'https://playoverwatch.com/en-us/career/pc/{name}')
    if not r.status_code == 200:
        logger.error(f'Bad response r.status_code from URL')
        return [0, 0, 0]
    soup = BeautifulSoup(r.text, 'html.parser')
    rank_area = soup.find('div', class_='competitive-rank')
    if not rank_area:
        logger.error(f'Could not find competitive rank HTML section for {name}')
        return [0, 0, 0]
    ranks = []
    for role in ['Tank', 'Damage', 'Support']:
        role_section = rank_area.find('div', {'data-ow-tooltip-text': f'{role} Skill Rating'})
        if not role_section:
            logger.debug(f'Cannot find {role} section for {name}')
            ranks.append(0)
            continue
        level = int(role_section.parent.find(class_='competitive-rank-level').string)
        ranks.append(level)
    return ranks


def update(name: str) -> None:
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        levels = get_levels(name)
        writer.writerow([
            datetime.now().timestamp(),
            name,
            levels[0],
            levels[1],
            levels[2]
        ])


def load_config(file_name: str = 'config.json') -> List[str]:
    logger.info('Loading configuration')
    with open(file_name) as f:
        data = json.load(f)
        names = data['names']
        return names


def do_update() -> None:
    names = load_config()
    for name in names:
        logger.info(f'Updating data for {name}')
        update(name)
    logger.info('Done')


if __name__ == '__main__':
    do_update()
