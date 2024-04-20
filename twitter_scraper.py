import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
import time
from twikit import Client
import json
import pandas as pd

client = Client('en-US')


# enter username and pass for x account
client.login(auth_info_1='*****', password='88888')
client.save_cookies('cookies.json')
client.load_cookies(path='cookies.json')


def extract_usernames(account_urls):
    usernames = []
    for url in account_urls:
        # Split the URL by '/'
        parts = url.split('/')
        # The username is the last part of the URL
        username = parts[-1]
        usernames.append(username)
    return usernames


# List of Twitter account URLs
account_urls = [
    "https://twitter.com/Mr_Derivatives",
    "https://twitter.com/warrior_0719",
    "https://twitter.com/ChartingProdigy",
    "https://twitter.com/allstarcharts",
    "https://twitter.com/yuriymatso",
    "https://twitter.com/TriggerTrades",
    "https://twitter.com/AdamMancini4",
    "https://twitter.com/CordovaTrades",
    "https://twitter.com/Barchart",
    "https://twitter.com/RoyLMattox"
]

# Extract usernames
usernames = extract_usernames(account_urls)
print("Usernames:", usernames)


def extract_stock_symbols(tweet):
    # Regular expression to match stock symbols
    pattern = r'\$\w{3,4}'
    return re.findall(pattern, tweet)


# Example usage:
# tweet = "I'm bullish on $AAPL and $TSLA!"
# symbols = extract_stock_symbols(tweet)
# print("Stock Symbols:", symbols)


def count_stock_mentions(user):

    tweets = user.get_tweets('Tweets', count=5)

    all_stock_symbols = []
    for tweet in tweets:

        print(tweet.full_text)
        if tweet.full_text:
            stock_symbols = extract_stock_symbols(tweet.full_text)
            all_stock_symbols.extend(stock_symbols)

    stock_symbol_counts = Counter(all_stock_symbols)
    for symbol, count in stock_symbol_counts.items():
        print(f"'{symbol}' was mentioned '{count}' times")


def display_results(symbol, count, interval_minutes):
    print(f"'{symbol}' was mentioned '{count}' times in the last '{interval_minutes}' minutes.")


# Example usage:
# display_results("$TSLA", 10, 15)


def scrape_twitter_accounts(username, ticker, interval_minutes):
    while True:
        for username in usernames:
            user = client.get_user_by_screen_name(username)
            if user:
                print(f"Scraping {username}:")
                count = count_stock_mentions(user)
                display_results(ticker, count, interval_minutes)
                print("=" * 50)
            else:
                print(f"Failed to scrape {username}")

        # Wait for the specified interval before scraping again
        print(
            f"Waiting for {interval_minutes} minutes before the next scraping session...")
        time.sleep(interval_minutes * 60)  # Convert minutes to seconds


ticker = "$TSLA"
interval_minutes = 15
scrape_twitter_accounts(usernames, ticker, interval_minutes)
