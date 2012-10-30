#!/usr/bin/env python

import tumblpy
import MySQLdb

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

#running...
num_iterations = num_images / 20
for i in range(num_iterations):
    #get the posts
    posts = t.get('posts',blog_url=blog_url,params={'limit':20, 'offset':(i*num_iterations)+start_offet})
    for j in range(len(posts['posts'])):
        #some posts don't have photo
        if(not('photos' in  posts['posts'][j])):
            continue
        #some posts have more than one image, we will ignore that for now
        if(len(posts['posts'][j]['photos']) != 1):
            continue
        #some posts don't have tag
        if(len(posts['posts'][j]['tags']) == 0):
            continue
        #print out the info, move to DB later
        print posts['posts'][j]['note_count']
        print posts['posts'][j]['tags']
        print posts['posts'][j]['photos'][0]['original_size']['url']