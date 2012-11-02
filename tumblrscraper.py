#!/usr/bin/env python

import tumblpy
import sqlite3
import ts_model

if __name__ == "__main__" : 
    #init with some key
    t = tumblpy.Tumblpy(app_key = 'V55FKUe1lMSdx0UyGSFknmO8DoSaeNzT9oByUwOE1Hvp7diQJ7',
                        app_secret = 'TD9eTgRhoo8ceu0cjcF0nROWAAMkst1uAkSx5XuSOjnYxrGq50',
                        callback_url = 'whatever.com/notimportant_now')

    #we don't need this code
    auth_props = t.get_authentication_tokens()
    auth_url = auth_props['auth_url']
    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']

    #ok, here is the thing

    #subject to cmd input
    blog_url='http://deviantart.tumblr.com'
    num_images = 40
    start_offet = 0;

    #running
    num_iterations = num_images / 20
    #get db connection
    conn = ts_model.touch_db('tumblr_photos.db')
    c = conn.cursor()
    #scraping...
    for i in range(num_iterations):
        #get the posts
        posts = t.get('posts',blog_url=blog_url,params={'limit':20, 'offset':(i*num_iterations)+start_offet})
        for p in posts['posts']:
          #some posts don't have photo
          if(not('photos' in  p)): continue
          #some posts have more than one image, we will ignore that for now
          if(len(p['photos']) != 1): continue
          #some posts don't have tag
          if(len(p['tags']) == 0): continue
          #print out the info, move to DB later
          note_count = p['note_count']
          tags = [ y.strip().lower() for x in p['tags']
                                     for y in x.split('\n') ]
          url = p['photos'][0]['original_size']['url']
          #if this is slow, switch to batch execute instead
          ts_model.add_tags(c, tags)
          ts_model.add_photo(c, url, note_count)
          ts_model.link_tags_photo(c, tags, url, verbose=True)
          conn.commit()
    conn.close()
