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

UN = getpass.getuser()
PW = getpass.getpass(prompt='Please enter password for '+UN)
BASEURL = ''
access_token = ''
client_id = 'morph-api'
plan_ids = []
CLOUD = ''

def args_parser(PW):
  global CLOUD
  if PW == '':
      print('No password for user')
      exit()
  parser = argparse.ArgumentParser(description='Disable CLOUD Plans in Morpheus')
  parser.add_argument("-c",help="Please enter CLOUD name")
  args = parser.parse_args()
  CLOUD = args.c
  if CLOUD is None:
    print('No CLOUD name given please add -c <CLOUD name as seen Morpheus settings under "Plans & Pricing">')
    exit()
  return CLOUD

def getToken(UN,PW):
    global access_token
    token_url = BASEURL+"/oauth/token"
    auth = {'grant_type': 'password','scope': 'write','username': UN, 'password': PW, 'client_id': client_id}
    access_token_r = requests.post(token_url, data=auth, verify=False)
    results = access_token_r.json()
    access_token = results.get('access_token')
    return access_token

def getPlans(access_token,CLOUD):
    global plan_ids
    headers = {'Authorization': 'BEARER '+access_token}
    plan_api_url = BASEURL+'/api/service-plans'
    params={'phrase': CLOUD, 'max': '1000'}
    r = requests.get(plan_api_url, headers=headers, params=params, verify=False )
    plans = r.json()
    serv_plans = plans.get('servicePlans')
    print(len(serv_plans))
    for desc in serv_plans:
        desc.get('description')
        print(desc.get('name'))
        plan_ids.append(desc.get('id'))
    return plan_ids

def disablePlan(plan_ids):
    headers = {'Authorization': 'BEARER '+access_token}
    for id in plan_ids:
        id = str(id)
        disable_plan_url = BASEURL+'/api/service-plans/'+id+'/deactivate'
        r = requests.put(disable_plan_url, headers=headers, verify=False )
        print(id, r)

args_parser(PW)
getToken(UN,PW)
getPlans(access_token,CLOUD)
disablePlan(plan_ids)