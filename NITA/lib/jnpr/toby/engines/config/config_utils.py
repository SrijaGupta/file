"""
Copyright (C) 2003-2015, Juniper Networks, Inc.
All rights reserved.
Authors:
    jpzhao
Description:
    config engine utility tools, may move to Toby utils later

"""
# pylint: disable=locally-disabled,undefined-variable,too-many-branches,too-many-nested-blocks
import os
import re
import itertools
import ipaddress
import netaddr
from collections import OrderedDict, Mapping
#import ruamel.yaml as yaml
import yaml
from jnpr.toby.utils.Vars import Vars

MYHEX = r'[A-Fa-f\d]'
# iso mininum (in bytes) is 2 4 4 4 4 2
REGEX_ISOADDR = r'{0}{{2}}(?:\.{0}{{4}}){{4}}(?:\.{0}{{2,4}}){{1,6}}'.format(MYHEX)
# mac address
REGEX_MAC = r'({0}{0}[:-]){{5}}{0}{0}'.format(MYHEX)
#ESI
REGEX_ESI = r'00:({0}{0}:){{8}}{0}{0}'.format(MYHEX)



def find_file(file):
    '''
    add suite location to the path
    '''

    if os.path.isfile(file):
        t.log('debug', '\n********* find file:' + str(file))
        return file
    elif Vars().get_global_variable('${SUITE_SOURCE}'):
        src_path = os.path.dirname(Vars().get_global_variable('${SUITE_SOURCE}'))
        suite_file = os.path.join(src_path, file)
        if os.path.isfile(suite_file):
            t.log('debug', '\n************ find suite file:' + suite_file)
            return suite_file

    raise Exception('cannot find file ' + file)

