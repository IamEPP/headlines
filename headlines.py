""" Flask Way. Headlines App. Flask By Example ch2  """
import datetime
import feedparser
from flask import Flask, render_template, request as flask_request, make_response
import json
import urllib
from urllib import parse

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

RSS_FEEDS = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
             "cnn": "http://rss.cnn.com/rss/edition.rss",
             "fox": "http://feeds.foxnews.com/foxnews/latest",
             "iol": "http://www.iol.co.za/cmlink/1.640",
             "so": "https://stackoverflow.com/feeds"}
DEFAULTS = {"provider": "bbc",
            "city": "Duque de Caxias,BR",
            "currency_from": "GBP",
            "currency_to": "USD"}

MY_WEATHER_API_KEY = "c7b3900a6c2311047a9a958f7e413e5d"

WEATHER_URI = ("http://api.openweathermap.org/data/2.5/weather?"
               "q={}&units=metric&appid={}")

MY_CURRENCY_RATE_API_KEY = "260265bb918a42de9bb0772ae6ce76f4"

CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id={}".format(MY_CURRENCY_RATE_API_KEY)


@app.route("/")
def home():
    articles = get_news(get_requested_provider())
    weather = get_weather(get_requested_city())
    rate = get_rate(get_requested_currency_from(), get_requested_currency_to())
    simple_response = make_response(render_template("home.html",
                                                    articles=articles,
                                                    weather=weather,
                                                    currency_from=get_requested_currency_from(),
                                                    currency_to=get_requested_currency_to(),
                                                    rate=rate,
                                                    currencies=get_currencies().keys()))
    return response_with_custom_cookies_for(simple_response)


def response_with_custom_cookies_for(response):
    expires_at = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("provider", get_requested_provider(), expires=expires_at)
    response.set_cookie("city", get_requested_city(), expires=expires_at)
    response.set_cookie("currency_from", get_requested_currency_from(), expires=expires_at)
    response.set_cookie("currency_to", get_requested_currency_to(), expires=expires_at)
    return response


def get_news(feed_provider):
    """ Get the news from our feed as HMTL
    """
    feed = feedparser.parse(RSS_FEEDS[feed_provider])
    return feed["entries"]


def get_rate(frm, to):
    parsed_currencies = get_currencies()
    from_rate = parsed_currencies.get(frm.upper())
    to_rate = parsed_currencies.get(to.upper())
    return to_rate / from_rate


def get_currencies():
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()
    return json.loads(all_currency).get("rates")


def get_weather(requested_city):
    """ Get customized weather based on user input or default
    """
    requested_city = parse.quote(requested_city)
    url = WEATHER_URI.format(requested_city, MY_WEATHER_API_KEY)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None

    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]}
    return weather


def get_requested_provider():
    """Get the feed provider from request
    """
    return get_value_with_fallback("provider").lower()


def get_requested_city():
    """ Get the city based on user input
    """
    return get_value_with_fallback("city")


def get_requested_currency_from():
    return get_value_with_fallback("currency_from")


def get_requested_currency_to():
    return get_value_with_fallback("currency_to")


def get_value_with_fallback(key):
    if flask_request.args.get(key):
        return flask_request.args.get(key)
    if flask_request.cookies.get(key):
        return flask_request.cookies.get(key)
    return DEFAULTS[key]


if __name__ == "__main__":
    app.run(port=5000, debug=True)
