# -*- coding: utf-8 -*-

import argparse
import csv
import glob
import logging
from lxml import etree
import multiprocessing as mp
import os
from time import process_time
from typing import List, Tuple
import zipfile


logger = mp.log_to_stderr()
logger.setLevel(logging.DEBUG)



def process_xml(xml_string: str) -> Tuple:
    """ Finds required info in xml file, assuming xml is correct """
    root = etree.fromstring(xml_string)
    id = root.xpath("//var[@name='id']/@value")[0]
    level = root.xpath("//var[@name='level']/@value")[0]
    objects_names = root.xpath("//objects/object/@name")
    return id, level, objects_names


def process_files(path: str) -> List[Tuple]:
    """ Multicore process dispatcher """
    res: List[Tuple] = []
    with mp.Pool(processes=mp.cpu_count())as pool:
        for file in sorted(glob.glob(os.path.join(path, '*.zip'))):
            logger.debug('Processing %s', file)
            with zipfile.ZipFile(file, 'r') as f:
                contents = f.namelist()
                res.append(pool.map(process_xml, (f.open(xml_file).read() for xml_file in contents)))
    return res


def write_data(data: List[Tuple], path: str) -> None:
    """ Writes result files """
    with open(os.path.join(path, 'levels.csv'), 'w') as levels_csv, \
            open(os.path.join(path, 'objects.csv'), 'w') as objects_csv:
        levels_writer = csv.writer(levels_csv)
        objects_writer = csv.writer(objects_csv)
        for id, level, objects in sum(data, []):
            levels_writer.writerow([id, level])
            for object in objects:
                objects_writer.writerow([id, object])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process xml files')
    parser.add_argument("path", action='store_false', help="work directory")
    args = parser.parse_args()

    work_dir = args.path or ''

    result = process_files(work_dir)
    write_data(result, work_dir)

    logger.info('Time elapsed %ss', process_time())
