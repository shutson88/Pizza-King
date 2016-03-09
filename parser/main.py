__author__ = 'Seth'
from Customer import Customer
from Server import Server
from Store import Store
from Order import Order
from Pizza import Pizza
import os
import json
import datetime, time
from xml.dom import minidom
import sqlite3


stores = []
orders = []
pizza = ""
for filename in os.listdir("PizzaGeneratorSampleData"):
    file = open("PizzaGeneratorSampleData/"+filename)
    if(file.name.__contains__("json")):
        data = json.load(file)

        for o in data["orders"]:

            pizzas = []

            for p in o["pizzas"]:
                pizzas.append(Pizza(p["name"]))


            bday_epoch = o["orderPlacer"]["birthday"]/1000
            bdday_ts = datetime.datetime.fromtimestamp(bday_epoch).strftime('%Y-%m-%d %H:%M:%S')

            cust_address = str(o["orderPlacer"]["address"]["houseNumber"]) + " " + o["orderPlacer"]["address"]["street"] + " " +  o["orderPlacer"]["address"]["city"] + ", " + o["orderPlacer"]["address"]["state"]
            customer = Customer(o["orderPlacer"]["name"], o["orderPlacer"]["surname"], cust_address, o["orderPlacer"]["age"], o["orderPlacer"]["female"], bdday_ts)

            serv_epoch = o["server"]["birthday"]/1000
            serv_ts = datetime.datetime.fromtimestamp(serv_epoch).strftime('%Y-%m-%d %H:%M:%S')

            server_address = str(o["server"]["address"]["houseNumber"]) + " " + o["server"]["address"]["street"] + " " +  o["server"]["address"]["city"] + ", " + o["server"]["address"]["state"]
            server = Server(o["server"]["name"], o["server"]["surname"], server_address, o["server"]["age"], o["server"]["female"], serv_ts)

            # date = o["date"] - time.time()

            ts_epoch = o["date"]/1000
            ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')

            order = Order(o["orderNumber"], customer, data["name"], server, ts, pizzas)

            orders.append(order)

    if(file.name.__contains__("xml")):
        xmldoc = minidom.parse(file)
        orderlist = xmldoc.getElementsByTagName('order')

        for order in orderlist:
            # customer = Customer(order.attributes['name'])
            id = orderlist[0].attributes['number'].value
            # print(id)
            name = order.getElementsByTagName('name')[0].firstChild.data
            name = str(name).replace('\n', '')
            date = order.getElementsByTagName('date')[0].firstChild.data
            date = str(date).replace('\n', '')

            addr_num = order.getElementsByTagName('number')[0].firstChild.data
            addr_st = order.getElementsByTagName('street')[0].firstChild.data
            addr_city = order.getElementsByTagName('city')[0].firstChild.data
            addr_state = order.getElementsByTagName('state')[0].firstChild.data

            address = addr_num + " " + addr_st + " " + addr_city + ", " + addr_state
            address = str(address).replace('\n', '')

            customer = Customer(name, '', address, '', '', '')

            server = order.getElementsByTagName('server')[0].firstChild.data
            server = str(server).replace('\n', '').replace('Person [name=', '').replace(' surname=', '').replace(' age=', '').replace(' birthday=', '').replace('female=', '').replace(']', '')
            server = server.split(',')
            server  = Server(server[0], server[1], '', server[2], server[4], server[3])
            pizzas = order.getElementsByTagName('pizza')
            pizzaArray = []
            for p in pizzas:
                # print(len(pizzas))
                pizzaArray.append(Pizza(str(p.childNodes[0].nodeValue).replace('\n', '')))
            order = Order(id, customer, 'Hoang\'s Pizzeria', server, date, pizzaArray)
            orders.append(order)




conn = sqlite3.connect('../db2.sqlite3')
c = conn.cursor()
id = 0
# print(pizza)
# print(orders[0].pizzas[0].name)
# Insert a row of data
# c.execute("INSERT INTO homepage_pizza VALUES ('1', \'dummy\','',0, '')")
for o in orders:

     # try:
    address = str(o.customer.address).replace(',', '').split(' ')
    print("Storing " + str(address))
    address = filter(lambda a: a != '', address)
    c.execute("INSERT INTO Pizza_King_Customer VALUES ("+str(id)+", \'"+o.customer.surname+"\',\'"+o.customer.name+"\',\'"+address[0]+"\', \'"+address[1]+"\', \'"+address[2]+"\', \'"+address[3]+"\')")
    id += 1
     # except:
     #     print (p.name + " Exists")
# for o in orders:
#     for p in o.pizzas:
#          try:
#             c.execute("INSERT INTO Pizza_King_Customer VALUES ("+str(id)+", \'"+p.name+"\','','', '')")
#             id += 1
#          except:
#              print (p.name + " Exists")
        # pizza_table = c.execute('SELECT name FROM homepage_pizza')


conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
print("done.")


