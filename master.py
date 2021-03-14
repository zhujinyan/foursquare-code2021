import redis
import json
import foursq_profiles
import foursq_tips
import foursq_friends
import random
import pymongo
import time
import traceback


r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
r.sadd("set1",1234) # can be changed
error_file = open("error.json",'a')

while True:
    try:
        uid = r.spop("set1")
        friendsUID = foursq_friends.fetch_usr_friends_uid(uid)
        if friendsUID != -1:
            if friendsUID != []:
                r.sadd("set1", *friendsUID)
            print('set1 OK')
            r.sadd("set2", uid)
            print(uid, 'bfs done')
            time.sleep(1)
        else:
            r.sadd("set1", uid)
            print(uid, 'went wrong')
            time.sleep(10)
    except Exception:
        error_file.write("%s -> %s\n" %(uid, traceback.format_exc()))
        time.sleep(10)
