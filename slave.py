import redis
import json
import foursq_profiles
import foursq_tips
import foursq_friends
import random
import pymongo
import traceback
import time

single_fetch_num = 10 # can be changed 
uids = []

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r_master = redis.Redis(host='144.202.113.150', port=6379, decode_responses=True) # need fulfill master host

total_user = 0
valid_user = 0
users_with_tips = 0
users_w_tips = 0

myclient = pymongo.MongoClient(host='localhost', port=27017) 
mydb = myclient["f4q_crawler"]
mycol = mydb["users"]

def get_json(user_id):
    global users_w_tips
    crawl_tips = {}
    crawl_tips['user info'] = foursq_profiles.fetch_user_profile(user_id)
    if crawl_tips['user info'] != -1:
        crawl_tips['tips'], users_w_tips = foursq_tips.fetch_usr_tips(user_id)
        crawl_tips['friends'] = foursq_friends.fetch_usr_friends(user_id)
    else:
        return -1
    return crawl_tips

def save_error(context):
    with open("error.json",'a') as file:
        file.write(context+'\n')
error_file = open("error.json",'a')

success = []
while True:
    try:
        if uids != []:
            uid = uids.pop(0)
            result = get_json(uid)
            if result != -1:
                x = mycol.insert_one(result)
                success.append(uid)
                print(uid, 'done')
            else:
                save_error(uid)
            time.sleep(1)
        else:
            if success != []:
                r_master.srem("set2", *success) 
            success = [] 
            select = r_master.srandmember("set2", 10)
            if len(list(select)) != 0:  
                uids = uids + list(select)
            else:
                time.sleep(10)
    except Exception:
        error_file.write("%s -> %s\n" %(uid, traceback.format_exc()))
        time.sleep(10)










