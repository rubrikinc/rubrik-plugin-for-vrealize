#!/usr/bin/python
from urllib import response
import requests, json, sys, pprint, time, argparse
import re
import pathlib
from os import listdir
from os.path import isfile, join
from requests.auth import HTTPBasicAuth
from getpass import getpass
import pprint
pp = pprint.PrettyPrinter(indent=4)

class VRASession:

    def __init__(self,argv):
        requests.packages.urllib3.disable_warnings()
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', dest='host', help='VRA Host')
        parser.add_argument('--tenant', dest='tenant', help='VRA Tenant')
        parser.add_argument('--username', dest='username', help='VRA User')
        parser.add_argument('--password', dest='password', help='VRA Password')
        parser.add_argument('--package', dest='package', help='VRA Package Name')
        args = parser.parse_args()
        self.host = args.host
        #self.tenant = args.tenant
        self.username = args.username
        self.password = args.password
        self.packageName = args.package
        self.baseurl = "https://" + self.host

        self.token =  self.authenticate(self.host, self.username, self.password)
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.token}
        
    def checkcall(self,r):
        acceptedResponses = [200, 201, 203, 204]
        if not r.status_code in acceptedResponses:
            print("STATUS: {status} ".format(status=r.status_code))
            print("ERROR: " + r.text)
            sys.exit(r.status_code)

    def authenticate(self, host, user, password):
        refToken = self.auth_get_vra_refresh_token(host, user, password)
        #print("Refresh Token: " + refToken)
        headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        payload = {"refreshToken": refToken }
        url = 'https://' + host + '/iaas/api/login'
        r = requests.post(url=url, data=json.dumps(payload), headers=headers, verify=False)
        self.checkcall(r)
        response = r.json()
        token = 'Bearer ' + response['token']
        #print("Bearer Token: " + token)
        return token

    def auth_get_vra_refresh_token(self, host, user, password):
        headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        payload = {"username": user, "password": password}
        url = 'https://'+ host + '/csp/gateway/am/api/login?access_token'
        r = requests.post(url= url, data=json.dumps(payload), headers=headers, verify=False  )
        self.checkcall(r)
        response = r.json()
        refresh_token = response['refresh_token']
        return refresh_token


    def get_call(self, call):
        uri = self.baseurl + call
        try:
            r = requests.get(uri, verify=False, headers=self.headers)
            r.raise_for_status()

        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            print(e)
            response = r.json()
            raise self.Exception("Call Failed: " + response['message'])
        response = r.json()
        return response

    def get_call_download(self, call):
        uri = self.baseurl + call         
        print("Downloading vRA Package")
        headers = {'Accept': 'application/octet-stream', 'Authorization': self.token}
        r = requests.get(uri, stream=True, headers=headers, verify=False)
        fn = re.findall('filename=(.+)', r.headers['Content-Disposition'])[0].replace('"','')
        with open(fn, 'wb') as f:
            f.write(r.content)

    def post_call(self, call, payload):
        uri  = self.baseurl + call
        try:
            r = requests.post(uri, data=json.dumps(payload), headers=self.headers, verify=False)
            r.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            print(e)
            print(r.status_code, r.reason)
            sys.exit(1)

    def delete_call(self, call):
        uri  = self.baseurl + call
        try:
            r = requests.delete(uri, headers=self.headers, verify=False)
            r.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            print(e)
            print(r.status_code, r.reason)
            sys.exit(1)

    def import_vra_blueprints(self):
        filelist = [f for f in listdir(pathlib.Path(__file__).parent.resolve())]
        
        for output in filelist:
            if str(output).split("_")[0] == "blueprint":
                with open(output) as f:
                    d = json.load(f)
                    session.post_call("/blueprint/api/blueprints", d)
                    print("Imported blueprint: " + d["name"])
    
    def import_vra_property_groups(self):
        filelist = [f for f in listdir(pathlib.Path(__file__).parent.resolve())]
        
        for output in filelist:
            if str(output).split("_")[0] == "property":
                with open(output) as f:
                    d = json.load(f)
                    session.post_call("/properties/api/property-groups", d)
                    print("Imported property group: " + d["name"])
    
    def import_vra_resource_actions(self):
        filelist = [f for f in listdir(pathlib.Path(__file__).parent.resolve())]
        
        for output in filelist:
            if str(output).split("_")[0] == "resource":
                with open(output) as f:
                    d = json.load(f)
                    session.post_call("/form-service/api/custom/resource-actions", d)
                    print("Imported resource action: " + d["name"])

    def import_vra_catalog_sources(self):
        filelist = [f for f in listdir(pathlib.Path(__file__).parent.resolve())]
        vro = session.get_call("/iaas/api/integrations?apiVersion=2021-07-15&$filter=name%20eq%20embedded-VRO")
        #print(vro["content"][0])
        for output in filelist:
            #print(output)
            if str(output).split("_")[0] == "catalog":
                with open(output) as f:
                    d = json.load(f)
                    d["config"]["workflows"][0]["integration"]["endpointUri"] = vro["content"][0]["integrationProperties"]["apiEndpoint"]
                    d["config"]["workflows"][0]["integration"]["endpointConfigurationLink"] = "/resources/endpoints/" + vro["content"][0]["id"]
                    session.post_call("/catalog/api/admin/sources", d)
                    print("Imported catalog source: " + d["name"])

if __name__ == '__main__':
    session = VRASession(sys.argv[1:])
    session.import_vra_property_groups()
    session.import_vra_blueprints()
    session.import_vra_resource_actions()
    session.import_vra_catalog_sources()
