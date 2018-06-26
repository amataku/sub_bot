import json, config
import MeCab
import random
from requests_oauthlib import OAuth1Session

mec = MeCab.Tagger()
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)
url = 'https://api.twitter.com/1.1/search/tweets.json'
url_send = 'https://api.twitter.com/1.1/statuses/update.json'

def get_tweet():
    query = 'ちゃった exclude:retweets exclude:replies -from:bang_subbot'
    params = {
        'q': query,
        'count': 1
    }

    res = twitter.get(url, params = params)
    result = []

    if res.status_code == 200:
        tweets = json.loads(res.text)
        result = tweets['statuses']
    else:
        print("Fail : %d"% res.status_code)

    for r in result:
        for k,v in r.items():
            if k in ['text']:
                print(v)
                return(v)

def check_tweet():
    tango = []
    hinsi = []
    gen = []
    tango_rev = []
    hinsi_rev = []
    gen_rev = []
    tango_huk = []
    i = 0
    j = 0
    get = get_tweet()
    result = mec.parse(get)
    big = result.split("\n")
    big.remove("EOS")
    big.remove("")
    ##配列検索
    for lis in big:
        tango.append(lis.split("\t")[0])
        hinsi.append(lis.split("\t")[1].split(",")[0])
        gen.append(lis.split("\t")[1].split(",")[6])
        if gen[i] == "ちゃう":
            break
        i = i + 1
    ##配列逆順
    for lis in (reversed(tango)):
        tango_rev.append(lis)
    for lis in (reversed(hinsi)):
        hinsi_rev.append(lis)
    ##助詞・記号で検索
    for lis in hinsi_rev:
        if lis == "助詞" or lis == "記号":
            if tango_huk[-1] == "ちゃっ" or tango_huk[-1] == "ちゃう":
                return tango_rev
            else:
                return tango_huk
        else:
            tango_huk.append(tango_rev[j])
        j = j + 1
    return tango_huk


def send_tweet():
    result = ""
    res_rev = []
    num = random.randint(1, 998)
    res = check_tweet()
    for lis in (reversed(res)):
        res_rev.append(lis)
    res_text = ''.join(res_rev)
    result = "第"+ str(num) + "話 " + res_text + "た！"
    params = {"status": result}
    req = twitter.post(url_send, params = params)
    if req.status_code == 200:
        print("send")
    else:
        print("Error: %d"% req.status_code)

send_tweet()
