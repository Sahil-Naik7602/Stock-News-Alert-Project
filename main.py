import requests
import math
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

account_sid = "**************"
auth_token  = "***************"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
ALPHAVANTAGE_API_KEY = "*************"
parameters_alphavantage = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "outputsize":"compact",
    "apikey":ALPHAVANTAGE_API_KEY
}
response_alphavantage = requests.get(url="https://www.alphavantage.co/query",params=parameters_alphavantage)
response_alphavantage.raise_for_status()
stock_data = response_alphavantage.json()
stock_data_in_list_form = [value for(key,value) in stock_data["Time Series (Daily)"].items()]

the_day_closing_data = float(stock_data_in_list_form[1]["4. close"])
last_day_closing_data = float(stock_data_in_list_form[2]["4. close"])

print(math.fabs(the_day_closing_data-last_day_closing_data)/last_day_closing_data*100)#------------>Just for testing the code
today_date = dt.datetime.now()

percentage_change = math.fabs(the_day_closing_data-last_day_closing_data)/last_day_closing_data*100

if percentage_change<=5:
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    NEWS_API = "************************"
    
    new_parameters = {
        "q":COMPANY_NAME,
        "from":today_date.date() ,
        "sortBy":"popularity",
        "apiKey":NEWS_API
        }
    response_news = requests.get(url=f"https://newsapi.org/v2/everything", params=new_parameters)
    response_news.raise_for_status()
    news_data = response_news.json()["articles"]
    for data in news_data[:3]:
        ## STEP 3: Use https://www.twilio.com
        ## Send a seperate message with the percentage change and each article's title and description to your phone number. 
        client = Client(account_sid, auth_token)
        if last_day_closing_data>the_day_closing_data:
            message = client.messages.create(
                to="+917978623593", 
                from_="+16067311819",
                body=f"""
                    \n{STOCK}: 🔺{percentage_change}%
                \nHeadline: {data["title"]} 
                \nBrief: {data["description"]}
                    """
                )
        elif last_day_closing_data<the_day_closing_data:
             message = client.messages.create(
                to="+917978623593", 
                from_="+16067311819",
                body=f"""
                    \n{STOCK}: 🔻{percentage_change}%
                \nHeadline: {data["title"]} 
                \nBrief: {data["description"]}
                    """
                )
        print(message.status)
        



