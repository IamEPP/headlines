""" Flask Ninja Way. Headlines App. Flask By Example ch2  """
import feedparser
from flask import Flask, render_template


app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'so' : 'https://stackoverflow.com/feeds'}


@app.route("/")
@app.route("/<provider>")
def get_news_from(provider="bbc"):
    """ Get the news from our feed as HMTL"""
    feed = feedparser.parse(RSS_FEEDS[provider]) 
    return render_template("home.html", articles=feed['entries'])



if __name__ == '__main__':
    app.run(port=5000, debug=True)
