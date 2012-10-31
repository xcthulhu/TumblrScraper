#!/usr/bin/env python

import sqlite3

def file_exists(filename):
    try:
        with open(filename) as f:
            return True
    except IOError:
        return False

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
        
def add_tags(c, tags):
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
            new_tags.append((tag ,));
            latest_id = latest_id + 1
            ids.append(latest_id)
        else:
            #get the id
            ids.append(record[0])
    #execute insert if any
    if len(new_tags) != 0 :
        c.executemany('INSERT INTO tags (tag) VALUES (?)', new_tags)
    return ids

def add_photo(c, url,note):
    data = (url, note,);
    latest_id = c.execute('SELECT photo_id FROM photos ORDER BY photo_id DESC LIMIT 1').fetchone()
    if latest_id is None:
        latest_id = 0
    else:
        latest_id = latest_id[0];
    c.execute('INSERT INTO photos (url, note_count) VALUES(?,?)', data);
    return latest_id + 1

def link_tags_photo(c, tag_ids, photo_id):
    data = [];
    for tag_id in tag_ids:
        data.append((tag_id, photo_id));
    c.executemany('INSERT INTO photo_tags (tag_id, photo_id) VALUES (?,?)', data)