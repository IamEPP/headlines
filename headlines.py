""" Flask Ninja Way. Headlines App. Flask By Example ch2  """
import feedparser
from flask import Flask

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"


@app.route("/")
def get_news():
    """ Get the news from our feed and generate HMTL"""
    feed = feedparser.parse(BBC_FEED)
    articles = """<html>
                    <body>
                      <h1>BBC Headlines</h1>"""
                 
    for article in feed['entries']:
        articles = articles + """
                <div>
                    <b>{0}</b> 
                    <i>{1}</i>
                    <p>{2}</p>
                </div>
        """.format(article.get("title"), article.get("published"), article.get("summary"))

    articles = articles + """</body>
                    </html> """

    return articles


if __name__ == '__main__':
    app.run(port=5000, debug=True)
