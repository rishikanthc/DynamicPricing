#from scipy.stats import bernoulli
from numpy.random import binomial
from numpy.random import multinomial
import db as d
import json
import ast
import time
from datetime import datetime
import rethinkdb as r
import numpy

final_list=[]
prft_id=0
db_name='finalv'

def to_JSON(object):
        return json.dumps(object, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)


class customer:
    id=1
    def __init__(self,type,bids):
        self.type=type
        self.bids=bids
        self.id=customer.id
        customer.id+=1

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)

class plot:
    def __init__(self,sales,pmd):
        self.sales=sales
        self.pmd=pmd
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)


class bids:
    # cur
    # tot
    #total=0

    'Common base class for all bids'
    def __init__ (self,cur=None,tot=None,id=None):
        if(tot==None):
            self.copy_constructor(cur)
        else:
            self.non_copy_constructor(cur,tot,id)
        return


    def non_copy_constructor(self,cur,tot,id):
        self.cur = cur
        self.tot = tot
        self.id=id
        self.created_at=0
        self.updated_at=0
        return

    def copy_constructor(self, obj):
        self.cur = obj.cur
        self.tot = obj.tot
        self.id=obj.id
        self.created_at=obj.created_at
        self.updated_at=obj.updated_at
        return

    def displayCurrent(self):
        print "Current number of bids %d" % self.cur
        return

    def displayTotBids(self):
        print "Total number of allowed bids %d" % self.tot
        return

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)


class choice:
    'For bidding'

    def __init__ (self,id):
        #zerro_array=[0,0,0,0,0]
        self.id=id
        self.prev_choice=0
        self.probability=[0,0,0,0,0] #numpy.zeros(5)
        self.propensity=[0,0,0,0,0] #numpy.zeros(5)
        self.seller_profit=[0,0,0,0,0] #numpy.zeros(5)

class inventory:
    # cur
    # maxi
    # t0
    #total=0

    'Common base class for all inventory'

    def __init__(self, cur=None, maxi=None, t0=None, id=None):
        if maxi==None :
            self.constructor_obj(cur)
        else :
            self.constructor_copy(cur, maxi,t0,id)


    def constructor_copy(self, cur, maxi,t0,id):
        self.id=id
        self.cur = cur
        self.maxi = maxi
        self.t0 = t0
        self.created_at=0
        self.updated_at=0

    def constructor_obj(self, obj):
        self.id = obj.id # dynamic pricing
        self.cur = obj.cur # classical pricing
        self.maxi=obj.maxi
        self.t0=obj.t0
        self.created_at=obj.created_at
        self.updated_at=obj.updated_at

    def displayCurrent(self):
        print "Current inventory %d" % self.cur

    def displayMax(self):
        print "Maximum inventory %d" % self.maxi

    def displayt0(self):
        print "Inventory at t0 %d" % self.t0

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)




class revenue:
    # dp
    # cp
   # total=0


    'Common base class for all revenue'

    def __init__(self, dp=None, cp=None, id=None):
        if cp==None:
            self.constructor_obj(obj)
        else:
            self.constructor_copy(dp,cp,id)


    def constructor_copy(self, dp, cp,id): # cp= classical pricing
        self.dp = dp # dynamic pricing
        self.cp = cp # classical pricing
        self.id=id
        self.created_at=0
        self.updated_at=0

    def constructor_obj(self, obj):
        self.dp = obj.dp # dynamic pricing
        self.cp = obj.cp # classical pricing
        self.id=obj.id
        self.created_at=obj.created_at
        self.updated_at=obj.updated_at


    def displayCurrent(self):
        print "Revenue generated from dynamic pricing strategy %d" % self.dp

    def display(self):
        print "Revenue generated from dynamic pricing strategy %d" % self.dp

    def displayMax(self):
        print "Revenue generated from classic pricing strategy %d" % self.cp

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)

    def getTime(self):
        time = r.epoch_time((self.updated_at['epoch_time'])).run()
        return time


class price:
    # cost
    # bid_min
    # bid_max
    # selling


    'Common base class for all price'



    def __init__(self, cost=None, bid_min=None,bid_max=None,selling=None,id=None):
        if(bid_min==None):
            self.copy_constructor(cost)
        else:
            self.non_copy_constructor(cost,bid_min,bid_max,selling,id)
        return

    def non_copy_constructor(self,cost,bid_min,bid_max,selling,id):
        self.cost = cost
        self.bid_min = bid_min
        self.bid_max = bid_max
        self.created_at=0
        self.updated_at=0
        self.selling = selling
        self.id=id

    def copy_constructor(self, obj):
        print 'copy_constructor_price_start'
        self.cost = obj.cost
        self.bid_min = obj.bid_min
        self.bid_max = obj.bid_max
        self.selling = obj.selling
        self.id=obj.id
        self.created_at=obj.created_at # time product was added to the retail store
        self.updated_at=obj.updated_at # time it was sold
        print 'copy_constructor_price_end'


    def displayCostprice(self):
        print "Cost Price %d" % self.cost

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
         sort_keys=True, indent=4)


