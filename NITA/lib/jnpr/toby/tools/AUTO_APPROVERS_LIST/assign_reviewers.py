#!/usr/local/bin/python3 

########################
#
# Original Author: Justin Hayes
#
########################


import requests # pylint: disable=import-error
import pprint
import json              # pylint: disable=unused-import
import sys
import yaml  # pylint: disable=import-error
import re # pylint: disable=unused-import
from ldap3 import Server, Connection, ALL, SUBTREE  # pylint: disable=import-error, unused-import


def main(argv):     # pylint: disable=too-many-locals, too-many-statements
    if len(argv) != 2:
        print("Error: Incorrect  usage ")   # pylint: disable=superfluous-parens,C0325
        print("Usage:\n\t assign_reviewers.py <merge_request_id> <yaml_file_location>")  # pylint: disable=superfluous-parens,C0325
        sys.exit(1)
    server = Server('LDAP-EQX-LB.jnpr.net')
    conn = Connection(server, user='jnpr\_tide_auth', password='E%S5(Mvvh1QWjed13iNj7cP3$Di)jV', auto_bind=True)  # pylint: disable= anomalous-backslash-in-string
    headers = {'PRIVATE-TOKEN':'FHxNyCyf8GWZKhwi9Jxq', 'Content-type' : 'application/json'}
    private_token = 'FHxNyCyf8GWZKhwi9Jxq'    # pylint: disable=unused-variable

    url = 'https://ssd-git.juniper.net/api/v4//projects/3006/merge_requests/'
    mr_url = url + str(argv[0])
    reviewers = yaml.load(open(argv[1]))
    response = requests.get(mr_url, headers=headers, verify=False)
    result = list()   # pylint: disable= unused-variable

    #get all open merge requests and iterate through them
    merge_request = response.json()
    mr_result = dict()
    mr_result['title'] = merge_request['title']
    mr_result['author_name'] = merge_request['author']['name']
    mr_result['author_userid'] = merge_request['author']['username']
    #gather current git approvers
    approval_url = url + str(merge_request['iid']) + '/approvals'
    approval_response = requests.get(approval_url, headers=headers, verify=False).json()
    approvers = approval_response['suggested_approvers'] # pylint: disable=unused-variable
        # comment out gathering of existing approvers for now
        # mr_result['current_reviewers'] = list()
        # for approver in approvers:
        #     mr_result['current_reviewers'].append(approver['username'])
        #gather changes
    change_url = url + str(merge_request['iid']) + '/changes'
    change_response = requests.get(change_url, headers=headers, verify=False).json()
    changes = change_response['changes']
    mr_result['changed_files'] = list()
    mr_result['required_reviewers'] = list()
    no_of_approvers = 2
    for change in changes:  # pylint: disable=  too-many-nested-blocks
        if change['new_path'].startswith('tesir'):
            #skip
            continue
        changed_file = change['new_path']
        mr_result['changed_files'].append(changed_file)
        folders = changed_file.split('/')
        found_reviewers = False
        while len(folders):             # pylint: disable= len-as-condition
            possible_folder = '/'.join(folders)
            possible_folder = possible_folder + "/"
            if possible_folder in reviewers.keys():
                for reviewer in reviewers[possible_folder]['reviewers']:
                    ldap_members = get_jam_members(str(reviewer), conn)
                    if ldap_members: #reviewer was a JAM alias
                        mr_result['required_reviewers'] = mr_result['required_reviewers'] + ldap_members
                    else:
                        mr_result['required_reviewers'].append(reviewer)
                found_reviewers = True
                no_of_approvers = reviewers[possible_folder]['num_reviewers']
                break
            else:
                tmp_folder = '/'.join(folders[0:1])
                if tmp_folder in reviewers.keys():
                    for reviewer in reviewers[tmp_folder]:
                        ldap_members = get_jam_members(str(reviewer), conn)
                        if ldap_members:  # reviewer was a JAM alias
                            mr_result['required_reviewers'] = mr_result['required_reviewers'] + ldap_members
                        else:
                            mr_result['required_reviewers'].append(reviewer)

            del folders[-1]
        if not found_reviewers:
            #mr_result['required_reviewers'] = mr_result['required_reviewers'] + reviewers['default']['reviewers']
            #no_of_approvers  = reviewers['default']['min_reviewer']
            print('\nNo reviewer found adding default TOBY as reviewer') # pylint: disable=superfluous-parens,C0325
        #mr_result['required_reviewers'].append('TOBY')

    approvers_id = list()
    for user in list(set(mr_result['required_reviewers'])):
        user_url = 'https://ssd-git.juniper.net/api/v4/users?username=' + user
        response = requests.get(user_url, headers=headers, verify=False).json()
        for element in response:
            approvers_id.append(element['id'])

    #remove redundancies
    mr_result['required_reviewers'] = list(set(mr_result['required_reviewers']))
    #no_of_approvers = len(mr_result['required_reviewers'])
    print('\nno_of_approvers', no_of_approvers)
    print('\nrequired_reviewers', mr_result['required_reviewers'])
    print('\napprovers_id', approvers_id)
    mr_result['required_reviewers'] = approvers_id

    if len(mr_result['changed_files']): # pylint: disable= len-as-condition
        #pp = pprint.PrettyPrinter(indent=4)    # pylint: disable=invalid-name
        #pp.pprint(mr_result)
        #print("\n")    # pylint: disable=superfluous-parens,C0325
        update_approvers_url = url  + str(merge_request['iid']) + '/approvers'
        data = '{"id": 3006, "approver_ids": ' + str(mr_result['required_reviewers']) + \
                   ', "merge_request_iid": ' + argv[0] + ', "approver_group_ids": []}'
        update_response = requests.put(update_approvers_url, headers=headers, data=str(data), verify=False)
        #print(update_response)   # pylint: disable=superfluous-parens,C0325
        #print(update_response.content)   # pylint: disable=superfluous-parens,C0325
        no_of_approvers += 1   # since _cd-builder approvals is removed we need not do +1
        data1 = '{"id": 3006, "approvals_required": ' + str(no_of_approvers) + '}'
        update_approvers_url = url + str(merge_request['iid']) + '/approvals'
        update_response = requests.post(update_approvers_url, headers=headers, data=str(data1), verify=False)
        #print(update_response.text + "\n\n")   # pylint: disable=superfluous-parens,C0325

    #print("\n")  # pylint: disable=superfluous-parens,C0325
    conn.unbind()

def get_jam_members(alias, conn):

    raw_members = []
    members = []
    search_filter = '(&(objectCategory=group)(cn=' + alias + '))'
    conn.search(search_base='dc=jnpr,dc=net',
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['member'],
                size_limit=0)
    for entry in conn.response:
        #print(entry)
        if 'attributes' in entry:
            raw_members = entry['attributes']['member']
    if len(raw_members): # pylint: disable= len-as-condition
        for member in raw_members:
            conn.search(search_base='dc=jnpr,dc=net',  \
                        search_filter='(distinguishedName=' + member + ')', \
                        search_scope=SUBTREE, \
                        attributes=['sAMAccountName'], \
                        paged_size=5, \
                        size_limit=1)
            for entry in conn.response:
                if 'attributes' in entry:
                   members.append(entry['attributes']['sAMAccountName'])  # pylint: disable=bad-indentation
    if len(members):  # pylint: disable= len-as-condition,no-else-return
        return members
    else:
        return False


if __name__ == "__main__":
   main(sys.argv[1:])  # pylint: disable=bad-indentation
