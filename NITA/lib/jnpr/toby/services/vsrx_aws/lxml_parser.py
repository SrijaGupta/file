''' This code applies xslt style sheet to the xml file '''
import lxml.etree as ET

def convert_config(xml_filename, \
                    xslt_filename='/homes/manasahg/customer-gateway-juniper-junos-j.xslt', \
                    vsrx_config_file='/homes/manasahg/vsrx-config.txt'):

    ''' Parses the xml file using the xslt style sheet
        to VSRX router command format,
        dumps the output to a file and returns the filename'''

    dom = ET.parse(xml_filename)
    xslt = ET.parse(xslt_filename)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    try:
        file_handler = open(vsrx_config_file, 'w')
        file_handler.write(str(newdom))
        file_handler.close()
    except IOError as error:
        print(error)
        return None
    return vsrx_config_file
