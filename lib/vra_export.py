#!/bin/python
import requests, json, sys, pprint, time,argparse
from requests.auth import HTTPBasicAuth
from getpass import getpass
import pprint
pp = pprint.PrettyPrinter(indent=4)


class VRASession:

    def __init__(self,argv):

        #Disable ssl warnings for Requests
        requests.packages.urllib3.disable_warnings()
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', dest='host', help='VRA Host')
        parser.add_argument('--tenant', dest='tenant', help='VRA Tenant')
        parser.add_argument('--username', dest='username', help='VRA User')
        parser.add_argument('--password', dest='password', help='VRA Password')
        parser.add_argument('--package', dest='package', help='VRA Package Name')
        args = parser.parse_args()
        self.host = args.host
        self.tenant = args.tenant
        self.username = args.username
        self.password = args.password
        self.packageName = args.package
        self.baseurl = "https://" + self.host
        if self.tenant in locals() or self.tenant in globals():
            self.token =  self.authenticate(self.host, self.username, self.password, self.tenant)
            self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.token}
        else:
            self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def checkcall(self,r):
        acceptedResponses = [200, 201, 203, 204]
        if not r.status_code in acceptedResponses:
            print "STATUS: {status} ".format(status=r.status_code)
            print "ERROR: " + r.text
            sys.exit(r.status_code)

    def authenticate(self, host, user, password, tenant):
        if tenant:
            headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
            payload = {"username": user, "password": password, "tenant": tenant}
            url = 'https://' + host + '/identity/api/tokens'
            r = requests.post(url=url, data=json.dumps(payload), headers=headers, verify=False)
            self.checkcall(r)
            response = r.json()
            token = 'Bearer ' + response['id']
        return token

    def get_call(self, call):
        uri = self.baseurl + call
        try:
            if self.tenant in locals() or self.tenant in globals():
                r = requests.get(uri, verify=False, headers=self.headers,auth=self.auth)
            else:
                r = requests.get(uri, verify=False, headers=self.headers,auth=(self.username,self.password))
            r.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            print e
            response = r.json()
            raise self.Exception("Call Failed: " + response['message'])
        response = r.json()
        return response

    def get_call_download(self, call, fn):
        uri = self.baseurl + call
        headers = {'Accept': 'application/zip', 'Authorization': self.token}
        r = requests.get(uri, stream=True, headers=headers, verify=False)
        with open(fn, 'wb') as f:
            f.write(r.content)

    def post_call(self, call, payload):
        uri  = self.baseurl + call
        try:
            r = requests.post(uri, data=json.dumps(payload), headers=self.headers, verify=False)
            r.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            print e
            print r.status_code, r.reason
            sys.exit(1)

    def delete_call(self, call):
        uri  = self.baseurl + call
        try:
            r = requests.delete(uri, headers=self.headers, verify=False)
            r.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            print e
            print r.status_code, r.reason
            sys.exit(1)

    def create_package(self):
        list = session.get_call("/content-management-service/api/contents?limit=200")
        obj = {}
        obj["contents"] = []
        for output in list['content']:
          print("Checking " + output['name'])
          if (output['tenantId'] == self.tenant) and ("ubrik" in output['name']):
            print("SAVING ********************************************")
            obj["name"]=self.packageName
            obj["description"]=self.packageName
            obj["contents"].append(output['id'])
        session.post_call("/content-management-service/api/packages",obj)

    def delete_package(self):
       # l = session.get_call("/content-management-service/api/packages")
        for output in l['content']:
          if output["name"] == self.packageName:
            session.delete_call("/content-management-service/api/packages/" + output['id'])

    def download_package(self):
        l = session.get_call("/content-management-service/api/packages")
        for output in l['content']:
          if output["name"] == self.packageName:
            session.get_call_download("/content-management-service/api/packages/" + output['id'], output['name']+".zip")
            print(output['name']+".zip")

    def download_vro(self):
        l = session.get_call("/vco/api/packages/com.rubrik.devops?exportConfigurationAttributeValues=false&exportGlobalTags=false&exportVersionHistory=true&exportAsZip=true&exportConfigSecureStringAttributeValues=false")


if __name__ == '__main__':
    session = VRASession(sys.argv[1:])
    if tenant in locals() or tenant in globals():
        session.delete_package()
        session.create_package()
        session.download_package()
    else:
        session.download_vro()
        
      
