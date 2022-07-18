#!/usr/bin/python
from urllib import response
import requests, json, sys, pprint, time, argparse
import re
import yaml
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
        
        #if self.tenant:
        #    self.token =  self.authenticate(self.host, self.username, self.password, self.tenant)
        #    self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.token}
        #else:
        #    self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

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

    def get_vra_blueprints(self):
        list = session.get_call("/blueprint/api/blueprints?search=%20-%20Rubrik")
        obj = {}
        obj["data"] = []
        for output in list['content']:
            bp = session.get_call("/blueprint/api/blueprints/" + output['id'])
            print("Exporting Blueprint: " + bp['name'])
            entity = {}
            entity['name'] = bp['name']
            entity['description'] = bp['description']
            entity['projectId'] = bp['projectId']
            entity['content'] = bp['content']
            with open("blueprint_"+ entity['name'] +".json", 'w') as outfile:
                json.dump(entity, outfile, indent="\t")
    
    def get_vra_resource_actions(self):
        list = session.get_call("/form-service/api/custom/resource-actions?name=Rubrik")
        obj = {}
        obj["data"] = []
        for output in list['content']:
            print("Exporting Resource Action: " + output["name"])
            del(output["orgId"])
            del(output["formDefinition"]["id"])
            del(output["formDefinition"]["tenant"])
            with open("resource_action_"+ output['name']+ ".json", 'w') as outfile:
                json.dump(output, outfile, indent="\t")
    
    def get_vra_property_groups(self):
        list = session.get_call("/properties/api/property-groups")
        for output in list["content"]:
            print("Exporting Property Group: " + output["name"])
            del(output["id"])
            del(output["createdAt"])
            del(output["createdBy"])
            del(output["updatedAt"])
            del(output["updatedBy"])
            del(output["orgId"])
            with open("property_group_" + output['name'] + ".json", 'w') as outfile:
                json.dump(output, outfile, indent="\t")
    
    def get_vra_catalog_sources(self):
        list = session.get_call("/catalog/api/admin/sources?%24skip=0&%24top=0&search=Rubrik%20-%20")
        for output in list["content"]:
            print("Exporting Service Broker Catalog Source: " + output["name"])
            del(output["id"])
            del(output["createdAt"])
            del(output["createdBy"])
            del(output["lastUpdatedAt"])
            del(output["config"]["workflows"][0]["integration"]["endpointUri"])
            del(output["config"]["workflows"][0]["integration"]["endpointConfigurationLink"])
            del(output["itemsImported"])
            del(output["itemsFound"])
            del(output["lastImportStartedAt"])
            del(output["lastImportCompletedAt"])
            del(output["lastImportErrors"])
            with open("catalog_source_" + output['name'] + ".json", 'w') as outfile:
                json.dump(output, outfile, indent="\t")

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
        l = session.get_call("/content-management-service/api/packages")
        for output in l['content']:
          if output["name"] == self.packageName:
            session.delete_call("/content-management-service/api/packages/" + output['id'])

    def download_package(self):
        l = session.get_call("/content-management-service/api/packages")
        for output in l['content']:
          if output["name"] == self.packageName:
            session.get_call_download("/content-management-service/api/packages/" + output['id'])

    def download_vro(self):
        session.get_call_download("/vco/api/packages/com.rubrik.devops?exportConfigurationAttributeValues=false&exportGlobalTags=false&exportVersionHistory=true&exportConfigSecureStringAttributeValues=false")

if __name__ == '__main__':
    session = VRASession(sys.argv[1:])
    #pp.pprint(sys.argv)
    #session.delete_package()
    #session.create_package()
    #session.download_package()
    session.get_vra_blueprints()
    session.get_vra_resource_actions()
    session.download_vro()
    session.get_vra_property_groups()
    session.get_vra_catalog_sources()