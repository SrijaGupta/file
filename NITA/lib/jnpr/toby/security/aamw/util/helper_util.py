import logging
import random
import re
import time
import urllib.request
import xml.etree.ElementTree as Et


def log_break(log_message, max_len=50):
    """Print a break with message on logs"""
    if len(log_message) >= max_len:
        head_len, foot_len = 5, 5
    else:
        head_len = int((max_len - len(log_message))//2)
        foot_len = max_len - len(log_message) - head_len

    logging.info('-'*head_len + log_message + '-'*foot_len)


def sleep(sleep_time: float = 0.0, message=None):
    """Print a message then sleep """
    if message:
        logging.info('Sleep %ss: %s', str(sleep_time), message)
    else:
        logging.info('Sleep %ss', str(sleep_time))
    time.sleep(float(sleep_time))
    return None


def get_vty_cmd_prefix(srx_handle):
    """Get vty command prefix for device"""
    model = srx_handle.current_node.current_controller.get_model().lower()
    srx_handle.log('Getting VTY prefix for model: %s' % model)
    if re.search('^vsrx2?|srx(1500|4[126]00)$', model):
        res = 'cprod -A fpc0 -c'
    elif re.search('^srx(550m|3(20|25|45))$', model):
        res = 'cprod -A 0x1 -c'
    elif re.search('^srx(5[468]00)$', model):
        res = 'srx-cprod.sh -s spu -c'
    else:
        message = 'Unrecognizable model: %s. Processing as SRX1500 for now' \
                  % model
        srx_handle.log(level='WARN', message=message)
        res = 'cprod -A fpc0 -c'
    srx_handle.log('VTY prefix: %s' % res)
    return res


def version_checker(srx_handle, compared_version):
    """
    Check the junos version for certain feature
    :param srx_handle: srx dut
    :param compared_version: the junos version you want to compare with
    """
    # print out certain junos version you want to check for certain feature
    logging.info('Certain junos version you want to check: %s', str(compared_version))
    # get the running junos version of SRX
    current_junos_version = srx_handle.current_node.current_controller.get_version()[:4]
    logging.info('SRX running junos version: %s', str(current_junos_version))
    return(bool(current_junos_version >= compared_version))


def generate_new_eicar_file(device_handle,
                            dest_file_path='/var/www/html/new_eicar.exe'):
    """Generate a new eicar file at file path"""
    random_component = '%s_%s' % (int(time.time()), random.randint(0, 1 << 20))
    eicar = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-' \
            r'TEST-FILE' + random_component + r'!$H+H*HHHHSHSHSHSJSHS*****'

    device_handle.su()
    device_handle.shell(command='rm -f %s' % dest_file_path)
    device_handle.shell(command='echo \'%s\' > %s' % (eicar, dest_file_path))


def get_device_serial(srx_handle):
    """Get SRX serial number"""
    response = srx_handle.cli(command='show chassis hardware').response()

    if not response or "Chassis" not in response:
        return None

    for line in response.split("\n"):
        if "Chassis" in line:
            return re.search("Chassis\s+([a-zA-Z0-9_]+)", line).group(1)

    return None


def get_appid_files_to_srx(srx_handle, server_handle, server_ip):
    """Get appid files to SRX"""
    # Proxy 36713
    srx_handle.log('Get all application id files to SRX')
    srx_folder = '/var/db/appid/sec-download/'
    need_files = ['application_groups2.xml.gz',
                  'applications.xsd',
                  'applications2.xml.gz',
                  'libqmprotocols.tgz']
    manifest = 'manifest.xml'

    manifest_url = _get_appid_manifest_url(srx_handle)

    # Download
    _download_appid_to_server(server_handle, manifest_url, need_files)
    url = 'http://' + server_ip + '/appid/'
    for f in need_files:
        srx_handle.shell(command='curl %s -o %s' % (url+f, srx_folder+f))

    srx_handle.shell(command='curl %s -o %s' % (url+manifest,
                                                srx_folder+manifest))
    srx_handle.log('Finish download all appid files to SRX')

    # gunzip downloaded files
    srx_handle.shell(command='gzip -d -f /var/db/appid/sec-download/*.gz')
    srx_handle.shell(command='ls /var/db/appid/sec-download/')
    srx_handle.log('Finish unzip all appid files in SRX')


def _get_appid_manifest_url(srx_handle):
    """Get appid manifest url"""
    # Proxy 36713
    model = srx_handle.current_node.current_controller.get_model().lower()
    srx_handle.log('Getting appid manifest url for model: %s' % model)
    if re.search('^vsrx2?|srx(1500|4[126]00)$', model):
        url = 'https://signatures.juniper.net/cgi-bin/index.cgi?type=ma' \
              'nifest&device=srxtvp&feature=ai&detector=0.0.0&to=lates' \
              't&os=18.2&build=44'
    elif re.search('^srx(550m|3(20|25|45))$', model):
        url = 'https://signatures.juniper.net/cgi-bin/index.cgi?type=m' \
              'anifest&device=srxtvp&feature=ai&detector=0.0.0&to=late' \
              'st&os=18.2&build=44'
    elif re.search('^srx(5[468]00)$', model):
        url = 'https://signatures.juniper.net/cgi-bin/index.cgi?type=m' \
              'anifest&device=srx5400&feature=ai&detector=0.0.0&to=lat' \
              'est&os=18.2&build=44'
    else:
        message = 'Unrecognizable model: %s. Processing as SRX1500 for now'\
                  % model
        srx_handle.log(level='WARN', message=message)
        url = 'https://signatures.juniper.net/cgi-bin/index.cgi?type=m' \
              'anifest&device=srxtvp&feature=ai&detector=0.0.0&to=late' \
              'st&os=18.2&build=44'
    srx_handle.log('Manifest url: %s' % url)
    return url


def _download_appid_to_server(device_handle, manifest_url, need_files,
                              dest_folder='/var/www/html/appid/'):
    """Download all the 5 files needed for appId installation, to one server
    which has public internet access"""

    # Proxy 36713
    device_handle.su()
    device_handle.shell(command='mkdir -p %s' % dest_folder)

    # Download manifest file
    device_handle.shell(command="curl -L '%s' -o %s" % (manifest_url,
                                                        dest_folder+'manifest.'
                                                                    'xml'))
    # Download all other needed files
    urls = _get_urls_from_manifest(manifest_url, need_files)
    for k, v in urls.items():
        device_handle.shell(command='curl %s -o %s' % (v, dest_folder+k),
                            timeout=300)


def _get_urls_from_manifest(url, att_names):
    """Get url from manifest"""
    # Proxy 36713: Download manifest on local host
    file_name = 'tmp_manifest.xml'
    urllib.request.urlretrieve(url, file_name)

    # Read manifest xml, get URL for all specified att_name
    urls = {}
    root = Et.parse(file_name).getroot()

    for e in root.findall('entry'):
        if e.find('id').text in att_names:
            urls[e.find('id').text] = e.find('url').text

    return urls
