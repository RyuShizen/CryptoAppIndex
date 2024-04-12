import requests
from data_management.database import AppRankTracker
from bs4 import BeautifulSoup

def current_rank_coinbase():
    url = "https://apps.apple.com/us/app/coinbase-buy-bitcoin-ether/id886427730"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        return ''.join(filter(str.isdigit, rank_text))
    return None

def current_rank_wallet():
    url = "https://apps.apple.com/us/app/coinbase-wallet-nfts-crypto/id1278383455"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        return ''.join(filter(str.isdigit, rank_text))
    return None
