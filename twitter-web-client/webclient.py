from flask import *

import redis

app = Flask(__name__) 

@app.route('/')
def output_tweets(): 
    output = ''
    longestWord = ''
    totalTweets = 0
    try: 
        conn = redis.StrictRedis(host='redis', port=6379)
        for key in conn.scan_iter("log.server.tweet*"):
            value = str(conn.get(key))
            output += str(key) + "<br />" + value + "<br /> "

        for k in conn.scan_iter("tweet.longestword"):
            value = str(conn.get(k))
            longestWord += value

        for t in conn.scan_iter("twitter.totalTweets"):
            value = int(conn.get(t))
            totalTweets += value
    except Exception as ex: 
        output = 'Error: ' + str(ex)
    return render_template('index.html', message=output, longestWord=longestWord, totalTweets=totalTweets)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
