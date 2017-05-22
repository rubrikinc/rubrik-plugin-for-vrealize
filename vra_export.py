import requests, json, sys, pprint, time
from getpass import getpass
from helpers import authenticate, checkcall


class VRASession:

    def __init__(self):

        #Disable ssl warnings for Requests
        requests.packages.urllib3.disable_warnings()

        #Prompt for configuration info
        self.host = "devops-vra.rubrik.demo"
        self.user = "peter.milanese@rubrik.demo"
        self.password = getpass("Enter in VRA password: ")
        self.tenant = 'rubrik'
        #attempt login
        self.token = authenticate(self.host, self.user, self.password, self.tenant)

if __name__ == '__main__':

    token = VRASession()
