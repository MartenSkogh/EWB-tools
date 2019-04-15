#! /usr/bin/env/python3
# -*- encding:utf-8 -*-

import datetime
from pprint import pprint
from operator import itemgetter


filename = "userdata.csv"
updated_emails_file = "emails_to_update.txt"
outpufilename = "updated_users.csv"

fields = ['first name', 
          'last name', 
          'email adress',
          'password',
          'password hash function',
          'org unit path',
          'new primary email',
          'home secondary email',
          'work secondary email',
          'work phone',
          'home phone',
          'mobile phone',
          'work adress',
          'home adress',
          'employee id',
          'employee type',
          'employee title',
          'manager email',
          'department',
          'cost center',
          'building id',
          'floor name',
          'floor section',
          'change password at next sign-in']

headers = []
users = []


with open(filename, 'r', encoding='utf8') as f:
    headers = f.readline().strip().split(',')
    for line in f:
        user_values = line.strip().split(',')
        users.append( {field: value for (field, value) in zip(fields,user_values)} )

with open(outpufilename, 'w+', encoding='utf8') as output_file:
    with open(updated_emails_file, 'w', encoding='utf8') as email_file:
        header_row = ','.join(headers)
        output_file.write(header_row + '\n')
        for user in users:
            current_email = user['email adress']
            if '@ingenjorerutangranser.se' in current_email:
                # Write the current emails to a file so they can be contacted 
                email_file.write(current_email + ',\n')
                user_name = current_email.split('@')[0]
                new_email = user_name + '@ewb-swe.org'
                user['new primary email'] = new_email
                user['change password at next sign-in'] = 'False'
                text_row = ','.join(val for val in user.values())
                output_file.write(text_row + '\n')

                

