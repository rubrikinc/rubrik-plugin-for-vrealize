import requests,json,sys

def checkcall(r):
        print("Checking Call")
        acceptedResponses = [200, 201, 203, 204]
        if not r.status_code in acceptedResponses:
            print "STATUS: {status} ".format(status=r.status_code)
            print "ERROR: " + r.text
            sys.exit(r.status_code)

def authenticate(host, user, password, tenant):
        headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        payload = {"username": user, "password": password, "tenant": tenant}
        print(payload)
        url = 'https://' + host + '/identity/api/tokens'
        r = requests.post(url=url, data=json.dumps(payload), headers=headers, verify=False)
        checkcall(r)
        response = r.json()
        token = 'Bearer ' + response['id']
        return token

