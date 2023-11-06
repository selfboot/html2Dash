#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import sqlite3
import subprocess
import shutil

from bs4 import BeautifulSoup


def update_db(name, path):
    try:
        cur.execute("SELECT rowid FROM searchIndex WHERE path = ?", (path,))
        dbpath = cur.fetchone()
        cur.execute("SELECT rowid FROM searchIndex WHERE name = ?", (name,))
        dbname = cur.fetchone()

        if dbpath is None and dbname is None:
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path)\
                    VALUES (?,?,?)', (name, "Section", path))
        else:
            pass
    except:
        pass


def add_urls():
    index_page = open(os.path.join(docset_path, 'index.html'), encoding="utf-8").read()
    soup = BeautifulSoup(index_page, "html.parser")
    any = re.compile('.*')
    for tag in soup.find_all('a', {'href': any}):
        name = tag.text.strip()
        if len(name) > 0:
            path = tag.attrs['href'].strip()
            if path.split('#')[0] not in ('index.html'):
                update_db(name, path)


def add_infoplist(info_path, index_page):
    name = docset_name.split('.')[0]
    info = """
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
            <key>CFBundleIdentifier</key>
            <string>{0}</string>
            <key>CFBundleName</key>
            <string>{1}</string>
            <key>DashDocSetFamily</key>
            <string>{2}</string>
            <key>DocSetPlatformFamily</key>
            <string>requests</string>
            <key>isDashDocset</key>
            <true/>
            <key>isJavaScriptEnabled</key>
            <true/>
            <key>dashIndexFilePath</key>
            <string>{3}</string>
    </dict>
    </plist>
    """.format(name, name, name, index_page)

    try:
        open(info_path, 'w', encoding="utf-8").write(info)
        print("Create the Info.plist File")
    except Exception as  e:
        print("**Error**:  Create the Info.plist File Failed...")
        print(e)
        clear_trash()
        exit(2)


def clear_trash():
    try:
        shutil.rmtree(docset_name)
        # subprocess.call(["rm", "-r", docset_name])
        print("Clear generated useless files!")
    except:
        print("**Error**:  Clear trash failed...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--name',
                        help='Name the docset explicitly')
    parser.add_argument('-d', '--destination',
                        dest='path',
                        default='',
                        help='Put the resulting docset into PATH')
    parser.add_argument('-i', '--icon',
                        dest='filename',
                        help='Add PNG icon FILENAME to docset')
    parser.add_argument('-p', '--index-page',
                        help='Set the file that is shown')
    parser.add_argument('SOURCE',
                        help='Directory containing the HTML documents')

    results = parser.parse_args()

    source_dir = results.SOURCE
    if source_dir[-1] == "/":
        source_dir = results.SOURCE[:-1]

    if not os.path.exists(source_dir):
        print(source_dir + " does not exsit!")
        exit(2)

    dir_name = os.path.basename(source_dir)
    if not results.name:
        docset_name = dir_name + ".docset"
    else:
        docset_name = results.name + ".docset"

    # create docset directory and copy files
    doc_path = docset_name + "/Contents/Resources/Documents"
    dsidx_path = docset_name + "/Contents/Resources/docSet.dsidx"
    icon = docset_name + "/icon.png"
    info = docset_name + "/Contents/info.plist"

    destpath = results.path
    if results.path and results.path[-1] != "/":
        destpath += "/"
    docset_path = destpath + doc_path
    sqlite_path = destpath + dsidx_path
    info_path = destpath + info
    icon_path = destpath + icon

    # printdocset_path, sqlite_path

    if not os.path.exists(docset_path):
        os.makedirs(docset_path)
        print( "Create the Docset Folder!")
    else:
        print("Docset Folder already exist!")

    # Copy the HTML Documentation to the Docset Folder
    for subdir in os.listdir(source_dir):
        try:
            shutil.copytree(os.path.join(source_dir, subdir), os.path.join(docset_path, subdir))
        except NotADirectoryError as not_dir:
            try:
                shutil.copy(os.path.join(source_dir, subdir), os.path.join(docset_path, subdir))
            except:
                clear_trash()
                raise "**Error**:  Copy Html Documents Failed..." from not_dir

    # create and connect to SQLite
    try:
        db = sqlite3.connect(sqlite_path)
        cur = db.cursor()
    except:
        print("**Error**:  Create SQLite Index Failed...")
        clear_trash()
        exit(2)

    try:
        cur.execute('DROP TABLE searchIndex;')
    except:
        pass

    cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY,\
                name TEXT,\
                type TEXT,\
                path TEXT);')
    cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')
    print("Create the SQLite Index")

    add_urls()
    db.commit()
    db.close()

    # Create the Info.plist File
    if not results.index_page:
        index_page = "index.html"
    else:
        index_page = results.index_page

    add_infoplist(info_path, index_page)

    # Add icon file if defined
    icon_filename = results.filename
    if icon_filename:
        if icon_filename[-4:] == ".png" and os.path.isfile(icon_filename):
            try:
                subprocess.call(["cp", icon_filename, icon_path])
                print("Create the Icon for the Docset!")
            except:
                print("**Error**:  Copy Icon file failed...")
                clear_trash()
                exit(2)
        else:
            print( "**Error**:  Icon file should be a valid PNG image...")
            clear_trash()
            exit(2)
    else:
        pass

    print("Generate Docset Successfully!")
