#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def my_sort_key(url):
  match1 = re.search(r'[\w]+.jpg', url)
  if match1:
      sort_base = match1.group()
      sort_base = sort_base[0:len(sort_base)-4]

  return sort_base

def my_sort(img_urls):
  """ check the first name
  if the suffix does not matche a pattern of -wordchars-wordchars.jpg then use the regular sort
  otherwise implement a new sort and return a custom sorted list """

  match = re.search(r'-[\w]+-+[\w]+.jpg', img_urls[0])
  if match:
      print "match"
      img_urls = sorted(img_urls, key=my_sort_key)

  else:
      print "no match"
      img_urls.sort()

  return img_urls


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""

    with open(filename, "r") as logfile:
        # prefix = "http://code.google.com"
        # building the prefix based on the file name
        k = logfile.name.rfind("_") + 1
        prefix = "http://" + logfile.name[k:] + ".com"

        # list of URLs
        lurls = []

        # loop through file
        for line in logfile:
            tmpurl = prefix
            # check if line has a puzzle substring
            match = re.search(r'puzzle/', line)
            if match:
                # copy the puzzle string and add prefix
                tmpurl += line[line.index('GET ') + 4:line.index(' HTTP/1.0')]

                # check if in list
                inlist = False
                for url in lurls:
                    if tmpurl == url:
                        inlist = True
                        break

                # if not in list then add to list
                if not inlist:
                    lurls.append(tmpurl)
    # sort the list
    # lurls.sort()

    return my_sort(lurls)

    # return lurls

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
    #get current working directory
    os_path = os.getcwd()

    # check if destination dir is defined
    if dest_dir:
        # join the destination folder to the cwd
        os_path = os.path.join(os_path, dest_dir)

        # check if destination dir exists
        if not os.path.exists(os_path):
        # if not then create the dir
            os.mkdir(os_path)

    #define the HTML file name
    htmlname = os.path.join(os.getcwd(), "index.html")

    #open the file for writing
    f = open(htmlname, 'w')
    #write the HTML prefix into the file
    f.write("<verbatim>")
    f.write("<html>")
    f.write("<body>")

    # loop through the list and save images
    i = 0
    for url in img_urls:
        img_name = "img" + str(i) + ".jpg"
        urllib.urlretrieve(url, os.path.join(os_path, img_name))
        f.write("<img src=\"./imgs/" + img_name + "\">")
        i += 1

    #write the HTML suffix into the file
    f.write("</body>")
    f.write("</html>")
    #close the file
    f.close()

def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)

if __name__ == '__main__':
    main()
