import requests

try:
    res = requests.get("https://httpbin.org/ip")
    print("通信成功 ✅")
    print(res.text)
except Exception as e:
    print("通信に失敗 ❌")
    print(e)
