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

def LoadGCP(gcp_file) :
    gcps= []
    infile = open(gcp_file,'r')
    for line in infile:
        gcps.append(line.strip())

    infile.close()
    return gcps

def SplitGPC(gcps, num) :
    gcpID = []
    for gcp_item in gcps :
        gcp = gcp_item.split(',')
        gcpID.append(gcp[0])

    random.shuffle(gcpID)

    gcp_control = []
    gcp_check = []

    for i in range(0, num) :
        gcp_control.append(gcpID[i])

    for i in range(num, len(gcpID)) :      
        gcp_check.append(gcpID[i])

    return gcp_control, gcp_check

def LoadFile(gcps, file_list) :
    gcp_control = []
    infile = open(file_list,'r')
    for line in infile:
        gcp_control.append(line.strip())

    infile.close()

    gcp_check = []
    for gcp_item in gcps :
        gcp = gcp_item.split(',')
        if gcp[0] not in gcp_control :
            gcp_check.append(gcp[0])

    return gcp_control, gcp_check

def Write3Dxml(gcps, gcpID, xml_file):
    doc = Document()
    doc_root = doc.createElement('DicoAppuisFlottant')
    doc.appendChild(doc_root)

    for gcp_item in gcps :
        gcp = gcp_item.split(',')

        if gcp[0] in gcpID :
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

    file_xml = open(xml_file,'w')
    file_xml.write(doc.toprettyxml(indent = '\t'))
    file_xml.close()


def Write2Dxml(image, gcplist, gcpID, xml_file) :
    img_num = len(image)
    gcp_num = len(gcplist)

    doc = Document()
    doc_root = doc.createElement('SetOfMesureAppuisFlottants')
    doc.appendChild(doc_root)

    for i in range(0, img_num) :
        # Nadir image
        if image[i].find('_163') >= 0 :
            item_root = doc.createElement('MesureAppuiFlottant1Im')

            title = doc.createElement('NameIm')
            title_text = doc.createTextNode(image[i] + args.ext)
            title.appendChild(title_text)
            item_root.appendChild(title)

            for gcp_item in gcplist[i] :
                gcp = gcp_item.split(',')

                if gcp[1] in gcpID :
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

    file_xml = open(xml_file,'w')
    file_xml.write(doc.toprettyxml(indent = '\t'))
    file_xml.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='split GCP into control points and check points Micmac file(gcp 2D xlm)')

    parser.add_argument("--gcp3d", type=str, default='', help='3D point text')
    parser.add_argument("--gcp2d", type=str, default='', help='Pix4D txt')
    parser.add_argument("--num", type=int, default=0, help='number of points selected')
    parser.add_argument("--list", type=str, default='', help='Pix4D txt')
    parser.add_argument("--ext", type=str, default='.jpg', help='image extension format')
    parser.add_argument("--control3d_xml", type=str, default='', help='output xml')
    parser.add_argument("--control2d_xml", type=str, default='', help='output xml')
    parser.add_argument("--check3d_xml", type=str, default='', help='output xml')
    parser.add_argument("--check2d_xml", type=str, default='', help='output xml')
    args = parser.parse_args()

    gcps = LoadGCP(args.gcp3d)

    # split
    if args.num > 0 :
        gcp_control, gcp_check = SplitGPC(gcps, args.num)
    elif args.list :
        gcp_control, gcp_check = LoadFile(gcps, args.list)
    else :
        print('all is the control ponts')
        gcp_control, gcp_check = SplitGPC(gcps, len(gcps))

    image, gcplist = LoadPix4d(args.gcp2d)    
    
    if args.control3d_xml :
        Write3Dxml(gcps, gcp_control, args.control3d_xml)

    if args.control2d_xml :
        Write2Dxml(image, gcplist, gcp_control, args.control2d_xml)

    if args.check3d_xml :
        Write3Dxml(gcps, gcp_check, args.check3d_xml)

    if args.check2d_xml :
        Write2Dxml(image, gcplist, gcp_check, args.check2d_xml)
