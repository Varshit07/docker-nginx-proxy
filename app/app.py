import time
import redis
import random
from flask import Flask

app = Flask(__name__)

cache = redis.Redis(host='redis', port = 6379)

cache.lpush('quotes', "To begin, begin")
cache.lpush('quotes', "The purpose of our lives is to be happy.")
cache.lpush('quotes', "We shape our tools, and thereafter our tools shape us")
cache.lpush('quotes', "We become what we behold")

def get_quote_from_redis():
    retries = 5
    quoteNumber = random.randint(0,3)
    
    while True:

        try:
            return cache.lindex('quotes',quoteNumber)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def retrieve_quote():
    quote = get_quote_from_redis()
    return quote


