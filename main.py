import requests
from twilio.rest import Client
import os

STOCK_NAME = "STOCK_NAME_AS_PER_LISTING"
COMPANY_NAME = "ENTER_COMPANY_NAME"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR_alphavantage_API_KEY"
NEWS_API = "YOUR_NEWS API_KEY"

TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH = "YOUR_TWILIO_AUTHENTICATION_CODE"


# Get yesterday's closing stock price.
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
y_closing_price = float(yesterday_data["4. close"])



# Get the day before yesterday's closing stock price
day_before_yesterday = data_list[1]
dby_closing_price = float(day_before_yesterday["4. close"])

# Find the positive difference between 1 and 2.
difference = abs(dby_closing_price - y_closing_price)
print(difference)

# Work on the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage = 1
print(percentage)
up_down = None
if percentage > 5:
    up_down = "🔺"

else:
    up_down = "🔻"


# use the News API to get articles related to the COMPANY_NAME.

if percentage > 0:

    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
        # "language": "en",
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

# Use Python slice operator to create a list that contains the first 3 articles.
    article_list = articles[:3]
    # print(article_list)

# Create a new list of the first 3 article's headline and description using list comprehension.


    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{percentage}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in article_list]
    # print(formatted_articles)

# Send each article as a separate message via Twilio.


    # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(TWILIO_SID, TWILIO_AUTH)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='GET_THIS_FROM_TWILIO',
            to='YOUR_PHONE_NUMBER'
        )