def read_yaml(string=None, file=None, ordered=True):
    '''
    used internally in config engine
    read yaml file and turn it into a python data structure
    override PyYAML's constructor to keep YAML mapping in OrderedDict
    This keeps the config data in order as it is in YAML text.

    :param string: yaml config string
    :param file: yaml config file
    '''
    def ordered_load(string, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
        '''
        load yaml to ordered dict
        '''
        class OrderedLoader(Loader):
            '''
            pass
            '''
            pass
        def construct_mapping(loader, node):
            '''
            construct_mapping
            '''
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(string, OrderedLoader)

    if file:
        file = find_file(file)
        if ordered is True:
            data = ordered_load(open(file))
        else:
            data = yaml.load(open(file))
            #data = yaml.safe_load(open(file))
    elif string:
        if ordered is True:
            data = ordered_load(string)
        else:
            data = yaml.load(string)
            #data = yaml.safe_load(string)
    else:
        raise Exception("mandatory arg 'file' or 'string' is missing")
    return data

def write_to_yaml(data, file=None):
    '''
        write OrderedDict back to yaml file, keep original order
        and keep space between each template ( use ruamel would be better )
    '''
    # set YAML to handle OderedDict
    def represent_order(dump, data):
        return dump.represent_mapping(u'tag:yaml.org,2002:map', data.items(), flow_style=False)
    yaml.add_representer(OrderedDict, represent_order)

    if file:
        with open(file, 'w') as f:
            #f.write('# cv variables saved for reference or reconnect:\n')
            f.write(yaml.dump(data, default_flow_style=False, indent=4))
    else:
        print(yaml.dump(data, default_flow_style=False, indent=4))
        return yaml.dump(data, default_flow_style=False, indent=4)

def _make_number_list(first=0, count=None, step=1, last=None, repeat=1, cycle=None, numbase=10):
    '''
    internal function
    return an iterator that will make a list of numbers(integers or float)
    '''

    # check step:
    if re.match(r'\d+$', str(step)):
        step = int(step)
    else:
        if is_ip(step):
            step = int(ipaddress.ip_address(step))
        elif re.match(r'/\d+', str(step)):
            steplen = re.sub(r'/', '', str(step))
            steplen = int(steplen)
            step = 2**(32 - steplen)
    xlist = itertools.count(first, step)
    # repeat first, and then cycle

    if cycle is not None:
        xlist = itertools.cycle(itertools.islice(xlist, cycle))
    if repeat > 1:
        xlist = itertools.chain.from_iterable(itertools.repeat(e, repeat) for e in xlist)
    if count:
        xlist = itertools.islice(xlist, count)
    elif last is not None:
        if not isinstance(last, int):
            raise Exception('last value "{}" is not a number: {}'.format(str(last), type(last)))
        elif last < first:
            raise Exception('in <<{}..{}>> last value should be larger than first'.format(str(first), str(last)))

        xlist = itertools.takewhile(lambda y: y <= last, xlist)

    #return xlist
    for x in xlist:
        if numbase == 10:    # decimal
            yield x
        elif numbase == 16:  # hex
            hex_str = str(hex(x))[2:]
            yield hex_str


def _make_string_list(first=None, count=None, step=1, last=None, repeat=1, cycle=None):
    '''
    internal function
    return an iterator that will make a list of string
    '''
    if first == None:
        t.log('warn', "missing madatory 'first'")
        return False

    matched = re.match(r'(.*[^\d]+)(\d*)', str(first))
    if matched is None:
        raise Exception("_make_string_list: cannot parse the first element:" + str(first))

    base = matched.group(1)
    if matched.group(2):
        begin = int(matched.group(2))
    elif count == 1:
        begin = ''
    else:
        begin = 0
    last_digit= None
    if last is not None:
        matched = re.match(r'(.*[^\d]+)(\d*)', str(last))
        if matched is None:
            raise Exception("_make_string_list: the last element is not a string: " + str(last))
        mbase = matched.group(1)
        if mbase != base:
            t.log('warn', "_make_string_list: last and first use different string, use first string")
            t.log('warn', "first: {}, last: {}".format(first, last))
        last_digit = matched.group(2)
        if re.match(r'\d+$', last_digit):
            last_digit = int(last_digit)
        else:
            raise Exception("_make_string_list: the last element {} does not match the first {}".format(last, first)) 

    # now get the iterable from the digit extension at the end

    args = {
        'first': begin,
        'step': step,
        'last':  last_digit,
        'repeat': repeat,
        'cycle': cycle}

    if count:
        args['count'] = count
    if count == 1:
        ext = [begin]
    else:
        ext = _make_number_list(**args)
    #xlist = itertools.zip_longest([base], ext, fillvalue=base)
    #xlist = itertools.chain([a + str(b) for a, b in xlist])
    for num in ext:
        thisstr = base + str(num)
        yield thisstr

def _make_ip_list(first=None, count=None, step=None, last=None, repeat=1, cycle=None):
    '''
    internal function
    returns a generator of ip address list
    '''

    if not is_ip(first):
        t.log('error', ' this is not ip: ' + str(first))
        return

    ip = first.split('/')
    addr = ipaddress.ip_address(ip[0])
    netlen = None
    if len(ip) > 1:
        netlen = ip[1]
        if step is None:
            step = "/" + str(netlen)

    # step: 0.0.1.0
    if step is not None:
        if is_ip(step):
            step = int(ipaddress.ip_address(step))
        elif re.match(r'/\d+', str(step)):
            steplen = re.sub(r'/', '', str(step))
            steplen = int(steplen)
            if re.match(r'IPv4', is_ip(addr)):
                step = 2**(32 - steplen)
            elif re.match(r'IPv6', is_ip(addr)):
                step = 2**(128 - steplen)
        else:
            step = int(step)
    else:
        step = 1   # default

    if last is not None:
        lastaddr = ipaddress.ip_address(last.split('/')[0])
        if lastaddr < addr:
            raise Exception('in <<{}..{}>> last value should be larger than first'.format(str(addr), str(lastaddr)))

    # infinite, count determied by other expansion in the string
    iaddr = addr
    icycle = cycle
    irepeat = repeat
    while True:
        thisip = str(iaddr)
        # dealing with cycle/repeat:

        if netlen is not None:
            thisip += "/" + str(netlen)

        yield thisip

        # prepare the next value
        # when to break
        if count is not None:
            count -= 1
            if count <= 0:
                break
        if last is not None:
            if iaddr >= lastaddr:
                break

        # what's next:
        # repeat then cycle if any
        irepeat -= 1
        if irepeat == 0:
            iaddr = iaddr + step
            irepeat = repeat
            if cycle is not None:
                icycle -= 1
                if icycle <= 0:
                    iaddr = addr
                    icycle = cycle


def _make_mac_list(first=None, count=None, step=None, last=None, repeat=1, cycle=None):
    '''
    return a generator of mac addresses
    '''
    if not is_mac(first):
        t.log('error', ' this is not mac: ' + str(first))
        return

    firstaddr = netaddr.EUI(first)

    # step: 0:0:0:0:1:0
    if step is not None:
        if is_mac(step):
            step = int(netaddr.EUI(step))
        elif re.match(r'\d+$', str(step)):
            step = int(step)
        else:
            raise Exception('e', 'Step is not a mac or an integer: ' + step)
    else:
        step = 1   # default

    if last is not None:
        lastaddr = netaddr.EUI(last)
        if lastaddr < firstaddr:
            raise Exception('in <<{}..{}>> last value should be larger than first'.format(str(first), str(last)))

    # iterator, count determied by other expansion in the string
    iaddr = firstaddr
    icycle = cycle
    irepeat = repeat
    while True:
        # always return the unix format: '00:1b:77:49:54:ff'
        iaddr.dialect = netaddr.mac_unix_expanded
        thismac = str(iaddr)

        yield thismac

        # prepare the next value
        # when to break
        if count is not None:
            count -= 1
            if count <= 0:
                break
        if last is not None:
            if iaddr >= lastaddr:
                break

        # repeat then cycle if any
        irepeat -= 1
        if irepeat == 0:
            iaddr = netaddr.EUI(int(iaddr) + step)
            irepeat = repeat
            if cycle is not None:
                icycle -= 1
                if icycle <= 0:
                    iaddr = firstaddr
                    icycle = cycle

def _make_binary_list(first=0, count=None, step=1, last=None, numbase=2):
    '''
    return expanded binary iterator
    '''
    step = str(bin(step))
    if not is_binary(step):
        raise Exception('e', 'Step is not a binary number: ' + step)
    step = step[2:]
    if count:
        for _ in range(count):
            yield first
            first = add_binary_nums(first, step)
    elif last and is_binary(last):
        while int(first, 2) <= int(last, 2):
            yield first
            first = add_binary_nums(first, step)
    else:
        while True:
            yield first
            first = add_binary_nums(first, step)
            
def is_binary(binary_string):
    '''
    Returns True if the string is binary
    '''
    if re.match(r'\"?(0b)[0|1]+\"?$', binary_string):
        return True
    else:
        return False

def add_binary_nums(x, y):
    '''
    Add two binary numbers
    '''
    max_len = max(len(x), len(y))
    x = x.zfill(max_len)
    y = y.zfill(max_len)
    result = ''
    carry = 0
    for i in range(max_len-1, -1, -1):
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1
    if carry != 0:
        result = '1' + result
    return result.zfill(max_len)


def is_mac(mac_str):
    '''
    validate 48bit mac address  00:1b:77:ff:fe:49:54:ff'
    todo: 64bit mac?
    '''
    if netaddr.valid_mac(mac_str):
        return True
    else:
        return False


def is_ip(ip):
    '''
    internal function.
    check if the params is an IP address or not
    '''

    ip = str(ip)
    if re.match(r'(.+)(/\d*)$', ip):
        try:
            res = ipaddress.ip_interface(ip)
            return type(res).__name__

        except ValueError:
            return False
    else:
        try:
            res = ipaddress.ip_address(ip)
            return type(res).__name__
        except ValueError:
            return False


def is_esi(esi_str):
    '''
    validate esi identifier
    esi_str = '00:00:00:00:00:00:00:00:01:00'
    '''
    if re.match(r'{}$'.format(REGEX_ESI), str(esi_str)):
        return True
    else:
        return False

def _esi_to_int(esi_str):
    '''
    turn esi to an integer
    '''
    trim_esi = re.sub(r':', '', esi_str)
    return int(trim_esi.lstrip('0'), 16)

def _int_to_esi(esi_int):
    '''
    turn an integer to esi string format
    To be improved..
    '''
    def int_to_words(int_val, word_size=8, num_words=10):
        '''
        turn an integer to a list of hex number 'words'
        the idea is taken form netaddr/strategy/ for MAC address
        '''
        max_word = 2 ** word_size - 1

        words = []
        for _ in range(num_words):
            word = int_val & max_word
            words.append(int(word))
            int_val >>= word_size
        return tuple(reversed(words))

    words = int_to_words(esi_int)
    tokens = ['{:02x}'.format(i) for i in words]
    esi = ':'.join(tokens)
    return esi


def _make_esi_list(first=None, count=None, step=None, last=None, repeat=1, cycle=None):
    '''
    return a generator of mac addresses
    '''
    if not is_esi(first):
        raise Exception('This is not an esi identifier: ' + str(first))

    firstaddr = _esi_to_int(first)

    # step: 00:00:00:00:00:00:00:01:00
    if step is not None:
        if is_esi(step):
            step = _esi_to_int(step)
        elif re.match(r'\d+$', str(step)):
            step = int(step)
        else:
            raise Exception('e', 'Step is not a esi or an integer: ' + step)
    else:
        step = 1   # default

    if last is not None:
        lastaddr = _esi_to_int(last)
        if lastaddr < firstaddr:
            raise Exception('in <<{}..{}>> last value should be larger than first'.format(str(first), str(last)))

    # iterator, count determied by other expansion in the string
    iaddr = firstaddr
    icycle = cycle
    irepeat = repeat
    while True:
        thisesi = _int_to_esi(iaddr)

        yield thisesi

        # prepare the next value
        # when to break
        if count is not None:
            count -= 1
            if count <= 0:
                break
        if last is not None:
            if iaddr >= lastaddr:
                break

        # repeat then cycle if any
        irepeat -= 1
        if irepeat == 0:
            iaddr = iaddr + step
            irepeat = repeat
            if cycle is not None:
                icycle -= 1
                if icycle <= 0:
                    iaddr = firstaddr
                    icycle = cycle


def _make_mixed_list(first=None, count=None, step=1, last=None, repeat=1, cycle=None):
    '''
    internal function
    <<(x, y, z)#{cycle:3, step:1, count:9}>>
    - count/step optional
    <<(x, y,z)..#{cycle:3}>>
    '''
    if first is None:
        t.log('error', 'first is mandatory')
        return
    matched = re.match(r'\((.+)\)(\.\.)*', first)
    xlist = matched.group(1).split(',')
    # todo: can be (1..4, 6,a)..  need to exapnd 1..4
    mlist = iter(xlist)

    if cycle is None:
        cycle = len(xlist)
    mlist = itertools.cycle(itertools.islice(mlist, cycle))

    if repeat > 1:
        mlist = itertools.chain.from_iterable(itertools.repeat(e, repeat) for e in mlist)
    if count is not None:
        mlist = itertools.islice(mlist, count)
    elif last is not None:
        mlist = itertools.takewhile(lambda y: y <= last, mlist)
    return mlist


def make_list(**kwargs):
    '''
    make a list of anything based on the following args:
    #first=None, count=None,step=1, last=None, repeat=1, cycle=None
    '''
    if kwargs.get('string'):
        orig_key = kwargs.pop('string')

    first_str = str(kwargs['first'])
    if re.match(r'^\d+$', first_str):
        return _make_number_list(**kwargs)
    elif re.match(r'\"?0x[0-9a-fA-F]+\"?$', first_str):
        kwargs['numbase'] = 16
        kwargs['first'] = int(first_str, kwargs['numbase'])
        return _make_number_list(**kwargs)
    elif is_binary(first_str):
        kwargs['numbase'] = 2
        kwargs['first'] = first_str[2:]
        return _make_binary_list(**kwargs)
    elif is_ip(first_str):
        return _make_ip_list(**kwargs)
    elif is_mac(first_str):
        return _make_mac_list(**kwargs)
    elif is_esi(first_str):
        return _make_esi_list(**kwargs)
    elif re.match(r'\(.+\)(\.\.)*', first_str):
        return _make_mixed_list(**kwargs)
    elif re.match(r'(.*[^\d]+)(\d*)', first_str):
        return _make_string_list(**kwargs)
    else:
        t.log('error', "syntax error: " + first_str)
        return

def str_sort_key(string, _nsre=re.compile(r'(\d+)')):
    '''
    internal function
    use the key to sort list of strings naturally, not alphabetically
    such as [e1,E2,e10,e11]
    '''
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, string)]


