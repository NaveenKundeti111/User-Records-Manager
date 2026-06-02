import urllib.request, urllib.error, sys
url='http://127.0.0.1:5000/api/users'
try:
    with urllib.request.urlopen(url, timeout=5) as r:
        data = r.read()
        print('STATUS', r.status)
        print(data.decode('utf-8')[:800])
except Exception as e:
    print('ERROR', repr(e))
    sys.exit(1)
