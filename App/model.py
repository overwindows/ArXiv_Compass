# coding:utf-8

import web

db = web.database(dbn='mysql', port=3307, host='127.0.0.1', db='ontime_meal', user='root', pw='mysql_sesame')

chinese_weekday = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期日'
}

def get_menu_dates(_date):
    return db.query('SELECT distinct sche_date FROM schedule WHERE sche_date >= $_date ORDER BY sche_date ASC limit 6 ', vars=locals())

def get_districts():
    return db.select('districts')

def get_zones():
    return db.select('zones')

def get_plazas():
    return db.select('plazas')

# 配合12.1首单营销策略[2015/11/28]
def get_user_orders_cnt(uid, date):
    return db.query(
        'SELECT count(*) as cnt FROM orders WHERE orders.orderdate>=$date AND orders.uid=$uid AND orders.status<>2',
        vars=locals())

def get_chinese_weekday(i):
    return chinese_weekday[i]

def get_offices():
    return db.select('offices')

def get_offices_ex():
    return db.query('select offices.officeid as officeid, offices.Name as officename, offices.Address as officeaddr, \
    plazas.name as plazaname, plazas.address as plazaaddr, offices.ID as ID, offices.plazaid as plazaid, offices.zoneid as zoneid \
    from offices left join plazas on offices.plazaid=plazas.id order by plazaname,officename')

def get_office(office_id):
    return db.select('offices', where='officeid=$office_id', vars=locals())


# 按路线，日期获取套餐列表
def get_menu(route_id, date):
    return db.query('select lunches.ID as ID, lunches.Restaurant as Restaurant, lunches.Meal as Meal, lunches.entree as entree,\
                     lunches.Price as Price, lunches.discount as Discount, lunches.price_0 as price_0, lunches.desc,\
                     schedule.stock as Stock, schedule.sold as Sold, lunches.type as Type, lunches.staple, lunches.garnish  \
                     from schedule,lunches \
                     where schedule.meal_id=lunches.ID AND schedule.sche_date=$date \
                     AND schedule.routeid=$route_id \
	             ORDER BY lunches.type, lunches.style, Restaurant ASC', vars=locals())


def get_lunch(lunch_id):
    return db.select('lunches', where='ID=$lunch_id', vars=locals())


def new_user(telephone, uname, opid, contact, offid, unitaddr, regtm):
    return db.insert('users', id=telephone, contactname=contact, username=uname, officeid=offid,  unitaddress=unitaddr, tel=telephone, openid=opid, regtime=regtm)


# 更新订餐联系人
def update_username(uid, name, offid, unitaddr, telephone):
    return db.update('users', where='id=$uid', contactname=name, officeid=offid, unitaddress=unitaddr, tel=telephone, vars=locals())


def get_user(userid, password):
    return db.select('users', where='id=$userid AND password=$password', vars=locals())


# weixin openid -> user
def get_user_1(open_id):
    return db.select('users', where='openid=$open_id', order="regtime DESC", vars=locals())


def new_pass(uid, pswd):
    # print uid,pswd
    return db.update('users', where='id=$uid', password=pswd, vars=locals())


# duplicate user check
def reg_dup_check(uid):
    return db.query('select id from users where users.id=$uid', vars=locals())


def new_order(orderid, telephone, person, office, order_date, all_price, _price0, _price1, _price2, all_cnt, modtime,
              order_tm, user_id, \
              _invoice, _address, _tminterval):
    db.insert('orders', tel=telephone, id=orderid, contact=person, officeid=office, status=0, \
              orderdate=order_date, price=all_price, cnt=all_cnt, modifytime=modtime, price0=_price0, price1=_price1,
              price2=_price2, \
              ordertm=order_tm, uid=user_id, invoice=_invoice, address=_address, tminterval=_tminterval)


def update_order(orderid, stat, modtime):
    return db.update('orders', where='id=$orderid', status=stat, modifytime=modtime, vars=locals())


def update_order_1(orderid, pay_stat):
    return db.update('orders', where='id=$orderid', pay=pay_stat, vars=locals())


def del_order(orderid):
    return db.delete('orders', where='id = $orderid', vars=locals())


def ongoing_orders_cnt(uid):
    return db.query('SELECT id FROM orders WHERE status=0 AND uid=$uid', vars=locals())


# 获取订单详情
def get_order(orderid):
    return db.query('Select orders.tel as Tel, orders.contact as Contact, offices.Name as OfficeName, offices.Address as OfficeAddress, \
    orders.orderdate as OrderDate, orders.price as Price, offices.place as OfficePlace, orders.pay, offices.arrivaltime, orders.price, \
    orders.price0, orders.price1, orders.price2,orders.modifytime, orders.tminterval, orders.address as orderaddr, orders.invoice \
	From orders,offices \
    Where orders.id=$orderid And orders.officeid=offices.officeid', vars=locals())


def get_orders(uid, stat):
    #   return db.select('orders',where = 'tel=$uid AND status=$stat',vars=locals())
    return db.query('SELECT orders.id as id, orders.tel as tel, orders.contact as contact, orders.orderdate as orderdate,\
                   orders.cnt as cnt, orders.price as price, offices.Name as officename, offices.Address as officeaddress,\
                   orders.modifytime as ModTime, orders.pay, orders.dispatch, orders.status,\
                   orders.tminterval, orders.address\
                   FROM orders, offices \
                   WHERE orders.uid=$uid AND orders.status=$stat AND orders.officeid=offices.officeid \
                   ORDER BY id DESC', \
                    vars=locals())


def new_detail(orderid, lunchid, cnt):
    return db.insert('details', orderid=orderid, lunchid=lunchid, num=cnt)


# 库存更新:1.更新库存量;2.更新已售出量
def upd_meal_sold(mealid, schedate, num):
    t = db.transaction()
    try:
        res_iter = db.query('SELECT stock FROM schedule WHERE meal_id=$mealid AND sche_date=$schedate', vars=locals())
        res = list(res_iter)
        # print '库存:'+str(res[0].stock)
        # print '购买:'+str(num)
        if int(res[0].stock) >= int(num):
            db.query('update schedule set stock=stock-$num WHERE meal_id=$mealid and sche_date=$schedate',
                     vars=locals())
            db.query('update schedule set sold=sold+$num WHERE meal_id=$mealid and sche_date=$schedate', vars=locals())
        else:
            return -1
    except:
        t.rollback()
        raise
    else:
        t.commit()
    return 0


# 获取套餐排期详情
def get_meal_detail(mealid, schedate):
    return db.select('schedule', where='meal_id=$mealid and sche_date=$schedate', vars=locals())


def get_detail(oid):
    return db.query('Select lunches.Meal as Name, lunches.Price as Price, details.num as Num, lunches.ID\
    From details, lunches \
    Where details.orderid=$oid And details.lunchid=lunches.ID', vars=locals())


# 获取订单详情
def get_details(oid):
    return db.select('details', where='orderid=$oid', vars=locals())


def del_detail(oid):
    return db.delete('details', where='orderid=$oid', vars=locals())


def get_plaza(_officeid):
    return db.query('SELECT plaza.* FROM plaza,offices \
    WHERE plazas.id=offices.plazaid AND offices.ID=$_officeid', vars=locals())


def get_plazas():
    return db.select('plazas')

def get_details_1(oid):
    return db.query('SELECT details.num,lunches.*\
    FROM details,lunches \
    WHERE details.orderid=$oid AND details.lunchid=lunches.ID',vars=locals())
