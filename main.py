import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_DATA_API_KEY = "https://www.alphavantage.co - API_KEY"
NEWS_API_KEY = "https://newsapi.org/v2/ - API_KEY"

TWILIO_SID = "TWILIO_ACC_SID"
AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
stock_data_parameters={"function":"TIME_SERIES_DAILY",
                       "symbol":STOCK_NAME,
                       "apikey": STOCK_DATA_API_KEY
}
response = requests.get(url=STOCK_ENDPOINT,params = stock_data_parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"
diff_percent = round((difference/float(yesterday_closing_price))*100)
if abs(diff_percent)>3:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(url=NEWS_ENDPOINT,params = news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline:{article['title']}. \n Brief: {article['description']}" for article in three_articles]
    client = Client(TWILIO_SID, AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
          from_="whatsapp:TWILIO_PHONE_NUMBER",
          body=article,
          to="whatsapp:YOUR_PHONE_NUMBER"
        )