def nested_set(base, keys, value, append=False):
    '''
    set a leaf node value with list of nested keys in a dict
    '''
    for key in keys[:-1]:
        base = base.setdefault(key, {})
    if keys[-1] not in base:
        base[keys[-1]] = value
    elif append:    # if is true, append value to existing key value
        if not isinstance(base[keys[-1]], list):
            base[keys[-1]] = [base[keys[-1]]]
        if isinstance(value, list):
            base[keys[-1]].extend(value)
        else:
            base[keys[-1]].append(value)
    else:   # by default, replace value if key already has value.
        base[keys[-1]] = value


def nested_update(base, update, append=False):
    """
    Update a nested dictionary with another nested dict.
    Modify ``base`` in place.
    """
    for key, value in update.items():
        if isinstance(base, Mapping):
            if isinstance(value, Mapping):
                returned = nested_update(base.get(key, {}), value, append=append)
                base[key] = returned
            elif not base.get(key):
                base[key] = update[key]
            elif append:
                # make a list if a leaf node already has a value
                if not isinstance(base[key], list):
                    base[key] = [base[key]]
                if isinstance(update[key], list):
                    base[key].extend(update[key])
                else:
                    base[key].append(update[key])
        else:
            base = {key: update[key]}

    return base

def nested_get(base, key, *key_list):
    """
    get a nested dictionary value through a list of keys
    """
    if key_list:
        return nested_get(base.get(key, {}), *key_list)
    return base.get(key)

