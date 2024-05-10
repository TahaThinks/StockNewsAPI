import api_data
import requests
from datetime import datetime as dt
from datetime import timedelta

day = dt.now().date()
current_day = day - timedelta(days=1)
previous_day = current_day - timedelta(days=1)

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

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if percentage > 1:
    print("Get NEWS")
    response = requests.get(NEWS_ENDPOINT, params=NEWS_ENPOINT_PARAMS)
    response.raise_for_status()
    print(response.json())

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


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
