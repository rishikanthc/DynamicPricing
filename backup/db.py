import rethinkdb as r
import ast
import time
import json
from datetime import datetime
import random
db_name='final_testing'





conn=r.connect('localhost', 28015).repl()

#r.db_create(db_name).run()

def table_create(db_name,tbl_name):
	r.db(db_name).table_create(tbl_name,primary_key='id').run()
	return r.db(db_name).table(tbl_name)

def table_return(db_name,tbl_name):
	return r.db(db_name).table(tbl_name)

# table_create(db_name,'inventory')
# table_create(db_name,'revenue')
# table_create(db_name,'price')
# table_create(db_name,'bids')
# table_create(db_name,'product')
# table_create(db_name,'customer')
# table_create(db_name,'plot')



def insert(db_name,tbl_name,obj):
	if (r.db(db_name).table_list().contains(tbl_name).run()):
		t=table_return(db_name,tbl_name)
	else:
		t=table_create(db_name,tbl_name)

	return t.insert(ast.literal_eval(obj)).run()

def insert_profit_margin(db_name,tbl_name,id,profit_margin):

	if (r.db(db_name).table_list().contains(tbl_name).run()):
		t=table_return(db_name,tbl_name)
	else:
		t=table_create(db_name,tbl_name)

	return t.insert({id: id, profit_margin: profit_margin}).run()




def replace(db_name,tbl_name,obj,key):
	#print r.db(db_name).table_list().contains(tbl_name).run()
	if (r.db(db_name).table_list().contains(tbl_name).run()):
		t=table_return(db_name,tbl_name)
	else:
		t=table_create(db_name,tbl_name)

	return t.get(key).replace(ast.literal_eval(obj)).run()

#deleting an entry with primary key
def delete(db_name,tbl_name,obj,key):
	#print r.db(db_name).table_list().contains(tbl_name).run()
	if (r.db(db_name).table_list().contains(tbl_name).run()):
		t=table_return(db_name,tbl_name)
	else:
		t=table_create(db_name,tbl_name)

	return t.get(key).replace(None).run()

#Get single document
def get(db_name,tbl_name,key):
	return r.db(db_name).table(tbl_name).get(key).coerce_to('string').run(conn)

def getProd(db_name,tbl_name,key):
	return r.db(db_name).table(tbl_name).get(key).coerce_to('string').run()

#Get all the documents
def getAll(db_name,tbl_name):
	return r.db(db_name).table(tbl_name).orderBy('id').run()


def getTime(db_name,tbl_name,key):
	#return r.db(db_name).table(tbl_name).get(key).run()
	return r.db(db_name).table(tbl_name).get(key).run()

def update_with_date(db_name,tbl_name, user_object,id):
    return r.db(db_name).table(tbl_name).get(id).replace(
        lambda doc: r.branch(
            (doc == None),
            doc.merge(doc).merge({'updated_at': r.now()}),
            doc.merge(doc).merge({'updated_at': r.now()}))).run()

def update_with_date_random(db_name,tbl_name, user_object,id):
    return r.db(db_name).table(tbl_name).get(id).replace(
        lambda doc: r.branch(
            (doc == None),
            doc.merge(doc).merge({'created_at': r.time(random.randrange(1995,2015,1), random.randrange(1,12,1), random.randrange(1,30,1), 'Z')}),
            doc.merge(doc).merge({'created_at': r.time(random.randrange(1995,2015,1), random.randrange(1,12,1), random.randrange(1,30,1), 'Z')},{'updated_at': r.now()}))).run()

