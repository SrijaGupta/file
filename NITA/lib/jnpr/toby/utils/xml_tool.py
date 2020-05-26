# coding: UTF-8
# pylint: disable=invalid-name
"""XML related methods"""
__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import jxmlease
import json


class xml_tool():
    """XML related methods"""
    def __init__(self):
        """INIT"""
        self.pprint = lambda x: json.dumps(x, indent=4, sort_keys=True, default=str, ensure_ascii=False)

        self.lxml_response_parser = lambda xml_obj: jxmlease.parse_etree(xml_obj)
        self.jxmlease_response_to_dict = lambda xml_obj: json.loads(self.pprint(xml_obj))
        self.lxml_response_to_dict = lambda xml_obj: eval(self.pprint(self.lxml_response_parser(xml_obj)))

        self.xml_string_to_dict = lambda xml_str: jxmlease.parse(xml_str)
        self.dict_to_xml_string = lambda xml_dict: jxmlease.emit_xml(xml_dict)
        self.xml_obj_to_string = lambda xml_obj: self.dict_to_xml_string(self.lxml_response_parser(xml_obj))

        self.xml_str_to_dict = self.xml_string_to_dict
        self.dict_to_xml_str = self.dict_to_xml_string
        self.xml_obj_to_dict = self.lxml_response_parser

    def xml_to_pure_dict(self, xml_structure, **kwargs):
        """Transit XML structure to pure python DICT whatever it is from jxml, jxmlease or xml string

        :param BOOL pprint:
            *OPTIONAL* pretty print DICT to stdout. default: False

        :return: DICT contain xml structure. If xml_structure is a dict already, or None, True, False, return directly.
        """
        options = {}
        options["pprint"] = kwargs.pop("pprint", False)

        if xml_structure in (None, True, False):
            return xml_structure

        type_keyword = re.search(r"class\s+['\"](\S+)['\"]", str(type(xml_structure))).group(1).split(r".")[0].lower()

        if type_keyword == "dict":
            return_value = xml_structure
        elif type_keyword == "lxml":
            return_value = self.lxml_response_to_dict(xml_structure)
        elif type_keyword == "str":
            return_value = self.jxmlease_response_to_dict(self.xml_str_to_dict(xml_structure))
        elif type_keyword == "jxmlease":
            return_value = self.jxmlease_response_to_dict(xml_structure)
        else:
            raise ValueError("Given xml_structure must be XML string, lxml object or jxmlease object, but got '{}'".format(type(xml_structure)))

        if options["pprint"] is True:
            print(self.pprint(return_value))

        return return_value

    @staticmethod
    def strip_xml_response(xml_response, rpc_tag="rpc-reply", ha_keyword="multi-routing-engine-results", return_list=True):
        """Strip XML structure for SA and HA topo both"""
        if rpc_tag in xml_response:
            xml_response = xml_response[rpc_tag]

        if "cli" in xml_response:
            del xml_response["cli"]

        if ha_keyword in xml_response:
            xml_response = xml_response[ha_keyword]["multi-routing-engine-item"]

        if return_list is True and not isinstance(xml_response, (list, tuple)):
            xml_response = [xml_response, ]

        return xml_response
