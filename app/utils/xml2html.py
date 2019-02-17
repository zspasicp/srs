import lxml.etree as ET
import os


def create_html(input_xml):
    dom = ET.XML(input_xml)
    dir_name = os.path.dirname(__file__)
    xslt = ET.parse(os.path.join(dir_name, 'nmap.xsl'))
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    data = str(ET.tostring(newdom, pretty_print=True))
    return data
