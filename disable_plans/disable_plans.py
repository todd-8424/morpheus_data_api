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
PW = getpass.getpass(prompt='Please enter password for PR1_'+UN+'\n')
BASEURL = 'https://bbwlxp00002.bbwtest.com'
access_token = ''
client_id = 'morph-api'
plan_ids = []
enable_plan_ids = []
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
    auth = {'grant_type': 'password','scope': 'write','username': "pr1_"+UN, 'password': PW, 'client_id': client_id}
    access_token_r = requests.post(token_url, data=auth, verify=False)
    results = access_token_r.json()
    access_token = results.get('access_token')
    return access_token

def getPlans(access_token,CLOUD):
    global plan_ids
    global enable_plan_ids
    match_plan_name = ['Standard_D2ds_v5 (2 Core, 8GB Memory)','Standard_D4ds_v5 (4 Core, 16GB Memory)','Standard_D8ds_v5 (8 Core, 32GB Memory)','Standard_D16ds_v5 (16 Core, 64GB Memory)']
    headers = {'Authorization': 'BEARER '+access_token}
    plan_api_url = BASEURL+'/api/service-plans'
    params={'phrase': CLOUD, 'max': '1000'}
    r = requests.get(plan_api_url, headers=headers, params=params, verify=False )
    plans = r.json()
    serv_plans = plans.get('servicePlans')
    # print(len(serv_plans))
    for desc in serv_plans:
        desc.get('description')
        # print(desc.get('name'))
        plan_ids.append(desc.get('id'))
        for name_idx in range(len(match_plan_name)):
          if desc.get('name') == match_plan_name[name_idx]:
            enable_plan_ids.append(desc.get('id'))
            # print(desc.get('description'),'-',desc.get('id'))
            # print(enable_plan_ids)
    return enable_plan_ids, plan_ids

def disablePlan(plan_ids):
    headers = {'Authorization': 'BEARER '+access_token}
    for id in plan_ids:
        id = str(id)
        disable_plan_url = BASEURL+'/api/service-plans/'+id+'/deactivate'
        r = requests.put(disable_plan_url, headers=headers, verify=False )
        print(id, r)

def enablePlan(enable_plan_ids):
    headers = {'Authorization': 'BEARER '+access_token}
    for id in enable_plan_ids:
        id = str(id)
        enable_plan_url = BASEURL+'/api/service-plans/'+id+'/activate'
        r = requests.put(enable_plan_url, headers=headers, verify=False )
        print("Enabled plan - ",id, r)

args_parser(PW)
getToken(UN,PW)
getPlans(access_token,CLOUD)
disablePlan(plan_ids)
enablePlan(enable_plan_ids)