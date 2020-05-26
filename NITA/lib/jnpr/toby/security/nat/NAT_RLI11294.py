from jnpr.toby.utils.message import message
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.junos.dut_tool import dut_tool
import jxmlease
import re


def configure_nat_pool_range(device=None, flavour=None, pool=None, low_rng=None, high_rng=None):
    """
    Configuring a NAT pool
    python:  configure_nat_pool_range (device=r0, flavour='source', pool='s1', low_rng='2020::10', high_rng='2020::20', commit =True)
    robot:  Configure Nat Pool Range    device={r0}  flavour=source  pool=s1  low_rng=2020::10  high_rng=2020::20  commit={True}

    """



    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat pool")
    if flavour is None:
        device.log(level="ERROR", msg="'flavour' is a mandatory parameter for configuring nat pool")
        raise Exception("'flavour' is a mandatory parameter for configuring nat pool")
    if pool is None:
        device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring " + flavour + " nat pool")
        raise Exception("'pool' is a mandatory parameter for configuring " + flavour + " nat pool")
    if low_rng is None:
        device.log(level="ERROR", msg="'low_rng' is a mandatory parameter for configuring " + flavour + " nat pool")
        raise Exception("'low_rng' is a mandatory parameter for configuring " + flavour + " nat pool")
    if high_rng is None:
        high_rng = low_rng
    if device is not None:
        device.config(command_list=['set security nat ' + flavour + ' pool ' + pool + ' address ' + low_rng + ' to ' + high_rng])
        device.commit(timeout=120)


def del_nat(device=None):
    """
    delete security nat 
    robot:  Del Nat    device={r0}

    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat pool")
    device.config(command_list=['delete security nat'])
    return device.commit(timeout=120)




def chk_src_summary(device=None, pool=None, low_rng=None, high_rng=None, port_rng=None, pool_id=None, tot_addr=None, H_A_B=None, rout_inst=None):
    """
    robot Chk Src Summary    device=${r0}  pool=s1  low_rng=2020::10  high_rng=2020::20

    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat pool")
    if low_rng is None:
        raise Exception("' low_rng ' needed")
    if high_rng is None:
        high_rng = low_rng
    if device is not None:
 #   src_cmd = ('show security nat source summary' + pool)
        device.cli(command='show security nat source pool ' + pool).response()
        result = device.cli(command='show security nat source pool ' + pool, format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)
    print(' check for S1 S2 src pool ')

    if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['pool-name']) != pool:
        device.log(level='ERROR', message='s1 pool info not visible')
        raise Exception("value not present")
    if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['address-range-low']) != low_rng:
        device.log(level='ERROR', message='s1 pool does not have low rnage address proper')
        raise Exception("value not present")
    if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['address-range-high']) != high_rng:
        device.log(level='ERROR', message='s1 pool does not have high range  address proper')
        raise Exception("value not present")
    if port_rng is not None:
        if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-port-translation']) != port_rng:
            device.log(level='ERROR', message='pool does not have proper port status ...')
            raise Exception("value not present")
    if tot_addr is not None:
        if(status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['total-pool-address']) != tot_addr:
            device.log(level='ERROR', message='pool does not have proper total address  number .....')
            raise Exception("value not present")
    if H_A_B is not None: 
        if(status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['host-address-base']) != H_A_B:
            device.log(level='ERROR', message='pool does not have proper host address base..........')
	                             #raise Exception("value not present")
    if rout_inst  is not None:
        if(status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['routing-instance-name']) != rout_inst:
            device.log(level='ERROR', message='pool does not have proper routing instance............')
            raise Exception("value not present")
        else:
            device.log(level='INFO', message='all pool info there ')


