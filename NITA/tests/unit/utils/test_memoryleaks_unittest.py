import os
import unittest
import logging
import sys
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils import memoryleaks
from jnpr.toby.utils.memoryleaks import __proto_memoryleaks as _proto_memoryleaks
from mock import MagicMock, patch
from jnpr.toby.utils.response import Response

class Memoryleaks_unittest(unittest.TestCase):

    def setUp(self):
        logging.info("\n##################################################\n")
        self.dev = MagicMock(spec=Juniper)

    def tearDown(self):
        logging.info("CLOSE SESSION ...\n")
        self.dev.close()
    
    @patch('jnpr.toby.utils.memoryleaks.sleep')
    def test_check_memory_leaks(self,sleep_patch):
        logging.info("Test case 1: with required arguments ")
        result = memoryleaks.check_memory_leaks(device=self.dev, protocol='ip', action='set',timeout=0,interval=1)
        self.assertEqual(result, True, " Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)

        logging.info("Test case 2: optional argument cmd ")
        cmd = "show system buffers"
        result = memoryleaks.check_memory_leaks(device=self.dev, protocol='ip', action='set', cmd=cmd,timeout=0,interval=1)
        self.assertEqual(result, True, " Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)

        logging.info("Test case 3: reset_config argument")
        cmd = "show system buffers"
        result = memoryleaks.check_memory_leaks(device=self.dev, protocol='ip', action='set', cmd=cmd, reset_config=1,timeout=0,interval=1)
        self.assertEqual(result, True, " Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)

        logging.info("Test case 4: __proto return value False")
        with patch('jnpr.toby.utils.memoryleaks.__proto_memoryleaks',return_value=False) as proto_patch:
            result = memoryleaks.check_memory_leaks(device=self.dev, protocol='ip', action='set',timeout=0,interval=1)
            self.assertEqual(result, False, " Failed, Result = %s"%result)
            logging.info(" Passed, Result = %s"%result)

        logging.info("Test case 5: __proto return value False")
        self.dev.cli = MagicMock(return_value=Response(response=''))
        result = memoryleaks.check_memory_leaks(device=self.dev, protocol='ip', action='set',timeout=0,interval=1)
        self.assertEqual(result, True, " Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)
        
        with patch('jnpr.toby.utils.memoryleaks.__proto_memoryleaks',return_value=False) as proto_patch:
            logging.info("Test case 6: commit error test (negative case)")
            self.dev.cli = MagicMock(return_value=Response(response=''))
            self.dev.commit = MagicMock(return_value=Exception('Error'))
            try :
                result = memoryleaks.check_memory_leaks(device=self.dev, protocol='ip', action='set',keep_rt_instance=True,timeout=0,interval=1)
            except :
                self.dev.commit = MagicMock(return_value=Response(response=''))
                result = memoryleaks.check_memory_leaks(device=self.dev, protocol='ip', action='set',keep_rt_instance=True,timeout=0,interval=1)
            self.assertEqual(result,False, " Failed, Result = %s"%result)
            logging.info(" Passed, Result = %s"%result)

        logging.info(" END : test_check_memory_leaks ")


    @patch('jnpr.toby.utils.memoryleaks.task_memory_snapshot')
    def test_proto_memoryleaks(self,records):
        logging.info("################################################################")
        logging.info("START : test_proto_memoryleaks") 

        logging.info("Test case 1:Without arguments ")
        records.return_value={'Protocol count24': ['10', '280'],
 'bfd_proto_block12': ['1', '16'],
 'bit_range20': ['3', '72'],
 'block_id_space24': ['20', '560'],
 'task_mem_cookies32': ['18', '648']}
        result = _proto_memoryleaks(device=self.dev)
        self.assertEqual(result, False, " Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)


        records.return_value={'Protocol count24': ['10', '280'],
 '': ['1', '16'],
 'bit_range20': ['3', '72'],
 'task_mem_cookies32': ['18', '648']}

        logging.info("Test case 2:With regex arguments ")
        pattern = '[\w\d\.]+|\w+[\w\d\.]+ [\w\d\.]+\s+'
        result = _proto_memoryleaks(device=self.dev, regex=pattern)
        self.assertEqual(result, False, " Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)


    def test_task_memory_command(self):
        logging.info("################################################################")
        logging.info("START : test_task_memory_command")

        logging.info("Test case 1: with filename argument ")
        result = memoryleaks.task_memory_command(device=self.dev, file_name='memoryleaks')
        self.assertEqual(result, True, " Failed, Result = %s"%result)
        logging.info("Passed, Result = %s"%result)


        logging.info("Test case 2: empty filename argument ")
        self.dev.cli=MagicMock(return_value=Response(response=''))
        result = memoryleaks.task_memory_command(device=self.dev,file_name='aa')
        self.assertEqual(result, False, " Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)


    def test_task_memory_snapshot(self):
        logging.info("################################################################")
        logging.info("START : test_task_memory_snapshot")

        logging.info("Test case 1 ")
        response="""  ------------------------- Overall Memory Report -------------------------
    96 T           -         -           -         17        1632          -
   100             -         1         100          2         200      16284
   144            22         -        3168       1187      170928      13216
  ------------------------ Allocator Memory Report ------------------------
  Name                 Size Alloc DTXP    Alloc     Alloc MaxAlloc  MaxAlloc
                             Size       Blocks     Bytes   Blocks     Bytes
  rt_nexthops_sesid_1     4     8            16       128       33       264
  patroot                 8    12           182      2184      185      2220
  gw_entry_list           8    12             2        24        2        24
  krt_remnant_rt          8    12  T          -         -       14       168
  dbg_sh_tdispatch_t     12    16            20       320       20       320
  struct krt_scb         12    16             3        48        4        64
  app_ctx_node_queue_t   12    16             -         -        4        64
  bfd_proto_block        12    16             1        16        1        16
  task_floating_socket   16    20             1        20        1        20
  tag_igp_context        16    20             3        60        3        60
  ldp_p2mp_proto_conte   16    20             1        20        1        20
  radix_inode_noattach   16    20   X       118      2360      244      4880
  policy_type_info       20    24            10       240       10       240
  itable                 20    24            50      1200       51      1224
  rt_table_family        20    24            19       456       19       456
  rt_table_name_node     20    24             5       120        6       144
  radix_root_struct      20    24            60      1440       64      1536
  RT STATIC IFA-Change   20    24             -         -       32       768
  bit_range              20    24             3        72        3        72
  rt_static_parms        20    24             -         -       14       336
  task_clocker_block     20    24             -         -        1        24
  krt_ifdest_updown_ev   20    24  T          -         -        2        48
  radix_inode_attached   20    24   X        29       696       46      1104
  rbroot                 24    28             4       112        5       140
  block_id_space         24    28            20       560       20       560
  Protocol count         24    28            10       280       11       308
  rt-entry state         24    28             6       168        8       224
  if_instance_ifl_node   24    28            12       336       12       336
  rte_mentry_t           24    28             -         -        2        56
  inet6_interface        24    28             1        28        1        28
  task_block             28    28           834     23352      834     23352
  rt_table_list          28    32             -         -        2        64
  if_link_iff            28    32            34      1088       81      2592
  rt_nexthop_addr_8      28    32             1        32        1        32
  rtlist_rtall_t         28    32             -         -        1        32
  task_mem_cookies       32    36            18       648       18       648
  ifae_local_tree_node   44    48             3       144        3       144
  noblock_cookie_blk     44    48  T          1        48        1        48
  rpd-trace-file-index   48    52             -         -        1        52
  rt_bit                 48    52            15       780       18       936
  rf_tree_t              48    52            15       780       15       780
  rte_table_t            48    52             -         -       20      1040
  rt_parse_memory     16380 16384  T P        -         -        1     16384
  noblock_buffer_blk  16380 16384  T P        2     32768        3     49152
  -------------------------------------------------------------------------
                                                  197248             276196
        
  -------------------------- Malloc Usage Report --------------------------
  Name                      Allocs     Bytes MaxAllocs  MaxBytes  FuncCalls
             Page directory size:      16384      Maximum:     16384"""

        self.dev.cli=MagicMock(return_value=Response(response=response))
        result = memoryleaks.task_memory_snapshot(device=self.dev)
        self.assertEqual(type(result), dict," Failed, Result = %s"%result)
        logging.info(" Passed, Result = %s"%result)


        logging.info("Test case 2 : ")
        response="""  ------------------------- Overall Memory Report -------------------------
  Size TXP    Allocs   Mallocs  AllocBytes  MaxAllocs    MaxBytes  FreeBytes
     8            16      7166       57456       7338       58704       8080
 16384 T P         1         -       16384          3       49152          -
  -------------------------------------------------------------------------
                                  2397430                3018966     912138

  ------------------------ Allocator Memory Report ------------------------
  Name                 Size Alloc DTXP    Alloc     Alloc MaxAlloc  MaxAlloc
                             Size       Blocks     Bytes   Blocks     Bytes
  rt_nexthops_sesid_1     4     8            16       128       33       264
  radix_inode_noattach   16    20   X       118      2360      244      4880
  policy_type_info       20    24            10       240       10       240
  itable                 20    24            50      1200       51      1224
  rt_table_family        20    24            19       456       19       456
  rt_table_name_node     20    24             5       120        6       144
  radix_root_struct      20    24            60      1440       64      1536
  RT STATIC IFA-Change   20    24             -         -       32       768
  bit_range              20    24             3        72        3        72
  rt_static_parms        20    24             -         -       14       336
  task_clocker_block     20    24             -         -        1        24
  krt_ifdest_updown_ev   20    24  T          -         -        2        48
  radix_inode_attached   20    24   X        29       696       46      1104
  inet6_interface        24    28             1        28        1        28
  task_block             28    28           834     23352      834     23352
  rt_table_list          28    32             -         -        2        64
  if_link_iff            28    32            34      1088       81      2592
  rt_nexthop_addr_8      28    32             1        32        1        32
  rtlist_rtall_t         28    32             -         -        1        32
  task_mem_cookies       32    36            18       648       18       648
  rt_tsi                 32    36            14       504       21       756
  com_01                 32    36             1        36        1        36
  proto conf             32    36            16       576       16       576
  task_lite_mpool        32    36             2        72        3       108
  rte_data_af_t          32    36             -         -       10       360
  rt_static_head         32    36            14       504       14       504
  task_job_subjob        32    36  T          -         -       33      1188
  rtlist_context         32    36  T          -         -        5       180
  Tag dyanmic PVC temp 1684  1820             1      1820        1      1820
  rt_parse_memory     16380 16384  T P        -         -        1     16384
  noblock_buffer_blk  16380 16384  T P        2     32768        3     49152
  -------------------------------------------------------------------------
                                                  197248             276196
        
  -------------------------- Malloc Usage Report --------------------------
  Name                      Allocs     Bytes MaxAllocs  MaxBytes  FuncCalls
              Total bytes in use:    9224192 (0% of available memory) """

        self.dev.cli=MagicMock(return_value=Response(response=response))
        result = memoryleaks.task_memory_snapshot(device=self.dev)
        self.assertEqual(type(result), dict, " Failed, Result = %s"%result)
        logging.info("\tPassed, Result = %s "%result)

        logging.info("Test case 3: No memory allocation data ")
        self.dev.cli=MagicMock(return_value=Response(response=''))
        result = memoryleaks.task_memory_snapshot(device=self.dev)
        self.assertEqual(type(result), dict, " Failed, Result = %s"%result)
        logging.info("\tPassed, Result = %s "%result)

    def test_check_args(self):

        logging.info(" Testing check_args......")
        logging.info("\tTest case 1 : Passing invalid argument in kw_dict")
        try :
            kvargs = {'term':'string'}
            result = memoryleaks.check_args(device=self.dev,valid_key=['name','match'],required_key=['name'],kw_dict=kvargs)
        except :
            logging.info("\t\tTestcase Passed")
        logging.info("\tTest case 2 : Passing invalid key in required_key")
        try :
            kvargs = {'name':'string'}
            result = memoryleaks.check_args(device=self.dev,valid_key=['name','match'],required_key=['term'],kw_dict=kvargs)
        except :
            logging.info("\t\tTestcase Passed")
        logging.info("\tTest case 2 : Passing valid required_keys")
        kvargs = {'name':'string'}
        result = memoryleaks.check_args(device=self.dev,valid_key=['name','match'],required_key=['name'],kw_dict=kvargs)
        self.assertEqual(result,kvargs,"Should return the Passed dict")
        logging.info("\t\tTestcase Passed")


if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name+".log", level=logging.INFO)
    unittest.main()

