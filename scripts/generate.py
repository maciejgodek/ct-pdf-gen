#!/usr/bin/env python3
import sys
import os
from parse.ccel_parse import *
from parse.na_parse import *

filepath = sys.argv[1]

with open(filepath) as f:
    lines = f.readlines()
    title = lines[0].rstrip()
    sections = lines[1].rstrip()
    author = lines[2].rstrip()

    i = 3
    sites = []
    while i < len(lines):
        if "http://" in lines[i]:
            url = lines[i].rstrip()
            selected_headers = []
            i += 1
            while i < len(lines) and "http://" not in lines[i]:
                selected_headers.append(lines[i].rstrip())
                i += 1
            sites.append((url, selected_headers))
    filename = os.path.basename(filepath)

    if "ccel" in filename:
        print(generate_from_ccel_sites(title, sections, author, sites))
    elif "nadv" in filename:
        print(generate_from_nadv_sites(title, sections, author, sites))
        
