import urllib3
def connectionHttp(username : str, password : str,address :str):
    http = urllib3.PoolManager()
    url = address
    headers = urllib3.util.make_headers(basic_auth=username+':'+password)
    r = http.request('GET', url, headers=headers)
    print(r.data)
    print(r.status)
