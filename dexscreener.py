import logging
import websockets
import json
import os
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("URI")

dexscreener_headers = {
    "GET": "wss://io.dexscreener.com/dex/screener/pairs/h24/1?rankBy[key]=txns&rankBy[order]=desc HTTP/1.1",
    "Host": "io.dexscreener.com",
    "Connection": "Upgrade",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade": "websocket",
    "Origin": "https://dexscreener.com",
    "Sec-WebSocket-Version": "13",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-GPC": "1",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"
}


def format_number(number):
    if number >= 10000000:
        if number % 10000000 == 0:
            return '{}B'.format(round(number / 10000000))
        else:
            return '{}B'.format(round(number / 10000000, 1))
    elif number >= 1000000:
        if number % 1000000 == 0:
            return '{}M'.format(round(number / 1000000))
        else:
            return '{}M'.format(round(number / 1000000, 1))
    else:
        return '{}K'.format(round(number / 1000))


def create_link_for_pair(chain, pair_contract, baseToken, quoteToken, discord=False):
    created_link = 'https://dexscreener.com/{}/{}'.format(chain, pair_contract)
    connected_pair = baseToken + '/' + quoteToken
    if discord:
        pair_with_html = '[{}]({})'.format(connected_pair, created_link)
    else:
        pair_with_html = "<a href='{}'>{}</a>".format(created_link, connected_pair)
    return pair_with_html


def format_data_into_message(gainers_data, losers_data, limit, discord):
    data_gainers = '\n🟢 Daily gainers 🟢'
    data_losers = '\n\n🔴 Daily losers 🔴'

    general_stats = "📊 Daily stats\nTransactions: {}\nVolume: ${}\n".format(
        format_number(gainers_data['stats']['h24']['txns']),
        format_number(round(gainers_data['stats']['h24']['volumeUsd'])))

    for pair, position in zip(gainers_data['pairs'][0:limit], range(limit)):
        pair_with_link = create_link_for_pair(pair['chainId'], pair['pairAddress'], pair['baseToken']['symbol'],
                                              pair['quoteToken']['symbol'], discord)
        data_gainers += '\n{}. {} +{}% (Market Cap: ${})'.format(position + 1,
                                                                 pair_with_link,
                                                                 format_number(round(pair['priceChange']['h24'])),
                                                                 format_number(pair['marketCap']))

    for pair, position in zip(losers_data['pairs'][0:limit], range(10)):
        pair_with_link = create_link_for_pair(pair['chainId'], pair['pairAddress'], pair['baseToken']['symbol'],
                                              pair['quoteToken']['symbol'], discord)
        data_losers += '\n{}. {} {}% (Market Cap: ${})'.format(position + 1,
                                                               pair_with_link,
                                                               format_number(round(pair['priceChange']['h24'])),
                                                               format_number(pair['marketCap']))
    return general_stats + data_gainers + data_losers


async def get_data(uri):
    async with websockets.connect(uri=uri, extra_headers=dexscreener_headers) as websocket:
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
            except TypeError:
                pass

            if bool(data):
                break
            else:
                logging.error("No data in response from DEXscreener")
                continue
    return data


async def get_message_from_dexscreener(discord=False):
    gainers_data = await get_data(URI.format('desc'))
    losers_data = await get_data(URI.format('asc'))
    message = format_data_into_message(gainers_data, losers_data, 10, discord)
    return message
