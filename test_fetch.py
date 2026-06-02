import urllib.request, urllib.error, json

def get_users():
    url='http://127.0.0.1:5000/api/users'
    with urllib.request.urlopen(url, timeout=5) as r:
        data=json.loads(r.read().decode())
        print('GET /api/users ->', len(data), 'users')
        print(data[:3])


def create_user():
    url='http://127.0.0.1:5000/api/users'
    payload = json.dumps({"name":"TEST_USER","age":30}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=5) as r:
        print('POST /api/users ->', r.status)
        print(json.loads(r.read().decode()))


if __name__ == '__main__':
    try:
        get_users()
        create_user()
        get_users()
    except Exception as e:
        print('ERROR', repr(e))
