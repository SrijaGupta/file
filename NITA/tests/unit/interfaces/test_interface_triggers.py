import unittest2 as unittest
import builtins
from mock import patch, Mock, MagicMock, call
from jnpr.toby.init.init import init
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.juniper.junos import Juniper
from collections import OrderedDict, defaultdict
from jnpr.toby.utils.Vars import Vars
from jnpr.toby.hldcl.device import Device
import jnpr.toby.engines.config.config
import jnpr.toby.engines.config.config_utils as config_utils
from jnpr.toby.engines.events.event_engine_utils import me_object, device_handle_parser, interface_handler_to_ifd, get_pfe, elog, _get_dev_handle
from jnpr.toby.interfaces.interface_triggers import _get_bcm_index,_pic_on_off,_check_pic_on_off,_check_10ge_xfp_laser,_check_cfp_laser,_get_qsfp_index,_check_ifd_cfg_activate_deactivate_orig,_check_sonet_xfp_laser,_check_agent_smith_laser,_check_mtip_gpcs_laser,_check_ifd_cfg_enable_disable,_check_ifd_shell_up_down,_set_qfx_sfp_laser,_set_10ge_xfp_laser,_set_10ge_dpc_xfp_laser,_set_t5e_10ge_sfpp_laser,_set_sonet_xfp_laser,_set_mtip_gpcs_laser,_set_agent_smith_laser,_set_cfp_laser,_set_cmic_laser,_set_qsfp_laser,_ifd_cfg_enable_disable,_ae_cfg_enable_disable,_option2_ifd_cfg_set_delete,_ifd_shell_up_down,_ae_shell_up_down,_set_ifdev_laser,_check_ifd,_check_cfp_laser,_check_fpc_restart,_check_fpc_on_off,_get_ifd_func_list,_check_ifd_cfg_activate_deactivate,_mic_on_off,_check_mic_on_off,_set_picd_laser

