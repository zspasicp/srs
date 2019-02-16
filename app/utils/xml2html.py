import os
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # noqc
sys.path.insert(0, path)  # noqc

from optparse import OptionParser  # noqa
import lxml.etree as ET  # noqa


def create_opt_parser():
    """
    Option parser function

    :return: OptionParser
    """
    parser = OptionParser(usage="%prog -i INPUT_CONFIGURATION_FILE -o OUTPUT_FILE" +
                          " -x INPUT_XSL_FILE",
                          version="%prog 0.1")
    parser.add_option("-i",
                      "--input",
                      dest="input_file",
                      help=("Input configuration XML file name"))
    parser.add_option("-o",
                      "--output",
                      dest="output_file",
                      help=("Output file name"))
    parser.add_option("-x",
                      "--xsl",
                      dest="xsl_file",
                      help=("Input XSL file name"))
    return parser
# end def create_opt_parser


if __name__ == "__main__":
    parser = create_opt_parser()
    opts = parser.parse_args()[0]
    if opts.output_file is None or opts.input_file is None or opts.xsl_file is None:
        parser.print_help()
        sys.exit(0)
    dom = ET.parse(opts.input_file)
    xslt = ET.parse(opts.xsl_file)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    with open(opts.output_file, "w") as html:
        html.write(str(ET.tostring(newdom, pretty_print=True)))

### __END__ xml2html
