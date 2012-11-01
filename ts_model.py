#!/usr/bin/env python

from os.path import exists as file_exists
import sqlite3

def touch_db(filename) :
    if not file_exists(filename):
        #create the database
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS tags
                  (tag_id integer primary key autoincrement, tag text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS photos
                  (photo_id integer primary key autoincrement, note_count integer, url text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS photo_tags
                  (tag_id integer, photo_id integer)''')
        conn.commit()
        return conn
    else:
        return sqlite3.connect(filename)
        
def add_tags(c, tags, verbose=None):
    ids = [];
    new_tags = [];
    latest_id = c.execute('SELECT tag_id FROM tags ORDER BY tag_id DESC LIMIT 1').fetchone()
    if latest_id is None:
        latest_id = 0
    else:
        latest_id = latest_id[0];
    for tag in tags:
        t = (tag,)
        record = c.execute('SELECT * FROM tags WHERE tag=?', t).fetchone()
        if record is None:
            #add the tag
            new_tags.append(t)
            if verbose : 
               print "Inserting %s in tags database" % tag
            latest_id += 1
            ids.append(latest_id)
        else:
            #get the id
            ids.append(record[0])
    #execute insert if any
    if len(new_tags) != 0 :
        c.executemany('INSERT INTO tags (tag) VALUES (?)', new_tags)
    return ids

def add_photo(c, url, note_count, verbose=None):
    data = (url, note_count,)
    latest_id = c.execute('SELECT photo_id FROM photos ORDER BY photo_id DESC LIMIT 1').fetchone()
    if latest_id is None:
        latest_id = 0
    else:
        latest_id = latest_id[0]
    if verbose : 
        print "New Photo -",
        print "Count : %s URL : %s" % (note_count, url)
    c.execute('INSERT INTO photos (url, note_count) VALUES(?,?)', data)
    return latest_id + 1

def link_tags_photo(c, tag_ids, photo_id, verbose=None):
    data = []
    for tag_id in tag_ids:
        data.append((tag_id, photo_id))
        if verbose : 
            print "Linking tag %s to photo %i" % (tag_id,photo_id)
    c.executemany('INSERT INTO photo_tags (tag_id, photo_id) VALUES (?,?)', data)
