#from scipy.stats import bernoulli
import sys
sys.path

import json
import ast
import time
import random
import db as d
from datetime import datetime
import rethinkdb as r
from main import product as product
from main import customer as customer
from main import plot as plot
r.connect('localhost', 28015).repl()

db_name='finalv'

# r.db_create(db_name).run()
# d.table_create(db_name,'inventory')
# d.table_create(db_name,'revenue')
# d.table_create(db_name,'price')
# d.table_create(db_name,'bids')
# d.table_create(db_name,'product')
# d.table_create(db_name,'customer')
# d.table_create(db_name,'plot')



def compute():

    for x in xrange(20):

        p=product()
        a=['silver','gold','platinum']
        bids=random.randrange(0,20)
        c=customer(random.choice(a),bids)


        pmd=random.randrange(0,25)
        sales=random.randrange(500,2000)
        q=plot(sales,pmd)

        p.inventory.cur=random.randrange(random.randrange(1+(x%20),10+(x%20),2),random.randrange(22+(x%20),500+(x%20),7), random.randrange(1,3,1))

        p.inventory.maxi=random.randrange(random.randrange(1+(x%20),10+(x%20),2),random.randrange(22+(x%20),500+(x%20),7), random.randrange(1,3,1))

        p.revenue.dp=random.normalvariate(random.randrange(500+(x%20),1550+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))

        p.revenue.cp=random.normalvariate(random.randrange(500+(x%20),1550+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))

        p.price.cost=random.normalvariate(random.randrange(500+(x%20),1550+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))

        #p.price.selling=random.normalvariate(random.randrange(600+(x%20),1650+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))

        p.inventory.t0=p.inventory.cur
        #Inserting into the db
        print d.insert(db_name,'inventory',p.inventory.to_JSON())
        print d.insert(db_name,'revenue',p.revenue.to_JSON())
        print d.insert(db_name,'price',p.price.to_JSON())
        print d.insert(db_name,'bids',p.bids.to_JSON())
        print d.insert(db_name,'product',p.to_JSON())
        print d.insert(db_name,'customer',c.to_JSON())
        print d.insert(db_name,'plot',q.to_JSON())
        print d.insert(db_name,'customer',c.to_JSON())

        # print d.update_with_date_random(db_name,'revenue',p.revenue.to_JSON(),p.id-1)
        # print d.update_with_date_random(db_name,'price',p.price.to_JSON(),p.id-1)
        # print d.update_with_date_random(db_name,'bids',p.bids.to_JSON(),p.id-1)
        # print d.update_with_date_random(db_name,'product',p.to_JSON(),p.id-1)


    return
compute()




