
import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom.minidom import Document

import numpy as np
import argparse

import pdb

XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'

def LoadGCP(gcp_file) :
    gcps= []
    infile = open(gcp_file,'r')
    for line in infile:
        gcps.append(line.strip())

    infile.close()
    return gcps

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate Micmac file from gcp')

    parser.add_argument("--gcp", type=str, default='', help='point list')
    parser.add_argument("--xml", type=str, default='', help='xml')

    args = parser.parse_args()

    gcps = LoadGCP(args.gcp)

    gcp_x = []
    gcp_y = []
    gcp_z = []
    for gcp_item in gcps :
        gcp = gcp_item.split(',')
        gcp_x.append(float(gcp[1]))
        gcp_y.append(float(gcp[2]))
        gcp_z.append(float(gcp[3]))

    print('min x: ' + str(min(gcp_x)))
    print('max x: ' + str(max(gcp_x)))
    print('min y: ' + str(min(gcp_y)))
    print('max y: ' + str(max(gcp_y)))
    print('min z: ' + str(min(gcp_z)))
    print('max z: ' + str(max(gcp_z)))

    if args.xml :
        doc = Document()
        doc_root = doc.createElement('DicoAppuisFlottant')
        doc.appendChild(doc_root)

        for gcp_item in gcps :

            gcp = gcp_item.split(',')
            item_root = doc.createElement('OneAppuisDAF')
            
            title = doc.createElement('Pt')
            title_text = doc.createTextNode(gcp[1] + ' ' + gcp[2] + ' ' + gcp[3])
            title.appendChild(title_text)
            item_root.appendChild(title)

            title = doc.createElement('NamePt')
            title_text = doc.createTextNode(gcp[0])
            title.appendChild(title_text)
            item_root.appendChild(title)

            title = doc.createElement('Incertitude')
            title_text = doc.createTextNode('1 1 1')
            title.appendChild(title_text)
            item_root.appendChild(title)
                
            doc_root.appendChild(item_root)

        file_xml = open(args.xml,'w')
        file_xml.write(doc.toprettyxml(indent = '\t'))
        file_xml.close()