class product:
    id=1

    'Common base class for all bids'

    def __init__(self,obj=None):
        if(obj==None):
            self.non_copy_constructor()
        else:
            self.copy_constructor(obj)

    def non_copy_constructor(self):
        self.inventory=inventory(0,0,0,product.id)
        self.revenue=revenue(0,0,product.id)
        self.price=price(0,0,0,0,product.id)
        self.bids=bids(0,0,product.id)
        self.choice=choice(product.id)
        self.created_at=0
        self.updated_at=0
        self.decision=0
        self.number_items_dp=0
        self.name='Product ' + str(product.id)
        self.id =  product.id
        product.id += 1


    def copy_constructor(self,obj):
        self.inventory=inventory(obj.inventory)
        self.revenue=revenue(obj.revenue.dp,obj.revenue.cp,obj.id)
        self.price=price(obj.price.cost,obj.price.bid_min,obj.price.bid_max,obj.price.selling,obj.id)
        self.bids=bids(obj.bids.cur,obj.bids.tot,obj.id)
        self.choice=choice(obj.id)
        self.created_at=obj.created_at
        self.updated_at=r.now()
        self.decision=obj.decision
        self.number_items_dp=obj.number_items_dp
        self.name=obj.name

    def copy_constructor2(self,obj):
        self.inventory=inventory(obj.inventory['cur'],obj.inventory['maxi'],obj.inventory['t0'],obj.id)
        self.revenue=revenue(obj.revenue['dp'],obj.revenue['cp'],obj.id)
        self.price=price(obj.price['cost'],obj.price['bid_min'],obj.price['bid_max'],obj.price['selling'],obj.id)
        self.bids=bids(obj.bids['cur'],obj.bids['tot'],obj.id)
        self.choice=choice(obj.id)
        self.created_at=obj.created_at
        self.updated_at=r.now()
        self.decision=obj.decision
        self.number_items_dp=obj.number_items_dp


    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)


# DONE ON A PRODUCT BASIS:
def selection(inventory,revenue):
    "Takes in the item and time and checks its corresponding inventory"
    print "Selection called"

    bernoulli_n=1
    if(inventory.cur<inventory.maxi):
        decision=0
        number_items_dp=0

    else:# add item to selection with some probability
        number_items_dp=inventory.cur-inventory.maxi
        # Commpute the probability
        prob=(float)(revenue.dp/(revenue.dp+revenue.cp))

        # make a Bernoulli draw with probability "prob"
        #decision=bernoulli.rvs(prob,loc=0,size=1) # part of scipy
        decision=binomial(bernoulli_n,prob,1)

    it=d.get1(db_name,'product',inventory.id)
    it['number_items_dp']=number_items_dp
    it['decision']=it['decision']
    d.replace1(db_name,'product',it,it['id'])

    return decision


def pricing_range(item,profit_margin):

    print "Pricing range called"
    p=item

    if p['bids']['tot']==0:
        den=1
    else:
        den=p['bids']['tot']
    market_trend = p['price']['cost']*(p['bids']['cur']/den)

    p['price']['bid_min']=p['price']['cost']+market_trend
    p['price']['bid_max']=(1+profit_margin/100)*p['price']['bid_min']

    return

