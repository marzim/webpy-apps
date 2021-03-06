#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     11/12/2013
# Copyright:   (c) mc185104 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import web, datetime

db = web.database(dbn='mysql', db='marzim83$blog', user='marzim83', pw='mustard_180', host='mysql.server')

def get_posts(id):
    try:
        return db.select('entries', where='userid='+ str(id), order='id DESC')
    except IndexError:
        return None

def get_post(id,uid):
    try:
        return db.select('entries', where='id=$id and userid='+ str(uid), vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text, userid):
    db.insert('entries', title=title, content=text, posted_on=datetime.datetime.utcnow(), userid=userid)

def del_post(id):
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('entries', where="id=$id", vars=locals(), title=title, content=text)

def get_users():
    return db.select('users', order='id DESC')

def get_user(user):
    try:
        return db.select('users', where='user=$user', vars=locals())[0]
    except IndexError:
        return None

def new_user(user, pwd, email):
    db.insert('users', user=user, pwd=pwd, email=email)

def del_user(user):
    db.delete('users', where="user=$user", vars=locals())

def update_user(user, pwd, email):
    db.update('users', where="user=$user", vars=locals(), pwd=pwd, email=email)

