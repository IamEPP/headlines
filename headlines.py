""" Flask Ninja Way. Headlines App. Flask By Example ch2  """
import feedparser
from flask import Flask

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route("/")
@app.route("/bbc")
def bbc():
    """BBC Feed"""
    return get_news("bbc")

@app.route("/cnn")
def cnn():
    """CNN Feed"""
    return get_news("cnn")

@app.route("/iol")
def iol():
    """IOL Feed"""
    return get_news("iol")

@app.route("/fox")
def fox(): 
    """Fox Feed"""
    return get_news("fox")

def get_news(provider):
    """ Get the news from our feed as HMTL"""

    feed = feedparser.parse(RSS_FEEDS[provider])
    html = get_upper_html_for(provider)
    html = html + get_articles_for(feed)
    html = html + get_lower_html()
    return html

 
def get_upper_html_for(provider):
    """Returns a string with the upper part my html page. """

    return """<html>
                    <body>
                      <h1>{0} Headlines</h1>""".format(provider.upper())


def get_articles_for(feed):
    """ Returns an HTML string with all articles separated by divs."""

    articles = ""
    for article in feed['entries']:
        articles = articles + get_article_as_html(article)
    return articles


def get_article_as_html(article):
    """Returns a single article as HTML"""

    return """
        <div>
            <b>{0}</b> 
            <i>{1}</i>
            <p>{2}</p>
        </div>
    """.format(article.get("title"), article.get("published"), article.get("summary"))


def get_lower_html():
    """Return the lower part of the HTML"""

    return """</body>
                    </html> """


if __name__ == '__main__':
    app.run(port=5000, debug=True)
