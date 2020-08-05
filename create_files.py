# -*- coding: utf-8 -*-

import argparse
from lxml import etree
import os
from random import randint
import uuid
import zipfile

ZIP_NUMBER = 50
XML_NUMBER = 100


def create_files() -> None:
    """ Sample files creator """
    for n in range(ZIP_NUMBER):
        with zipfile.ZipFile(os.path.join(BASEPATH, '{:02d}.zip'.format(n+1)), 'w', zipfile.ZIP_DEFLATED) as f:
            for m in range(XML_NUMBER):
                root = etree.Element('root')
                etree.SubElement(root, 'var', name='id', value=str(uuid.uuid4()))
                etree.SubElement(root, 'var', name='level', value=str(randint(1, 100)))
                objects = etree.SubElement(root, 'objects')
                for _ in range(randint(1,10)):
                    etree.SubElement(objects, 'object', name=str(uuid.uuid4()))

                tree = etree.ElementTree(root)
                f.writestr('{:03d}.xml'.format(m+1), etree.tostring(tree, pretty_print=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create xml files')
    parser.add_argument("path", action='store_false', help="work directory")
    args = parser.parse_args()

    BASEPATH = args.path or ''

    create_files()
