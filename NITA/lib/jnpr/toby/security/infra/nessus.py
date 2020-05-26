"""Require Python3"""
from __future__ import print_function
import json
import subprocess as sb
import time


def get_token():
    """Returns tokens"""
    var1 = 'curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d' \
           + ' ' + '\'{"username":"kkart@juniper.net", "password":"Juniper@123"}\'' + \
           ' ' + '"https://cloud.tenable.com/session"'
    token_obtained = sb.Popen(var1, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, shell=True)
    token, err = token_obtained.communicate()
    content = token.decode("utf-8")
    data_dict = json.loads(content)
    token = data_dict["token"]
    return token


def get_id(token, ip_address):
    """returns token id"""
    device = ip_address
    scan_id = "127473"
    uuid_key = "ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66"
    scan = 'curl \'https://cloud.tenable.com/scans\' -k \
     -X POST -H \'Content-Type: application/json\' -H \'X-Cookie: token=' + \
           str(token) + '\' -d \'{"uuid":"' + \
           str(uuid_key) + \
           '","settings":{"name":"Test","description":"Basic Scan using API","text_targets":"' + \
           str(device) + '", "launch":"ONETIME", "enabled":true,"scanner_id" :' \
           + str(scan_id) + ', "launch_now":true}\'  | python -m json.tool'
    token_obtained1 = sb.Popen(scan, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, shell=True)
    id_scan, err = token_obtained1.communicate()
    id_scan = id_scan.decode("utf-8")
    data_dict = json.loads(id_scan)
    token_id = data_dict["scan"]["id"]
    return token_id


def get_data(token, token_id):
    """Fetches the data from the cloud tenable server"""
    var2 = "curl -k -H 'X-Cookie: token=" + str(token) + "' https://cloud.tenable.com/scans/" + str(
        token_id) + " |   python -m json.tool"
    token_obtained2 = sb.Popen(var2, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, shell=True)
    print("running..")
    time.sleep(600)
    token_obtained2 = sb.Popen(var2, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, shell=True)
    full_scan, err = token_obtained2.communicate()
    content = full_scan.decode("utf-8")
    full_scan = json.loads(content)
    status = check_status(full_scan)
    print(status)
    counter = 0
    while status == "not completed":
        print("waiting for another mins..")
        time.sleep(600)
        token_obtained2 = sb.Popen(var2, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, shell=True)
        full_scan, err = token_obtained2.communicate()
        content = full_scan.decode("utf-8")
        full_scan = json.loads(content)
        counter = counter+1
        if counter == 5:
            break
    return full_scan


def check_status(full_scan):
    """Check if the status is set to completed"""
    if full_scan["info"]["status"] == "completed":
        # data = full_scan["hosts"][0]["severitycount"]["item"]
        # print(data)
        return "completed"
    else:
        return "not completed"


def display(vurl_dict):
    """Display the data"""
    for key_val, value_val in vurl_dict.items():
        data_k1 = str(key_val)
        print("Severity Level " + data_k1 + ":")
        print("----------------")
        for key_val1, value_val1 in value_val.items():
            data_k2 = str(value_val1[1])
            print(key_val1 + "      " + value_val1[0] + "       " + data_k2)
        print()
        print()
        print()


def get_result(vurl_dict):
    """Check if the result is pass or fail"""
    sev = sorted(vurl_dict.keys(), reverse=True)
    if int(sev[0]) > 3:
        print()
        print()
        print("*********************")
        print("The script has failed")
        print("*********************")
        print()
        print()
        for key_val, value_val in vurl_dict.items():
            if key_val > 3:
                data_k1 = str(key_val)
                print("Severity Level " + data_k1 + ":")
                print("----------------")
                for key_val1, value_val1 in value_val.items():
                    data_k2 = str(value_val1[1])
                    print(key_val1 + "      " + value_val1[0] + "       " + data_k2)
        return "FAIL"
    else:
        return "PASS"


def nessus_vulner(ip_address):
    """Main module"""
    token = get_token()
    print(token)
    token_id = get_id(token, ip_address)
    print(token_id)
    full_scan = get_data(token, token_id)
    try:
        if full_scan["error"] in "Unauthorized":
            token = get_token()
            full_scan = get_data(token, token_id)
    except:
        print("No error in Unauthorized")
    status = check_status(full_scan)
    if status == "completed":
        pass
    else:
        print("Error: Timeout")
        return "FAIL"
    vurl = full_scan["vulnerabilities"]
    vurl_dict = {}
    for i in range(len(vurl)):
        if vurl[i]["severity"] not in vurl_dict.keys():
            vurl_dict[vurl[i]["severity"]] = {}
        if vurl[i]["plugin_name"] not in vurl_dict[vurl[i]["severity"]]:
            vurl_dict[vurl[i]["severity"]][vurl[i]["plugin_name"]] = list()
            vurl_dict[vurl[i]["severity"]][vurl[i]["plugin_name"]].append(vurl[i]["plugin_family"])
            vurl_dict[vurl[i]["severity"]][vurl[i]["plugin_name"]].append(vurl[i]["count"])
    display(vurl_dict)
    result = get_result(vurl_dict)
    return result