def expand_to_list(base=None, sort=False):
    '''
    expand a string with the following syntax into a list of strings
    <<10..19>>
    <<10#{count:10, step:1, cycle:1, repeat:1},30, 40..44 >>
    <<1..>>
    <<http, ftp, scp>>
    '''
    base2 = base
    # search list tags in strings
    listp = re.compile(r'<<(.+?)>>[>]*')
    list_keys = listp.findall(base)

    if not list_keys:
        return [base]

    # remove duplicated tags:
    list_keys = list(OrderedDict.fromkeys(list_keys))
    key_disp = {}

    # at least one list needs to have a count, to avoid endless iteratoion
    has_count = None

    # process args in each list
    for orig_key in list_keys:
        xlist = []
        join2 = False
        tempkeys = []
        tmp_orig_key = orig_key
        if re.search(r'string\s*:\s*[\'\"],[\'\"]', orig_key):
            tmp_orig_key = re.sub(r'string\s*:\s*[\'"],[\'"]', 'string:"csv"', orig_key)
        # << a, b, (x,y,z,)..#{cycle:3, step:2}>>
        for ele in tmp_orig_key.split(','):
            # remove white spaces
            #ele = re.sub(r'\s+', '', ele)
            ele = ele.strip()

            # assemble (x,y,z,) back into one element
            if re.search(r'\(', ele):
                if re.search(r'\)', ele):
                    tempkeys.append(ele)
                else:
                    tmp = ele
                    join2 = True
            elif join2:
                tmp = ','.join([tmp, ele])
                if re.search(r'\)', ele):
                    tempkeys.append(tmp)
                    join2 = False
            else:
                tempkeys.append(ele)

        if join2:
            t.log('error', "missing closing ')'? \ncheck: " + orig_key)
            return
        subkeys = []
        join2 = False
        for ele in tempkeys:
            # assemble #{cycle:3, step:2} back into one element
            if re.search(r'#{', ele):
                if re.search(r'}', ele):
                    subkeys.append(ele)
                else:
                    tmp = ele
                    join2 = True
            elif join2:
                tmp = ','.join([tmp, ele])
                if re.search(r'}', ele):
                    subkeys.append(tmp)
                    join2 = False
            else:
                subkeys.append(ele)

        if join2:
            t.log('error', "missing closing '}'? \ncheck: " + orig_key)
            return

        # expand each list,(list pattern:iterables dict)
        counted = True
        exp_in_string = False
        for subkey in subkeys:
            opt = {}
            list_opt = re.match(r'(.+)#\{([^\}]+)\}', subkey)
            if list_opt is not None:
                subkey = list_opt.group(1).strip()
                largs = list_opt.group(2)
                #largs = re.sub(r'\s+', '', list_opt.group(2))

                for arg in largs.split(','):
                    k, val = arg.split(':', 1)
                    opt[k.strip()] = val.strip()

            min_max = re.match(r'(.+)\.\.(.+)', subkey)
            if min_max is not None:
                opt['first'] = min_max.group(1).strip()
                opt['last'] = min_max.group(2).strip()
            else:
                min_no_max = re.match(r'(.+)\.\.\s*$', subkey)
                if min_no_max is not None:
                    opt['first'] = min_no_max.group(1).strip()
                else:
                    oneitem = re.match(r'.+$', subkey)
                    if oneitem:
                        opt['first'] = subkey.strip()
                        if 'count' in opt:
                            pass
                        else:
                            opt['count'] = 1

            numbase = 10
            for key in opt:
                if isinstance(opt[key], str):
                    if re.match(r'^\d+$', opt[key]):
                        opt[key] = int(opt[key])
                    elif re.match(r'0x[a-zA-Z\d]+$', opt[key]):
                        # hex number
                        opt[key] = int(opt[key], 16)
                        numbase = 16
            if numbase == 16:
                opt['numbase'] = numbase
            if not any(key in opt for key in ('count', 'last')):
                counted = False

            # make the sub list iterator and chain to the main list iterator
            sublist = []
            try:
                sublist = make_list(**opt)
            except Exception as err:
                raise Exception('failed to expand the cfg with error <{}>:\n{}'.format(err, base))

            if opt.get('string') is not None:
            # expand into a string, not a list
            # <<1..5#{string:"csv"}>>:   "1,2,3,4,5"
            # <<1..5#{string:" "}>>:  "1 2 3 4 5"
                exp_in_string = True
                string_delem = opt['string'].strip('\"\'')
                if re.match('csv', string_delem, re.I):
                    string_delem = ','
                xlist = itertools.chain(xlist, [string_delem.join([str(ele) for ele in sublist])])
            else:
                #pass
                xlist = itertools.chain(xlist, sublist)

        # now if the subkeys has only one key, and it contains 'string'
        # this is the case it should just be expanded into a string,
        if exp_in_string and len(subkeys) == 1:
            exp_raw = re.escape("<<" + orig_key + ">>")
            exp_str = str(next(xlist))
            base2 = re.sub(exp_raw, exp_str, base2)
        # If one of the list expression in the string has 'count', it is good
        # we will not get into infinit iteration.
        else:
            #  list pattern:iterables dict
            key_disp["<<" + orig_key + ">>"] = xlist
        if counted:
            has_count = True

        #

    #all expansion keys are ready:
    if not has_count:
        msg = 'Infinit iterator in:\n' + base
        msg += ' \nneed to have at least one count or last'
        raise Exception(msg)

    if len(key_disp) == 0:
        return "{}".format(base2)
    # replace/expand string
    cfg_exp = []
    while True:
        ncfg = base2
        try:
            for key, exp_iter in key_disp.items():
                exp_raw = re.escape(key)
                ncfg = re.sub(exp_raw, str(next(exp_iter)), ncfg)
        except StopIteration:
            break

        if (len(cfg_exp) > 0  and cfg_exp[-1] != ncfg) or len(cfg_exp) == 0:
            cfg_exp.append(ncfg)

    if sort:
        cfg_exp.sort(key=str_sort_key)
    return cfg_exp