def bidding_compute(item, buyer_offer,customer_loyalty,buyer_demand,profit_margin):
# Roth-Erev Reinforcement Learning Algorithm
    print "Bidding called"


    bins=5
    p=item

    print 'Dict total',p['bids']['tot']
    print p['choice']['probability']
    print 'number of dp items', p['number_items_dp']
    print 'buyer demand', buyer_demand


    if p['number_items_dp']==0 or buyer_demand>p['number_items_dp']:
       return 0

    pricing_range(p, profit_margin)
    print 'back here!!'

    # UPDATE BID.TOTAL


    prev_choice=p['choice']['prev_choice']# call to database to obtain the index of the last choice made for this product
    seller_profit=p['choice']['seller_profit']
    probability=p['choice']['probability']
    propensity=p['choice']['propensity']
    print "probability",probability
    print "propensity",propensity
    print "prev choice",prev_choice


    # Model parameters
    sp=100
    ep=0.97
    rp=0.04

    if p['bids']['tot']==0:
        t=0
        print "tot is zero"
    else:
        t=1
        print 'tot is 1'

    p['bids']['tot']+=1
    print 'Printing t',t
    if t==0:
        print "entering "
        for choice in xrange(0,5):
            probability[choice]=(1/float(bins))
            print probability[choice]
            propensity[choice]=(2*sp/bins)

    else:
        prop_sum=0
        print("entering here")
        # UPDATE PROBABILITY AND PROPENSITY FOR THE CHANGES BELOW
        for choice in xrange(0,len(propensity)):
            if prev_choice==choice:
                propensity[choice]=(1-rp)*propensity[choice]+seller_profit[choice]*(1-ep)
            else:
                propensity[choice]=(1-rp)*propensity[choice]+(propensity[choice]*ep)/(bins-1)
            prop_sum=prop_sum+propensity[choice]
        for choice in xrange(0,len(probability)):
            # Normalize
            probability[choice]=propensity[choice]/prop_sum

    #DB UPDATE

    p['choice']['probability']=probability
    p['choice']['propensity']=propensity
    print "prob",probability
    print "prop",propensity


    # Probabilistically select a multinomial random variable [1:K] with probability vector. Final choice is the random variable minus 1 (array starts with 0 index)
    #a=[]
    a=multinomial(1, probability, size=1) # np = numpy
    #choice_index=a.index(1)

    for x in xrange(0,5):
        if(a[0][x]==1):
            choice_index=x
            break


    p['choice']['prev_choice']=choice_index
    # UPDATE PREV_CHOICE WITH THE ABOVE CHOICE_INDEX FOR FUTURE
    print "choice index", choice_index
    seller_offer=p['price']['bid_min']+((p['price']['bid_max']-p['price']['bid_min'])/(bins-1))*choice_index


    # Factoring in inventory

    alpha_control = 0.4# SET some value between (0,1)
    inventory_term=alpha_control*((p['inventory']['cur']-p['inventory']['maxi'])/p['inventory']['t0'])

    seller_offer=seller_offer-inventory_term

    # Factoring in loyalty
    if customer_loyalty==1:
        # new customer
        loyalty=0.05*p['price']['cost']
    elif customer_loyalty==2:
        # old customer
        loyalty=0.1*p['price']['cost']
    else:
        loyalty=0

    seller_offer=seller_offer-loyalty

    if seller_offer<=buyer_offer:
        offer_accept=1 # items sold
        seller_profit[choice_index]=(buyer_offer-p['price']['cost'])*buyer_demand # UPDATE DB WITH NEW SELLER PROFIT
        p['inventory']['cur']=p['inventory']['cur']-buyer_demand
        p['number_items_dp']=p['number_items_dp']-buyer_demand
        p['bids']['cur']=p['bids']['cur']+1
        p['revenue']['dp']=p['revenue']['dp']+buyer_offer*buyer_demand
        p['price']['selling']=buyer_offer

    else:
        offer_accept=0

    p['choice']['seller_profit']=seller_profit

    d.replace1(db_name,'product',p,p['id'])

    return offer_accept # binary value



def input_profit_margin(profit_margin):
    prft_id = prft_id+1
    print d.insert_profit_margin(db_name,'profit_margin',prft_id,profit_margin)
    return



def initial_dp_list():
    arr=[]


    for i in xrange(1,20):
        rev=type('revenue', (object,), json.loads(d.get(db_name,'revenue',i)))
        inv=type('inventory', (object,), json.loads(d.get(db_name,'inventory',i)))
        decision=selection(inv,rev)

        if(decision==1):
            arr.append(rev.id)
    print arr
    ar=[]
    for i in xrange(0,len(arr)):
        y=[]
        q=type('product', (object,), json.loads(d.get(db_name,'product',arr[i])))
        y.append(q.id)
        y.append(str(q.name))
        y.append(q.number_items_dp)
        y.append(q.inventory['maxi'])
        ar.append(y)
    print ar
    return ar

def final_dp_list(arr):
    final_list=arr
    for i in arr:
        r.db('db_name').table("product").get(i).update({"decision": 1}).run()
    return



def real_time_data():
    final_list=[19]
    data=[]
    for i in xrange(0,len(final_list)):
        x=[]
        q=type('product', (object,), json.loads(d.get(db_name,'product',final_list[i])))
        x.append(q.id)
        x.append(str(q.name))
        x.append(q.bids['tot'])
        x.append(q.bids['cur'])
        x.append(int (q.revenue['dp']))
        data.append(x)
    print data
    return

def bidding(item, buyer_offer,customer_loyalty,buyer_demand,profit_margin):
    it=d.get1(db_name,'product',item)
    bidding_compute(it,buyer_offer,customer_loyalty,buyer_demand,profit_margin)
    return

def test():
    initial_dp_list()
    bidding(17,4057,0,2,15)
    bidding(17,570,0,2,15)
    real_time_data()
    return

#test()

#SEQUENCE OF OPERATIONS:

# 1) Call to DB for revenue and profit margin decisions by frontend
# 2) Update profit_margin value
# 3) Call to initial_dp_list() by frontend, call selection for each item, return list of items to final_dp_list(<arr>) and update DB
# 4) For those items available for DP:  Receive consumer loyalty, bid offer,  product and quantity demanded
# 5) Each customer submits 2 bids sequentially, bidding(item) called and 0/1 decision returned





