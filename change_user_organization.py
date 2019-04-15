#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from pprint import pprint


gsuite_data_file = None
user_data_file = None
output_data_file = None

unit_names = ['CTH','Chalmers'] # Find this in the user_data_file
new_org_unit = '/Local Groups/Chalmers' # Change to this in the G-suite data

if len(sys.argv) < 3:
    print("Error! Too few arguments given!")
    exit()

gsuite_data_file = sys.argv[1] # Full list of all G-suite accounts
user_data_file = sys.argv[2] # List from the old system
output_data_file = sys.argv[3] # Output file, csv-encoded


# Add all users to an array, easier to work with
gsuite_header_row = ''
gsuite_data = []

with open(gsuite_data_file,'r') as data_file:
    gsuite_header_row = data_file.readline()
    for data in data_file:
        gsuite_data.append(data.strip().split(','))

user_data = []
updated_user_data = []


# Find the users we want to update
with open(user_data_file,'r') as data_file:
    for data in data_file:
        user_data.append(data.strip().split('\t'))
        if user_data[-1][-1] in unit_names:
            new_data = user_data[-1]
            new_data[2] = new_data[2].lower()
            if '@ingenjorerutangranser.se' in  new_data[2]:
                new_email = new_data[2].split('@')
                new_email[1] = '@ewb-swe.org'
                new_data[2] = ''.join(new_email) 
            new_data[5] = new_org_unit
            updated_user_data.append(new_data)


# Write to file
print('Updated users:')
with open(output_data_file,'w') as output_file:
    output_file.write(gsuite_header_row)
    for new_data in updated_user_data:
        user_found = False
        for old_gsuite in gsuite_data:
            if new_data[2] in old_gsuite and new_data[2]:
                print('{}: {} -> {}'.format(new_data[2], old_gsuite[5], new_org_unit))
                new_gsuite = old_gsuite
                new_gsuite[5] = new_org_unit
                output_file.write(','.join(new_gsuite) + '\n')
                user_found = True
        if not user_found:
            print('Could not find user "{}"'.format(new_data[2]))

#pprint(updated_user_data)
#print(len(gsuite_data))
