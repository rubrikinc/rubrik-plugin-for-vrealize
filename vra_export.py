#!/bin/python
import requests, json, sys, pprint, time
from getpass import getpass
import pprint


class VRASession:

    def __init__(self):

        #Disable ssl warnings for Requests
        requests.packages.urllib3.disable_warnings()

        #Prompt for configuration info
        self.host = "devops-vra.rubrik.demo"
        self.baseurl = "https://devops-vra.rubrik.demo"
        self.user = "peter.milanese@rubrik.demo"
        self.password = getpass("Enter in VRA password: ")
        self.tenant = 'rubrik-devops'
        #attempt login
        self.token =  self.authenticate(self.host, self.user, self.password, self.tenant)
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.token}

    def checkcall(self,r):
        acceptedResponses = [200, 201, 203, 204]
        if not r.status_code in acceptedResponses:
            print "STATUS: {status} ".format(status=r.status_code)
            print "ERROR: " + r.text
            sys.exit(r.status_code)

    def authenticate(self, host, user, password, tenant):
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
            r = requests.get(uri, verify=False, headers=self.headers)
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

    def create_package(self,tenantId):
        list = session.get_call("/content-management-service/api/contents")
        obj = {}
        obj["contents"] = []
        for output in list['content']:
          if output['tenantId'] == tenantId:
            obj["name"]="Rubrik_Package"
            obj["description"]="Package containing Rubrik Contents"
            obj["contents"].append(output['id'])
        session.post_call("/content-management-service/api/packages",obj)


if __name__ == '__main__':
    pp=pprint.PrettyPrinter()
    session = VRASession()
#    l = session.get_call("/content-management-service/api/packages")
#    for output in l['content']:
#      if output["name"] == "Rubrik_Package":
#        session.delete_call("/content-management-service/api/packages/" + output['id'])
#    session.create_package("rubrik-devops")
    l = session.get_call("/content-management-service/api/packages")
    pp.pprint(l)
    for output in l['content']:
      if output["name"] == "Rubrik_Package":
        print("exporting package")
        session.get_call_download("/content-management-service/api/packages/" + output['id'], output['name']+".zip")
      
