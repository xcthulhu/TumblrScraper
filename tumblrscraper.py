#!/usr/bin/env python

import tumblpy
import sqlite3
import ts_model
import sys

def tumblr_scraper(base_url,db_name,num_images,start_offset=0,limit=20,url_type='blog'):
    #init with some key
    t = tumblpy.Tumblpy(app_key = 'V55FKUe1lMSdx0UyGSFknmO8DoSaeNzT9oByUwOE1Hvp7diQJ7',
                        app_secret = 'TD9eTgRhoo8ceu0cjcF0nROWAAMkst1uAkSx5XuSOjnYxrGq50',
                        callback_url = 'whatever.com/notimportant_now')

    #we don't need this code
    auth_props = t.get_authentication_tokens()
    auth_url = auth_props['auth_url']
    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']

    #running
    #get db connection
    print "Connecting to %s" % db_name
    conn = ts_model.touch_db(db_name)
    c = conn.cursor()
    #scraping...
    print "Scraping %s" % base_url
    n = 0
    i = 0
    while n < num_images :
        #get the posts
        print "Get posts %i to %i" % (i*limit+start_offset,(1+i)*limit+start_offset)
        if url_type == 'blog':
           posts = t.get('posts',blog_url=base_url,params={'limit':limit, 'offset':i*limit+start_offset})
        i += 1
        for p in posts['posts']:
          #some posts don't have photo
          if(not('photos' in  p)): continue
          #some posts have more than one image, we will ignore that for now
          if(len(p['photos']) != 1): continue
          #some posts don't have tag
          if(len(p['tags']) == 0): continue
          # If we made it through that, we have a new photo
          n += 1
          #print out the info, move to DB later
          note_count = p['note_count']
          tags = [ y.strip().lower() for x in p['tags']
                                     for y in x.split('\n') ]
          url = p['photos'][0]['original_size']['url']
          #if this is slow, switch to batch execute instead
          print "Found %s %i: %s %s" % (sys.argv[1],n,url,"#" + " #".join(tags))
          ts_model.add_tags(c, tags)
          ts_model.add_photo(c, url, note_count)
          ts_model.link_tags_photo(c, tags, url)
          conn.commit()
    conn.close()

if __name__ == "__main__" : 
    #subject to cmd input
    base_url='http://%s.tumblr.com' % sys.argv[1]
    db_name = '%s.db' % sys.argv[1]
    num_images = int(sys.argv[2])
    if len(sys.argv) >= 4:
       start_offset = int(sys.argv[3])
    else :
       start_offset = 0
    tumblr_scraper(base_url,db_name,num_images,start_offset=start_offset,limit=20)
