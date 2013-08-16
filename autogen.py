#!/usr/bin/python
import argparse
import json
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('name', help='Base name of html file to generate. name.md must exist.')
args = parser.parse_args()
name = args.name

with open(name + '.md', 'r') as md_file, \
     open(name + '.html', 'w') as html_file, \
     open('header', 'r') as header_file, \
     open('footer', 'r') as footer_file:

  data = {"text": md_file.read(), "mode": "gfm"}

  p = subprocess.Popen(['curl', '-s', '--data-binary', '@-', 'https://api.github.com/markdown'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate(json.dumps(data))

  if p.returncode != 0:
    print 'Error calling curl: ' + err, sys.stderr

  html_file.write(header_file.read())
  html_file.write(out)
  html_file.write(footer_file.read())
