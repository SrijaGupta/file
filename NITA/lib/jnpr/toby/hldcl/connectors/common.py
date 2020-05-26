import logging
import time
import socket


def check_socket(host, **kwargs):
    """
    Static method that returns socket status of a device

    :param host:
        **REQUIRED** hostname or IP address of device
    :param socket_type:
        *OPTIONAL* Type of socket to check on the host
    :param port:
        *OPTIONAL* Port number of socket to check on the host
    :param timeout:
        *OPTIONAL* Time to connect to socket. Default is 1200
    :param interval:
        *OPTIONAL* Interval at which socket needs to be checked. Default is 30
    :param negative:
        *OPTIONAL* Check to find if socket is available/unavailable. Default is 0
    :return: True if Pass or exception if Fail
    """
    socket.setdefaulttimeout(1)
    negative = kwargs.get('negative', 0)
    timeout = kwargs.get('timeout', 1200)
    interval = kwargs.get('interval', 30)
    socket_type = kwargs.get('socket_type', 'other')
    port = 0
    if socket_type == 'telnet':
        port = 23
    elif socket_type == 'ssh':
        port = 22
    else:
        if 'port' in kwargs:
            port = kwargs['port']
        else:
            logging.error('Unknown socket type %s: FAIL' % socket_type)
            return False
    count = 0
    result = True
    while True:
        try:
            sock = socket.socket()
            sock.connect((host, port))
            logging.info('Successfully opened %s socket to %s' % (socket_type,
                                                                  host))
            if negative:
                logging.info('But this is a negative socket test.')
                if count < timeout/interval:
                    logging.info('Trying again in %s seconds...' % interval)
                    sock.close()
                    time.sleep(interval)
                    count += 1
                else:
                    logging.error('Negative %s socket test FAIL' % socket_type)
                    sock.close()
                    result = False
                    break
            else:
                logging.info('Socket test PASS')
                sock.close()
                result = True
                break
        except Exception as error:
            if negative:
                logging.info('%s socket to %s is currently unavailable: ' %
                             (socket_type, host))
                logging.info('Negative socket test PASS')
                sock.close()
                result = True
                break
            else:
                logging.info('%s socket to %s is currently unavailable: ' %
                             (socket_type, host))
                if count < timeout/interval:
                    logging.info('Trying again in %s seconds...' % interval)
                    time.sleep(interval)
                    count += 1
                else:
                    logging.error('Socket test FAIL')
                    sock.close()
                    result = False
                    break
    return result
