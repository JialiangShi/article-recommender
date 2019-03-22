# article-recommender
Recommend BBC news articles based on gloves word embeddings

The goal of this project is to make a simple article recommendation engine using a semi-recent advance in natural language processing called [word2vec](http://arxiv.org/pdf/1301.3781.pdf) (or just *word vectors*). In particular, we're going to use a "database" from [Stanford's GloVe project](https://nlp.stanford.edu/projects/glove/) trained on a dump of Wikipedia. The project involves reading in a database of word vectors and a corpus of text articles then organizing them into a handy table (list of lists) for processing.

Around the recommendation engine, you are going to build a web server that displays a list of [BBC](http://mlg.ucd.ie/datasets/bbc.html) articles for URL `http://localhost:5000` (testing) or whatever the IP address is of your Amazon server (deployment):

<img src=figures/main_page.png width=400>

Clicking on one of those articles takes you to an article page that shows the text of the article as well as a list of five recommended articles:

<img src=figures/article1.png width=450>

<img src=figures/article2.png width=450>

## Launching your server at Amazon

Creating a server that has all the appropriate software can be tricky so I have recorded a sequence that works for me.

Creating a server that has all the appropriate software can be tricky so I have recorded a sequence that works for me.

The first thing is to launch a server with different software than the simple Amazon linux. We need one that has, for example, `numpy` and friends so let's use an *image* (snapshot of a disk with a bunch of stuff installed) that already has machine learning software installed: Use "*Ubuntu Server 16.04 LTS (HVM), SSD Volume Type*":

Create a `t2.medium` size computer (in Oregon; it's cheaper)!

When you try to connect, it will tell you to use user `root` but use `ec2-user` like we did for the other machines.  In other words, here's how I login:

```bash
$ ssh -i "mykey.pem" ec2-user@34.203.194.19
```

Once connected to AWS, we need to install anaconda:

Or, another student had good luck with the following process:

Then install software we need:

```
sudo apt update
sudo apt install python3-pip
sudo apt install unzip
```
Then we can begin to intall the Python packages we need:

```
pip3 install numpy
pip3 install gunicorn
pip3 install flask
```

Now, clone your repository into the home directory:

```bash
cd ~
git clone https://github.com/JialiangShi/article-recommender.git
cd article-recommender
```

Now, download the data you need and unzip:

```bash
wget https://s3-us-west-1.amazonaws.com/msan692/glove.6B.300d.txt.zip
wget https://s3-us-west-1.amazonaws.com/msan692/bbc.zip
unzip glove.6B.300d.txt.zip
unzip bbc.zip
```

You should now be able to run your server:

```bash
$ gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc
```

All output goes into `server.log`, even after you log out. The `-D` means put the server in daemon mode, which runs the background.

Don't forget to open up port 5000 in the firewall for the server so that the outside world can access it. Make sure that you test from your laptop!

Make sure the `IP.txt` file as the **public** IP address of your server with `:5000` on the line by itself, such as `54.198.43.135:5000`!
