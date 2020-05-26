#!/usr/bin/env python3
"""

Library to format XML for easier processing

"""

import os
import sys
from lxml import etree

def normalize_xml(xml_raw_content):
    '''
    Normalize XML output received from node for further processing
    '''

    # XSL style sheet path used for normalization
    style_sheet_template = os.path.join(os.path.abspath(os.path.dirname(__file__)), "style_sheet.xsl")

    # Parse argument content as XML
    parser = etree.XMLParser(remove_blank_text=True)
    try:
        xml_content = etree.XML(xml_raw_content, parser)
    except etree.XMLSyntaxError:
        t.log("Error", "Unable to parse input text as XML")
        return False
    xml_tree = xml_content.getroottree()

    # Normalize XML output for further processing
    try:
        xslt_content = etree.parse(style_sheet_template, parser)
    except OSError:
        t.log("Error", "Unable to access style sheet file : " +  style_sheet_template)
        sys.exit(1)
    except etree.XMLSyntaxError:
        t.log("Error", "Unable to parse style sheet file : " + style_sheet_template)
        sys.exit(1)
    xml_tree = xml_tree.xslt(xslt_content)

    # Remove rpc-reply and cli tags from output
    sub_tree = xml_tree.getroot()[0]

    return sub_tree
