# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    return render_template('articles.html', articles = myarticles)

@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    i = filenames.index(topic + '/' + filename)
    contents = myarticles[i][2]
    title = myarticles[i][1]
    article = myarticles[i]
    recommends = recommended(article, myarticles, 5)
    return render_template('article.html', title = title, contents = contents, recommends = recommends)



# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
myarticles = load_articles(articles_dirname, gloves)
filenames = [a[0] for a in myarticles]
#titles = [a[1] for a in articles]
#contents = [a[2] for a in articles]
