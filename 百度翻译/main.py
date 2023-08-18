import execjs
import requests
import urllib3

urllib3.disable_warnings()


class BaiDUTransAPI:
    def __init__(self, query, from_="zh", to="en", proxy=None, verify=False, is_proxy=False):
        self.query = query
        self.data = {
            "from": "zh",
            "to": "en",
            "query": self.query,
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": self.getSign(),
            "token": "66449cd19d085e336ff09ee40777dce2",
            "domain": "common",
            "ts": "1692322511114"
        }
        self.url = "https://fanyi.baidu.com/v2transapi?from={}&to={}".format(from_, to)
        self.cookies = {
            "BAIDUID": "340F498BD2E32B13160D6D4953434E88:FG=1",
        }
        self.proxy = proxy or {
            "http": "http://127.0.0.1:8888",
            "https": "http://127.0.0.1:8888"
        }
        self.verify = verify
        self.is_proxy = is_proxy

    def getSign(self):
        with open('./sign.js', 'r', encoding='utf-8') as f:
            cxt = execjs.compile(f.read())
            sign = cxt.call("getSign", self.query)
            return sign

    def getResults(self):
        res = None
        if self.is_proxy:
            res = requests.post(url=self.url, data=self.data, cookies=self.cookies, verify=self.verify,
                                proxies=self.proxy)
        else:
            res = requests.post(url=self.url, data=self.data, cookies=self.cookies, verify=self.verify)
        result = []
        for item in res.json()['trans_result']['data']:
            result.append(item['dst'])
        return result


if __name__ == '__main__':
    API = BaiDUTransAPI(query="第一")
    print(API.getResults())
