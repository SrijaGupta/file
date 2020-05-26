"""
    This module holds the credentials that need to be used to
    log into various devices.
    These credentials must be set blank when publishing.
"""
# pylint: disable=C0103
Junos = {
    'USERNAME': 'regress',
    'PASSWORD': 'MaRtInI',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
    'SU': 'root',
    'SUPASSWORD': 'Embe1mpls',
}
Unix = {
    'USERNAME': 'regress',
    'PASSWORD': 'MaRtInI',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
    'SU': 'root',
    'SUPASSWORD': 'Embe1mpls',
}
Agilent = {
    'USERNAME': None,
    'PASSWORD': None,
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
Spirent = {
    'USERNAME': 'admin',
    'PASSWORD': 'spt_admin',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
Ixia = {
    'USERNAME': 'admin',
    'PASSWORD': 'admin',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
IxiaAppserver = {
    'USERNAME': 'admin',
    'PASSWORD': 'admin',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
IxVeriwave = {
    'USERNAME': 'root',
    'PASSWORD': None,
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
Breakingpoint = {
    'USERNAME': 'regress',
    'PASSWORD': 'MaRtInI',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
Paragon = {
    'USERNAME': 'regress',
    'PASSWORD': 'MaRtInI',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
Elevate = {
    'USERNAME': ' ',
    'PASSWORD': ' ',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}
Cisco = {
    'USERNAME': 'root',
    'PASSWORD': 'Embe1mpls',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
    'SU': 'root',
    'ENABLEPASSWORD': 'Embe1mpls',
}
Windows = {
    'USERNAME': 'administrator',
    'PASSWORD': 'Embe1mpls',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
    'SU': None,
    'SUPASSWORD': None,
}
Landslide = {
    'USERNAME': 'sms',
    'PASSWORD': 'a1b2c3d4',
    'TELNETUSERNAME': 'cfguser',
    'TELNETPASSWORD': 'cfguser',
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
}

class ReadOnlyDict(dict):
    """
        A readonly class that creates dictionaries
        through which we can access the necessary
        credentials.
    """
    def __readonly__(self, *args, **kwargs):
        raise RuntimeError("Cannot modify ReadOnlyDict")
    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__
    del __readonly__

JUNOS = ReadOnlyDict(Junos)
UNIX = ReadOnlyDict(Unix)
AGILENT = ReadOnlyDict(Agilent)
SPIRENT = ReadOnlyDict(Spirent)
BREAKINGPOINT = ReadOnlyDict(Breakingpoint)
PARAGON = ReadOnlyDict(Paragon)
ELEVATE = ReadOnlyDict(Elevate)
LANDSLIDE = ReadOnlyDict(Landslide)
IXIA = ReadOnlyDict(Ixia)
IXIAAPPSERVER = ReadOnlyDict(IxiaAppserver)
IXVERIWAVE = ReadOnlyDict(IxVeriwave)
IOS = ReadOnlyDict(Cisco)
WINDOWS = ReadOnlyDict(Windows)

def get_credentials(**kwargs):
    """
    Gets OS credentials
    """
    if not kwargs.get('user') or not kwargs.get('password'):
        if kwargs.get('os').upper() == 'JUNOS':
            dev_cred = JUNOS
        elif kwargs.get('os').upper() == 'UNIX' or kwargs.get('os').upper() == 'LINUX' or \
                kwargs.get('os').upper() == 'FREEBSD' or kwargs.get('os').upper() == 'CENTOS' or \
                kwargs.get('os').upper() == 'UBUNTU':
            dev_cred = UNIX
        elif kwargs.get('os').upper() == 'IOS':
            dev_cred = IOS
        elif kwargs.get('os').upper() == 'BREAKINGPOINT' or kwargs.get('os').upper() == 'BPS':
            dev_cred = BREAKINGPOINT
        elif kwargs.get('os').upper() == 'PARAGON':
            dev_cred = PARAGON
        elif kwargs.get('os').upper() == 'ELEVATE':
            dev_cred = ELEVATE
        elif kwargs.get('os').upper() == 'LANDSLIDE':
            dev_cred = LANDSLIDE
            return dev_cred
        elif kwargs.get('os').upper() == 'SPIRENT':
            dev_cred = SPIRENT
        elif kwargs.get('os').upper() == 'IXIA':
            dev_cred = IXIA
        elif kwargs.get('os').upper() == 'IXIAAPPSERVER':
            dev_cred = IXIAAPPSERVER
        elif kwargs.get('os').upper() == 'IXVERIWAVE':
            dev_cred = IXVERIWAVE
        elif kwargs.get('os').upper() == 'WINDOWS':
            dev_cred = WINDOWS
        else:
            raise Exception('Unknown Device OS')

        print("print username and password", dev_cred['USERNAME'], dev_cred['PASSWORD'])
        # Check if default credentials are available
        if not dev_cred['USERNAME'] and not dev_cred['PASSWORD']:
            raise Exception("Username/Password cannot be determined")
        return dev_cred['USERNAME'], dev_cred['PASSWORD']
    return kwargs['user'], kwargs['password']
