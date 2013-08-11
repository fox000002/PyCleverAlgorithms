#!/usr/bin/env python

"""
"""

template_text = """#!/usr/bin/env python

def main():
    pass

if __name__ == "__main__":
    main()
"""

template_text_test = """#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

class Test%s(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
"""


def generate_template(name):
    import os
    print 'Generate Template for ', name

    file_path = './' + name + '.py'

    if os.path.exists(file_path):
        return

    fout = open(file_path, 'w')
    print >>fout, template_text
    fout.close()


def generate_template_test(name):
    import os
    if not os.path.exists('tests'):
        os.makedirs('tests')

    file_path = './tests/' + name + '_test.py'

    if os.path.exists(file_path):
        return

    print 'Generate Template Test for ', name
    fout = open(file_path, 'w')
    print >>fout, template_text_test % name
    fout.close()


def main():
    import sys
    import getopt
    argv = sys.argv[1:]
    names = []
    gen_test = False
    try:
        opts, args = getopt.getopt(argv, "htn:", ["name="])
    except getopt.GetoptError:
        print 'bare.py [-t] -n <name>'
        sys.exit(-2)
    for opt, arg in opts:
        if opt == '-h':
            print 'bare.py [-t] -n <name>'
            sys.exit(0)
        elif opt == '-t':
            gen_test = True
        elif opt in ("-n", "--name"):
            names.append(arg)

    print 'Names :', names
    for name in names:
        generate_template(name)
        if gen_test:
            generate_template_test(name)


if __name__ == "__main__":
    main()
