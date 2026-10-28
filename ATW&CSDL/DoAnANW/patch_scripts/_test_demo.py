import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

res = urllib.request.urlopen('http://127.0.0.1:8000/api/auth/demo-accounts')
print(json.dumps(json.loads(res.read()), indent=2, ensure_ascii=False))
