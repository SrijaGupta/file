''' This code scps the config file to the router '''
import os

def scp_file_to_vsrx(ip_addr, filename, ssh_key):

    ''' sends the file to the vsrx router and returns true or false '''

    command = 'scp -i ' + ssh_key + \
              ' -o StrictHostKeyChecking=no ' + filename + ' root@' + ip_addr + ':.'
    try:
        os.system(command)
    except OSError as error:
        print(error)
        return False
    return True
