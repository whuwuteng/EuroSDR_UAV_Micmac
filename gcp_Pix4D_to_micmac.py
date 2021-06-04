import sys
import os

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom.minidom import Document
from lxml import etree

import numpy as np
import argparse

import pdb

XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'

def LoadPix4d(gcp_file) :
    gcplist = []
    gcps= []
    image = []
    last_image = ''
    infile = open(gcp_file,'r')
    for line in infile:
        info = line.strip()
        gcp = info.split(',')
        #pdb.set_trace()
        if gcp[0] == last_image :
            gcps.append(info)
        else:
            if last_image :
                gcplist.append(gcps)

            gcps= []
            gcps.append(info)

            last_image = gcp[0]
            image.append(gcp[0])

    if last_image :
        gcplist.append(gcps)
    infile.close()

    return image, gcplist

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='show Micmac file(gcp 2D xlm)')

    parser.add_argument("--xml", type=str, default='', help='Micmac xml')
    parser.add_argument("--txt", type=str, default='', help='Pix4D txt')
    parser.add_argument("--ext", type=str, default='.jpg', help='image extension format')

    args = parser.parse_args()

    doc = Document()
    doc_root = doc.createElement('SetOfMesureAppuisFlottants')
    doc.appendChild(doc_root)

    image, gcplist = LoadPix4d(args.txt)
    
    img_num = len(image)
    gcp_num = len(gcplist)
    #pdb.set_trace()

    for i in range(0, img_num) :
        if image[i].find('_163') >= 0 :
            item_root = doc.createElement('MesureAppuiFlottant1Im')

            title = doc.createElement('NameIm')
            title_text = doc.createTextNode(image[i] + args.ext)
            title.appendChild(title_text)
            item_root.appendChild(title)

            for gcp_item in gcplist[i] :
                gcp = gcp_item.split(',')
                object_item = doc.createElement('OneMesureAF1I')

                title = doc.createElement('NamePt')
                title_text = doc.createTextNode(gcp[1])
                title.appendChild(title_text)
                object_item.appendChild(title)

                title = doc.createElement('PtIm')
                title_text = doc.createTextNode(gcp[2] + ' ' + gcp[3])
                title.appendChild(title_text)
                object_item.appendChild(title)
                item_root.appendChild(object_item)
            
            doc_root.appendChild(item_root)

    file_xml = open(args.xml,'w')
    file_xml.write(doc.toprettyxml(indent = '\t'))
    file_xml.close()
