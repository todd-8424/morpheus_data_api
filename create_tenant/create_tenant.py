"""
Name: disable_plans.py
Author: tkearney
Date: March 2020
Version: 0.0.1
Purpose: Disable plans in Morpheus through the API
"""
import argparse
import requests
import json
import getpass
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#UN = getpass.getuser()
#UN = ''
UN = 'tkearney'
PW = getpass.getpass(prompt='Please enter password for '+UN)
BASEURL = 'https://morpheus.k24.lan'
access_token = ''
client_id = 'morph-api'
plan_ids = []
TENANT = ''

def args_parser(PW):
  global TENANT
  if PW == '':
      print('No password for user')
      exit()
  parser = argparse.ArgumentParser(description='Create Tenant')
  parser.add_argument("-n",help="Please enter Tenant name")
  args = parser.parse_args()
  TENANT = args.n
  if TENANT is None:
    print('No TENANT name given please add -n and supply the name')
    exit()
  return TENANT

def getToken(UN,PW):
    global access_token
    token_url = BASEURL+"/oauth/token"
    auth = {'grant_type': 'password','scope': 'write','username': UN, 'password': PW, 'client_id': client_id}
    access_token_r = requests.post(token_url, data=auth, verify=False)
    results = access_token_r.json()
    access_token = results.get('access_token')
    return access_token

def createTenant(access_token, TENANT):
    headers = {'Authorization': 'BEARER '+access_token}
    tenant_api_url = BASEURL+'/api/accounts'
    params={'max': '1000'}
    data="{'account':{'name': "+TENANT+" }}"
    r = requests.post(tenant_api_url, headers=headers, params=params, data=data, verify=False)
    tenants = r.json()
    print(json.dumps(tenants, indent=4))

def createGroup(access_token, TENANT):
    headers = {'Authorization': 'BEARER '+access_token}
    tenant_api_url = BASEURL+'/api/groups'
    params={'max': '1000'}
    data="{'group':{'name': "+TENANT+" }}"
    r = requests.post(tenant_api_url, headers=headers, params=params, data=data, verify=False)
    tenants = r.json()
    print(json.dumps(tenants, indent=4))

args_parser(PW)
getToken(UN,PW)
createTenant(access_token,TENANT)
createGroup(access_token,TENANT)