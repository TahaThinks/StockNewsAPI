import api_data
import requests
from datetime import datetime as dt
from datetime import timedelta
from twilio.rest import Client

day = dt.now().date()
current_day = day - timedelta(days=2)
previous_day = current_day - timedelta(days=3)

PRICE_API_KEY = api_data.PRICES_API
NEWS_API_KEY = api_data.NEWS_API

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHA_ENDPOINT_PARAMS = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK_NAME,
    'apikey': PRICE_API_KEY
}

NEWS_ENPOINT_PARAMS = {
    'q': "bitcoin",
    'from': previous_day,
    'sortBy': "popularity",
    'apiKey': NEWS_API_KEY
}

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

response = requests.get(STOCK_ENDPOINT, params=ALPHA_ENDPOINT_PARAMS)
response.raise_for_status()
daily_prices = response.json()["Time Series (Daily)"]
print(daily_prices)

# TODO 2. - Get the day before yesterday's closing stock price

current_day_close = float(daily_prices[str(current_day)]["4. close"])
previous_day_close = float(daily_prices[str(previous_day)]["4. close"])
print(f"Current Price {current_day_close}")
print(f"Previous Price {previous_day_close}")

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
closing_price_diff = abs(current_day_close - previous_day_close)

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage = round((closing_price_diff / previous_day_close) * 100, 2)
print(f"Percentage: {percentage}")

articles = []

if percentage > 1:
    print("Getting NEWS")
    response = requests.get(NEWS_ENDPOINT, params=NEWS_ENPOINT_PARAMS)
    response.raise_for_status()
    articles = response.json()["articles"][:3]
    print(articles)

account_sid = api_data.TWILIO_ACCOUNT_SID
auth_token = api_data.TWILIO_TOKEN

client = Client(account_sid, auth_token)

for article in articles:
    message = client.messages.create(
                                  body=f'{STOCK_NAME} {percentage}%\n'
                                       f'Headline:{article["title"]}\n'
                                       f'Brief{article["description"]}\n'
                                       f'by TahaLearns',
                                  from_=f'whatsapp:{api_data.TWILIO_NUMBER}',
                                  to=f'whatsapp:{api_data.MY_NUMBER}'
                              )
    print(message.sid)

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