def send_email(sendfrom, sendto, subject, message, **kwargs):
    '''
    #todo: find the location of sendmail first
    '''
    sendmail_location = "/usr/sbin/sendmail"
    try:
        p = os.popen("{} -t".format(sendmail_location), "w")
    except:
        print('WARN:  cannot run sendmail')
        return

    email = "From:{}\n".format(sendfrom) \
          + "To: {}\n".format(sendto) \
          + "CC:{}\n".format(sendfrom) \
          + "Subject: {}\n\n".format(subject) \
          + message
    p.write(email)
    status = p.close()
    if status is not None:
        print("Sendmail exit status", status)

def match_list(string, regex_list, **kwargs):
    '''
    match a list of regex pattern to get to the point in a long string
    instead of having a long complete regex that is hard to handle
    the match is non-greedy so that you can go step by step
    '''
    #data = deepcopy(string)
    data = string
    mat = None
    res = None
    # group number to be used as returned value
    use_group = int(kwargs.get('use_group', 1))
    if not isinstance(regex_list, list):
        regex_list = [regex_list]
    for reg in regex_list:
        mat = re.search(reg, data, re.M|re.S)
        if not mat:
            print('warn: no pattern matched for {}'.format(reg))
            return res
        data = data[mat.end():]

    if mat:
        if mat.lastindex and mat.lastindex >= use_group:
            res = mat.group(use_group)
        else:
            print('==No group {} found in the match'.format(str(use_group)))

    else:
        print('==No match found')

    return res