class Testevent_engine(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock(spec=init)
        t.is_robot = True
        t._script_name = "test_init"
        t.background_logger = MagicMock()
        t.log = MagicMock()
        create_t_data()
        t.resources = t.t_dict['resources']
        t.__getitem__ = MagicMock(return_value=t.t_dict['resources'])
        builtins.dh = MagicMock(spec=Device)
        dh.get_version = MagicMock(return_value='16.1')
        dh.get_model = MagicMock(return_value='mx240')
        builtins.tv = {'r0__name': 'tetra'}
        
    def test_ifd_cfg_activate_deactivate_orig(self):
        dh = MagicMock()

        # action is None
        dh.config.return_value = Response(status=True, response='inactive:')
        self.assertTrue(_check_ifd_cfg_activate_deactivate_orig(dh, 'xe-0/0/0', action=None))
       
        # action is 'on' 
        dh.config.return_value = Response(status=True, response='test')
        self.assertTrue(_check_ifd_cfg_activate_deactivate_orig(dh, 'xe-0/0/0', action='on'))
 
        # action is 'off'
        dh.config.return_value = Response(status=False, response='inactive')
        self.assertFalse(_check_ifd_cfg_activate_deactivate_orig(dh, 'xe-0/0/0', action='off')) 

    def test_ifd_cfg_activate_deactivate(self):
        dh = MagicMock()

        dh.config.return_value = Response(status=True, response='inactive:')
        self.assertTrue(_check_ifd_cfg_activate_deactivate(dh, 'xe-0/0/0', action=None))

        dh.config.return_value = Response(status=True, response='test')
        self.assertTrue(_check_ifd_cfg_activate_deactivate(dh, 'xe-0/0/0', action='on'))

        dh.config.return_value = Response(status=False, response='inactive')
        self.assertFalse(_check_ifd_cfg_activate_deactivate(dh, 'xe-0/0/0', action='off'))

    def test_check_ifd_cfg_enable_disable(self):
        dh = MagicMock()

        dh.config.return_value = Response(status=True, response='disable')
        self.assertTrue(_check_ifd_cfg_enable_disable(dh, 'xe-0/0/0', action=None))
        dh.config.return_value = Response(status=True, response='test')
        self.assertTrue(_check_ifd_cfg_enable_disable(dh, 'xe-0/0/0', action='enable'))
       
        dh.config.return_value = Response(status=False, response='inactive')
        self.assertFalse(_check_ifd_cfg_enable_disable(dh, 'xe-0/0/0', action='off'))

    def test_check_ifd_shell_up_down(self):
        dh = MagicMock()
        
        dh.shell.return_value = Response(status=True, response='DOWN')
        self.assertTrue(_check_ifd_shell_up_down(dh, 'xe-0/0/0', action=None))
          
        dh.shell.return_value = Response(status=True, response='test')
        self.assertTrue(_check_ifd_shell_up_down(dh, 'xe-0/0/0', action='on'))
      
        dh.shell.return_value = Response(status=False, response='inactive')
        self.assertFalse(_check_ifd_shell_up_down(dh, 'xe-0/0/0', action='off'))

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_10ge_xfp_laser(self,mocksh):
        dh = MagicMock()
        _set_10ge_xfp_laser(dh, 'xe-0/0/0', action='on')
        _set_10ge_xfp_laser(dh, 'xe-0/0/0', action='off')


    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_10ge_dpc_xfp_laser(self,mocksh):
        dh = MagicMock()
        _set_10ge_dpc_xfp_laser(dh, 'xe-0/0/0', action='on')
        _set_10ge_dpc_xfp_laser(dh, 'xe-0/0/0', action='off')    

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_sonet_xfp_laser(self,mocksh):
        dh = MagicMock()
        _set_sonet_xfp_laser(dh, 'xe-0/0/0', action='on')
        _set_sonet_xfp_laser(dh, 'xe-0/0/0', action='off')

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_t5e_10ge_sfpp_laser(self,mocksh):
        dh = MagicMock()
        _set_t5e_10ge_sfpp_laser(dh, 'xe-0/0/0', action='on')
        _set_t5e_10ge_sfpp_laser(dh, 'xe-0/0/0', action='off')
        _set_t5e_10ge_sfpp_laser(dh, 'xe-0/0/0', action='flap')


    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_agent_smith_laser(self,mocksh):
        dh = MagicMock()
        _set_agent_smith_laser(dh, 'xe-0/0/0', action='on')
        _set_agent_smith_laser(dh, 'xe-0/0/0', action='off')


    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_mtip_gpcs_laser(self,mocksh):
        dh = MagicMock()
        _set_mtip_gpcs_laser(dh, 'xe-0/0/0', action='on')
        _set_mtip_gpcs_laser(dh, 'xe-0/0/0', action='off')
        _set_mtip_gpcs_laser(dh, 'xe-0/0/0', action='flap')
        _set_mtip_gpcs_laser(dh, ifd=None, action='flap')

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_cfp_laser(self,mocksh):
        dh = MagicMock()
        _set_cfp_laser(dh, 'xe-0/0/0', action='on')
        _set_cfp_laser(dh, 'xe-0/0/0', action='off')


    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_cmic_laser(self,mocksh):
        dh = MagicMock()
        _set_cmic_laser(dh, 'xe-0/0/0', action='on')
        _set_cmic_laser(dh, 'xe-0/0/0', action='off')


    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_qsfp_laser(self,mocksh):
        dh = MagicMock()
        _set_qsfp_laser(dh, 'xe-0/0/0', action='on')
        _set_qsfp_laser(dh, 'xe-0/0/0', action='off')
        _set_qsfp_laser(dh, 'xe-0/0/0:0', action='on')
        _set_qsfp_laser(dh, 'xe-0/0/0:0', action='off')
        _set_qsfp_laser(dh, 'xe-0/0/', action='off')

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_qfx_sfp_laser(self,mocksh):
        dh = MagicMock()
        _set_qsfp_laser(dh, 'et-0/0/0', action='on')
        _set_qsfp_laser(dh, 'et-0/0/0', action='off')
        _set_qsfp_laser(dh, 'et-0/0/0:0', action='on')
        _set_qsfp_laser(dh, 'et-0/0/0:0', action='off')
        _set_qsfp_laser(dh, 'et-0/0/', action='off')

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_ifd_cfg_enable_disable(self,mocksh):
        dh = MagicMock()   
        _ifd_cfg_enable_disable(dh, 'xe-0/0/0', action='on')
        _ifd_cfg_enable_disable(dh, 'xe-0/0/0', action='off')
        _ifd_cfg_enable_disable(dh, 'xe-0/0/0', action='flap')
        
    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_ae_cfg_enable_disable(self,mocksh):
        dh = MagicMock()   
        _ae_cfg_enable_disable(dh, 'ae0', action='enable')
        _ae_cfg_enable_disable(dh, 'ae0', action='disable')
        _ae_cfg_enable_disable(dh, 'ae0', action='flap')


    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_ifd_shell_up_down(self,mocksh):
        dh = MagicMock()
        _ifd_shell_up_down(dh, 'xe-0/0/0', action='up')
        _ifd_shell_up_down(dh, 'xe-0/0/0', action='down')
        _ifd_shell_up_down(dh, 'xe-0/0/0', action='flap')


    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_ae_shell_up_down(self,mocksh):
        dh = MagicMock()
        _ae_shell_up_down(dh, 'ae0', action='up')
        _ae_shell_up_down(dh, 'ae0', action='down')
        _ae_shell_up_down(dh, 'ae0', action='flap')
        
   
    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_ifdev_laser(self,mocksh):
        dh = MagicMock()
        _set_ifdev_laser(dh, 'xe-0/0/0', action='on')
        _set_ifdev_laser(dh, 'xe-0/0/0', action='off')

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_check_cfp_laser(self,mockshf):
        dh = MagicMock()

        # state is 'on'
        dh.vty.return_value = Response(status=True, response=' Tx laser disable: 1 Clear')
        self.assertEqual(_check_cfp_laser(dh, 'ge-0/0/0', action=None),'on')

        # state is 'off'
        dh.vty.return_value = Response(status=True, response=' Tx laser disable: 1 Set')
        self.assertEqual(_check_cfp_laser(dh, 'ge-0/0/0', action=None),'off')

        dh.vty.return_value = Response(status=True, response=' Tx laser disable: 1 Cle')
        self.assertEqual(_check_cfp_laser(dh, 'ge-0/0/0', action=None),None)

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_check_mtip_gpcs_laser(self,mockshf):
        dh = MagicMock()

        # state is 'on'
        dh.vty.return_value = Response(status=True, response=' control : 0x00001140')
        self.assertEqual(_check_mtip_gpcs_laser(dh, 'ge-0/0/0', action=None),'on')

        # state is 'off'
        dh.vty.return_value = Response(status=True, response=' control : 0x00001d40')
        self.assertEqual(_check_mtip_gpcs_laser(dh, 'ge-0/0/0', action=None),'off')

        dh.vty.return_value = Response(status=True, response=' control : 0x00001d')
        self.assertEqual(_check_mtip_gpcs_laser(dh, 'ge-0/0/0', action=None),None)

    @patch("jnpr.toby.interfaces.interface_triggers._get_bcm_index",return_value='7')
    def test_check_agent_smith_laser(self,mockshf):
        dh = MagicMock()

        # state is 'on'
        dh.vty.return_value = Response(status=True, response='7     0/0/0    2      ON')
        self.assertEqual(_check_agent_smith_laser(dh, 'xe-0/0/0', action=None),'on')

        # state is 'off'
        dh.vty.return_value = Response(status=True, response='7      0/0/0   2      OFF')
        self.assertEqual(_check_agent_smith_laser(dh, 'xe-0/0/0', action=None),'off')

        dh.vty.return_value = Response(status=True, response='7      0/0/0   2      BOOG')
        self.assertEqual(_check_agent_smith_laser(dh, 'xe-0/0/0', action=None),None)

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_check_sonet_xfp_laser(self,mockshf):
        dh = MagicMock()

        # state is 'on'
        dh.vty.return_value = Response(status=True, response=' Tx power low warn: 1 Clear')
        self.assertEqual(_check_sonet_xfp_laser(dh, 'ge-0/0/0', action=None),'on')

        # state is 'off'
        dh.vty.return_value = Response(status=True, response=' Tx power low warn: 1 Set')
        self.assertEqual(_check_sonet_xfp_laser(dh, 'ge-0/0/0', action=None),'off')

        dh.vty.return_value = Response(status=True, response=' Tx power low warn:')
        self.assertEqual(_check_sonet_xfp_laser(dh, 'ge-0/0/0', action=None),None)

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_check_10ge_xfp_laser(self,mockshf):
        dh = MagicMock()

        # state is 'on'
        dh.vty.return_value = Response(status=True, response=' Tx not ready: 1 Clear')
        self.assertEqual(_check_10ge_xfp_laser(dh, 'ge-0/0/0', action=None),'on')

        # state is 'off'
        dh.vty.return_value = Response(status=True, response=' Tx not ready: 1 Set')
        self.assertEqual(_check_10ge_xfp_laser(dh, 'ge-0/0/0', action=None),'off')

    def test_check_ifd(self):
        dh = MagicMock()

        # state is 'on'
        dh.cli.return_value = Response(status=True, response='xe-0/0/0 up up')
        self.assertEqual(_check_ifd(dh, 'xe-0/0/0', action='on'),'on')

        # state is 'off'
        dh.cli.return_value = Response(status=True, response='xe-0/0/0 up down')
        self.assertEqual(_check_ifd(dh, 'xe-0/0/0', action='off'),'off')

        # state is 'not found default to off'
        dh.cli.return_value = Response(status=True, response='error: device xe-0/0/46 not found')
        self.assertEqual(_check_ifd(dh, 'xe-0/0/46', action='off'),'off')

        # state is 'admin_down'
        dh.cli.return_value = Response(status=True, response='xe-0/0/0 down down')
        self.assertEqual(_check_ifd(dh, 'xe-0/0/0', action='up'),True)

        # state is None
        dh.cli.return_value = Response(status=True, response='xe-0/0/0 down up')
        self.assertIsNone(_check_ifd(dh, 'xe-0/0/0', action=None))
        
    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_check_fpc_on_off(self,mockshf):
        dh = MagicMock()

        # state is 'online'
        dh.cli.return_value = Response(status=True, response='Offline')
        self.assertEqual(_check_fpc_on_off(dh, 'xe-0/0/0', action='offline', wait_to_check=0), False)
        
        dh.cli.return_value = Response(status=True, response='  0  Online            51     15          0       15     15     14    3584        6         25')
        self.assertEqual(_check_fpc_on_off(dh, 'xe-0/0/0', action='online', wait_to_check=0), True)

    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_check_fpc_restart(self,mockshf):
        dh = MagicMock()

        # state is 'online'
        dh.cli.return_value = Response(status=True, response='online')
        self.assertEqual(_check_fpc_restart(dh, 'xe-0/0/0', action='online', wait_to_check=0), None)
    
    # @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_check_pic_on_off(self):
        dh = MagicMock()
    
        # state is 'online'
        dh.cli.return_value = Response(status=True, response='    State    Online')
        self.assertEqual(_check_pic_on_off(dh, 'xe-0/0/0', action='on'), False)
    
        # state is 'offline'
        dh.cli.return_value = Response(status=True, response='    State    Offline')
        self.assertEqual(_check_pic_on_off(dh, 'xe-0/0/0', action='off'), False)
        
    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_pic_on_off(self,mocksh):
        dh = MagicMock()
        dh.get_model.return_value = 'mx80'
        _pic_on_off(dh, 'xe-0/0/0', action='online')
        dh.get_model.return_value = 'mx2020'
        dh.cli.return_value = Response(status=True, response='FPC slot 2 does not support this command')
        self.assertEqual(_pic_on_off(dh, 'xe-0/0/0', action='online', wait=0), True)
        self.assertEqual(_pic_on_off(dh, 'xe-0/0', action='online', debug_log_on=True), False)       
 
    @patch("jnpr.toby.interfaces.interface_triggers._find_mic_type",return_value='1')
    def test_mic_on_off(self, mic_patch):
        dh = MagicMock()
        dh.get_model.return_value = 'mx80'
        _mic_on_off(dh, 'xe-0/0/0', action='online') 
        dh.get_model.return_value = 'mx2020' 
        dh.cli.return_value = Response(status=True, response='FPC slot 2 does not support this command')
        self.assertEqual(_mic_on_off(dh, 'xe-0/0/0', action='online', wait=0), True)
        self.assertEqual(_mic_on_off(dh, 'xe-0/0', action='online', debug_log_on=True), False)
    
    @patch("jnpr.toby.interfaces.interface_triggers._find_mic_type",return_value='2')
    def test_check_mic_on_off(self, mic_patch):
        dh = MagicMock()
        result = _check_mic_on_off(dh, 'xe-0/0/0', action='on', debug_log_on=True)
        self.assertEqual(result, False)

        # state is 'online'
        dh.fru_info = {}
        dh.cli.return_value = Response(status=True, response='    State    Online')
        result = _check_mic_on_off(dh, 'xe-0/0/0', action='on')
        self.assertEqual(result, True)

        # state is 'offline'
        dh.fru_info = {}
        dh.cli.return_value = Response(status=True, response='    State    Offline')
        result = _check_mic_on_off(dh, 'xe-0/0/0', action='off')
        self.assertEqual(result, True)
        
    @patch("jnpr.toby.interfaces.interface_triggers.get_pfe",return_value=None)
    def test_set_cfp_laser(self,mocksh):
        dh = MagicMock()
        result_on = _set_picd_laser(dh, 'xe-0/0/0', action='on')
        self.assertEqual(result_on, None)
        result_off = _set_picd_laser(dh, 'xe-0/0/0', action='off')
        self.assertEqual(result_off, None)

        

def create_t_data():
    """
    Create t data
    :return:
        Returns t data
    """
    t.t_dict = dict()
    t.t_dict['resources'] = dict()
    t.t_dict['resources']['r0'] = dict()
    t.t_dict['resources']['r0']['interfaces'] = dict()
    t.t_dict['resources']['r0']['interfaces']['fe0'] = dict()
    t.t_dict['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'
    t.t_dict['resources']['r0']['interfaces']['fe0']['link'] = 'link'
    t.t_dict['resources']['r0']['system'] = dict()
    t.t_dict['resources']['r0']['system']['dh'] = "test"
    t.t_dict['resources']['r0']['system']['primary'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'dummy_host'
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['osname'] = 'JunOS'
    t.t_dict['resources']['r0']['system']['primary']['name'] = 'dummy_host'
    t.t_dict['resources']['r0']['system']['primary']['model'] = 'mx'
    t.t_dict['resources']['r0']['system']['primary']['make'] = 'Juniper'
    t.t_dict['resources']['r0']['system']['primary']['osname'] = 'JunOS'


if __name__ == '__main__':
   unittest.main()