#def conf_rotng_inst (device=None, intf=None, routng_inst=None, routng_opt=None, instance-tpe=None, inet=None):
#def configure_rotng_inst (device, intf, routng_inst, routng_opt, instance-tpe) :
 #   if device is None:
  #      raise Exception("'device' is mandatory parameter for configuring nat pool")
  #  if intf is None:
  #      raise Exception("'intf' is mandatory parameter for configuring routing instance")
  #  if routng_inst is None:
  #      raise Exception("'routng_inst' is mandatory parameter for configuring routing instance")
  #  if routng_opt is None:
  #      raise Exception("'routng_opt' is mandatory parameter for configuring routing instance")
  #  if instance-tpe is None:
  #      raise Exception("'inet' is mandatory parameter for configuring routing instance")

   # if device is not None:
  #      device.config(command_list=['set routing-instances '+ routng_inst +' red instance-type '+instance-tpe ,
   #                                 'set routing-instances '+ routng_inst +' interface '+intf,
   #                                 'set routing-instances '+ routng_inst +' routing-options '+routng_opt+' rib-group inet if-rib2',
   #                                 'set routing-options '+routng_opt+'  rib-group inet if-rib1',
   #                                 'set routing-options static rib-group if-rib1',
   #                                 'set routing-options rib-group if-rib2 import-rib red.inet.0',
   #                                 'set routing-options rib-group if-rib2 import-rib inet.0',
   #                                 'set routing-options rib-group if-rib1 import-rib inet.0',
   #                                 'set routing-options rib-group if-rib1 import-rib red.inet.0'])
 #       device.commit(timeout=240)



def chk_src_summary_rout_inst(device, routng_inst, pool):
    """
    Robot:-Chk Src Summary Rout Inst    device=${r0}  routng_inst=red  pool=s1 

    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat pool")
    if routng_inst is None:
        raise Exception("'routng_inst' is mandatory parameter for configuring routing instance")

    if device is not None:
        device.cli(command='show security nat source pool ' + pool).response()
        result = device.cli(command='show security nat source pool ' + pool, format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)
        print(' check for S1 S2 src pool ')
#       if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['routing-instance-name']) != routng_inst:

        if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['routing-instance-name']) != routng_inst:
            device.log(level='ERROR', message='s1 pool does not have correct routing instance')
            raise Exception("value not present")


def chk_src_summary_duo(device=None, pool=None, low_rng=None, high_rng=None, indx=None):
    """
    Robot :-  Chk Src Summary Duo     device=${r0}  pool=s1  low_rng=2020::10  high_rng=2020::20  indx=1

    """ 
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat pool")
#    indx = indx - 1
    if device is not None:
 #   src_cmd = ('show security nat source summary' + pool)
        device.cli(command='show security nat source pool ' + pool).response()
        result = device.cli(command='show security nat source pool ' + pool, format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)
        print(' check for S1 S2 src pool ')

        if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['pool-name']) != pool:
            device.log(level='ERROR', message='s1 pool info not visible')
            raise Exception("value not present")
        if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['address-range-low'][1]) != low_rng:
            device.log(level='ERROR', message='s1 pool does not have low rnage address proper')
            raise Exception("value not present")
        if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['address-range-high'][1]) != high_rng:
            device.log(level='ERROR', message='s1 pool does not have high range  address proper')
            raise Exception("value not present")

        else:
            device.log(level='INFO', message='s1 pool info there ')


def chk_src_summary_prefix(device=None, pool=None, addr=None):
    """
    Robot :-  Chk Src Summary Prefix      device=${r0}  pool=s1  addr=2010::/64

    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat pool")
    if device is not None:
        device.cli(command='show security nat source pool ' + pool).response()
        result = device.cli(command='show security nat source pool ' + pool, format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    print(' check for S1 src pool ')
    if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['pool-name']) != pool:
        device.log(level='ERROR', message='s1 pool info not visible')
        raise Exception("value not present")
    if (status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['address-range-low']) != addr:
        device.log(level='ERROR', message='s1 pool does not have address prefixx proper')
        raise Exception("value not present")
