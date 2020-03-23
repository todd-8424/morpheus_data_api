# Name: disable_plans.py
## Author: tkearney
## Date: March 2020
## Dependencies:
    1. argparse 
    2. requests
    3. json
    4. getpass
    5. urllib3

## Aruguments:
    -c is the Cloud type for the Plan

## Purpose:
    This is designed to disable plans for each type of cloud in Morpheus

## Execute:
    python disable_plans/disable_plans.py -c <CLOUD name as seen Morpheus settings under "Plans & Pricing">

## Actions and Results:
    ### Actions:
    1. The script should identify what user is logged in and ask for their password if the password is not passed script will exit()
    2. Then it will contact the morpheus api to check authorization of that user
    3. Gets a token if the user does not already have one
    4. Gets all the plans and based on what type of cloud you are looking to modify examples are (Azure, GCP, AWS)
    5. Loop through those plans and disable them

    ### Results:
    1. All plans from selected cloud will be disabled