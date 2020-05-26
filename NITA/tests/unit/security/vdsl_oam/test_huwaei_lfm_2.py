#!/usr/bin/python3
import unittest
from jnpr.toby.security.vdsl_oam import huwaei_lfm_2


class test_dev_conf(unittest.TestCase):
	def test_connect_dslam_con(self):
		with self.assertRaises(Exception):
			huwaei_lfm_2.connect_dslam_con(dslam=None)
		with self.assertRaises(Exception):
			huwaei_lfm_2.connect_dslam_con(dslam='cnrd-ts64',dslam_con_port=None)
		self.assertEqual(huwaei_lfm_2.connect_dslam_con(dslam='cnrd-ts64',dslam_con_port=7005),None)
			
	def test_configure_lfm_on_dslam(self):
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection = None)
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(dslam_port = None)
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(command = None)
		#handler = huwaei_lfm_2.connect_dslam_con(dslam='cnrd-ts64',dslam_con_port=7005)
		handler = True
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='enable_efm_active')
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='enable_efm_passive')
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='disable_efm')
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='config_port_untag')
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='config_port_tag')
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='invoke_loopback_forward')
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='invoke_loopback_drop')
		with self.assertRaises(Exception):	
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='reset_stat')
		with self.assertRaises(Exception):
			huwaei_lfm_2.configure_lfm_on_dslam(connection=handler,dslam_port='0/1/25',command='reset_dslam')

	def test_check_loop_back(self):
		#handler = huwaei_lfm_2.connect_dslam_con(dslam='cnrd-ts64',dslam_con_port=7005)
		handler = True
		with self.assertRaises(Exception):
			huwaei_lfm_2.check_loop_back(connection=None)
		with self.assertRaises(Exception):
			huwaei_lfm_2.check_loop_back(connection=handler,dslam_port=None)
		with self.assertRaises(Exception):
			huwaei_lfm_2.check_loop_back(connection=handler,dslam_port='0/1/25',packet_count=None)
		with self.assertRaises(Exception):
			huwaei_lfm_2.check_loop_back(connection=handler,dslam_port='0/1/25',packet_count=0)


if __name__ == '__main__':
	unittest.main()		
