"""
Linux ssl certificate creation
"""
# =========================================================================
#
#         FILE:  linux_ssl_cert_creation.py
#  DESCRIPTION:  Keywords to start,stop and check status of linux service
#       AUTHOR:  Thyagarajan S Pasupathy (thyag@juniper.net)
#      COMPANY:  Juniper Networks
#      VERSION:  1.0
# =========================================================================

def generate_self_signed_cert(device=None, **kwargs):
    """
    Generate certificate and key
    Example :-
        generate_self_signed_certificate(device=unix1)
        generate_self_signed_certificate(device=unix1,
        serial_number="45396877595662337796295750953143259065"
         , key_filename="20byteserver_key_path.key", cert_filename="20byteserver_key_path.crt")
    Robot example :-
        generate self signed certificate    device=unix1

    :param Device device:
        **REQUIRED** Device handle
    :param str openssl_path:
        *OPTIONAL* openssl binary path
            ``Default value``   : openssl
    :param str rsa_keysize:
        *OPTIONAL* rsa key size
            ``Default value``   : 1024
    :param str key_filename:
        *OPTIONAL* generated key filename with path
            ``Default value``   : /tmp/server.key
    :param str cert_filename:
        *OPTIONAL* generated certificate filename with path
            ``Default value``   : /tmp/server.crt
    :param str validity_days:
        *OPTIONAL* Validity of the certificate in days
            ``Default value``   : 30
    :param str subj_org:
        *OPTIONAL* Certificate subject organization
            ``Default value``   : juniper-test
    :param str subj_org_unit:
        *OPTIONAL* Certificate subject organization unit
            ``Default value``   : jnpr-ngfw
    :param str subj_country:
        *OPTIONAL* Certificate subject country (2 nos characters only)
            ``Default value``   : IN
    :param str subj_state:
        *OPTIONAL* Certificate subject state name
            ``Default value``   : Karnataka
    :param str subj_locality:
        *OPTIONAL* Certificate locality
            ``Default value``   : Bangalore
    :param str subj_common_name:
        *OPTIONAL* Certificate common name
            ``Default value``   : www.jnpr-test.net
    :param str serial_number
        *OPTIONAL* Serial number of the certificate
    :return: Returns "True"
    :rtype: bool
    """
    openssl_path = kwargs.get('openssl_path', "openssl").lower()
    rsa_keysize = kwargs.get('rsa_keysize', "1024")
    key_filename = kwargs.get('key_filename', "/tmp/server.key")
    cert_filename = kwargs.get('cert_filename', "/tmp/server.crt")
    validity_days = kwargs.get('validity_days', "30")
    subj_org = kwargs.get('subj_org', "juniper-test")
    subj_org_unit = kwargs.get('subj_org_unit', "jnpr-ngfw")
    subj_country = kwargs.get('subj_country', "IN")
    subj_state = kwargs.get('subj_state', "Karnataka")
    subj_locality = kwargs.get('subj_locality', "Bangalore")
    subj_common_name = kwargs.get('subj_common_name', "www.jnpr-test.net")
    serial_number = kwargs.get('serial_number', None)

    if device is None:
        raise ValueError("device is mandatory argument")

    serial_number_append = ""
    if serial_number is not None:
        serial_number_append = " -set_serial " + serial_number

    cmd = openssl_path + " genrsa -out " + key_filename + " " + rsa_keysize
    device.shell(command=cmd)
    cmd = openssl_path + " req -new -x509 -days " + validity_days + " -key " + key_filename + \
          " -out " + cert_filename + " -subj " + '"/C=' + subj_country + "/ST=" + subj_state + \
          "/L=" + subj_locality + "/O=" + subj_org + "/OU=" + subj_org_unit + "/CN=" + \
          subj_common_name + '"' + serial_number_append
    device.shell(command=cmd)

    return True
