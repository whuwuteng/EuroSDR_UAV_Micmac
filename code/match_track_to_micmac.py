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

def LoadPMul(track_file) :
    infile = open(track_file, 'r')

    # header
    for i in range(5) :
        infile.readline()
    num_line = infile.readline()

    image_num = int(num_line.split(' ')[0])

    image = []
    for i in range(image_num) :
        name_line = infile.readline()
        image.append(name_line.split('=')[0])

    infile.readline()

    gcplist = []
    for i in range(image_num) :
        gcplist.append([])

    config_line = infile.readline()
    config_num = int(config_line.split(' ')[0])

    # letter
    for i in range(8) :
        infile.readline()

    # consider micmac index 
    count = 100000
    for i in range(config_num) :
        num_view_line = infile.readline()
        num = int(num_view_line.split(' ')[0])
        view = int(num_view_line.split(' ')[1])

        index_view_line = infile.readline()
        index_view = []
        for j in range(view) :
            index_view.append(int(index_view_line.split(' ')[j]))

        #print(index_view)
        for j in range(num) :
            view_pt_line = infile.readline()
            view_pt = view_pt_line.split(' ')

            for k in range(view) :
                index = index_view[k]
                gcplist[index].append(str(count) + ',' + view_pt[k*2] + ',' + view_pt[k*2 + 1])
            
            count = count + 1

        # last
        infile.readline()
    print('number of points: ' + str(count - 100000))
    
    return image, gcplist

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='show Micmac file(gcp 2D xlm)')

    parser.add_argument("--xml", type=str, default='', help='Micmac xml')
    parser.add_argument("--txt", type=str, default='', help='track txt')

    args = parser.parse_args()

    doc = Document()
    doc_root = doc.createElement('SetOfMesureAppuisFlottants')
    doc.appendChild(doc_root)

    image, gcplist = LoadPMul(args.txt)

    #print(image)

    img_num = len(image)
    gcp_num = len(gcplist)
    #pdb.set_trace()

    for i in range(0, img_num) :
        item_root = doc.createElement('MesureAppuiFlottant1Im')

        title = doc.createElement('NameIm')
        title_text = doc.createTextNode(image[i])
        title.appendChild(title_text)
        item_root.appendChild(title)

        for gcp_item in gcplist[i] :
            gcp = gcp_item.split(',')
            object_item = doc.createElement('OneMesureAF1I')

            title = doc.createElement('NamePt')
            title_text = doc.createTextNode(gcp[0])
            title.appendChild(title_text)
            object_item.appendChild(title)

            title = doc.createElement('PtIm')
            title_text = doc.createTextNode(gcp[1] + ' ' + gcp[2])
            title.appendChild(title_text)
            object_item.appendChild(title)
            item_root.appendChild(object_item)
        
        doc_root.appendChild(item_root)

    file_xml = open(args.xml,'w')
    file_xml.write(doc.toprettyxml(indent = '\t'))
    file_xml.close()
