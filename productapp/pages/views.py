
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
import json
import collections
from pytz import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# Create index funnction pass in the request
dbName = 'devices.db'


def getProducts(ids):
    products = []

    sql = "SELECT id, project_name, description, sku, odm, chipset_vendor, cpu, class, bands, dfs, usb, power_current,  \
			   radio1_freq, radio1_protocol, radio1_mimo, radio1_bw, radio2_freq, radio2_protocol, radio2_mimo, radio2_bw,\
               radio3_freq, radio3_protocol, radio3_mimo, radio3_bw, compare1, compare2, compare3, compare4 , notes   \
               FROM products "
    if ids != "all":
        sql = sql + " where id in (" + ids + ")"
    
    sql = sql + " order by project_name;"

    try: 
        connect = sqlite3.connect(dbName)
        cursor = connect.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        
        productList = []
        for row in rows:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['project_name'] = row[1]
            d['description'] = row[2]
            d['sku'] = row[3]
            d['odm'] = row[4]
            d['chipset_vendor'] = row[5]
            d['cpu'] = row[6]
            d['class'] = row[7]
            d['bands'] = row[8]
            d['dfs'] = row[9]
            d['usb'] = row[10]
            d['power_current'] = row[11]
            d['radio1_freq'] = row[12]
            d['radio1_protocol'] = row[13]
            d['radio1_mimo'] = row[14]
            d['radio1_bw'] = row[15]  
            d['radio2_freq'] = row[16]
            d['radio2_protocol'] = row[17]
            d['radio2_mimo'] = row[18]
            d['radio2_bw'] = row[19]    
            d['radio3_freq'] = row[20]
            d['radio3_protocol'] = row[21]
            d['radio3_mimo'] = row[22]
            d['radio3_bw'] = row[23]      
            d['compare1'] = row[24]    
            d['compare2'] = row[25]
            d['compare3'] = row[26]
            d['compare4'] = row[27]
            d['notes'] = row[28]                       
            productList.append(d)

    except sqlite3.Error as error:
        print("ERROR :", error)
    finally:
        if connect:
            connect.close()   
    return productList

def insertProduct(Sku, Vendor, ProductName, Description,Class, Band):
    result = 1
    try:
        connect = sqlite3.connect(dbName)
        cursor = connect.cursor()

        sql= """INSERT INTO products
                    ( sku,chipset_vendor,  project_name, description, class, bands) VALUES (?, ?, ?, ?, ?, ?);"""

        data = (Sku, Vendor, ProductName, Description,Class, Band)
        cursor.execute(sql, data)
        connect.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("ERROR :", error)
        result = 0
    finally:
        if connect:
           connect.close()
    return result

def removeProduct(id):
    result = 1
    try:
        connect = sqlite3.connect(dbName)
        cursor = connect.cursor()

        sql= query = """DELETE from products where id = ?"""
        cursor.execute(sql, (id,))
        connect.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("ERROR :", error)
        result = 0
    finally:
        if connect:
           connect.close()
    return result



def home(request):
    return render(request, 'pages/home.html')

def product(request):
     return render(request, 'pages/product.html')

def page2(request):
    return render(request, 'pages/page2.html')

def getProduct(request):
    ids =  request.GET['productIds']  
    productList = getProducts(ids)
    #print("listOfProduct = ", productList)
    return JsonResponse({'data': productList})

def getSelectedProduct(request):
    ids =  request.GET['productIds']  
    print("IDs= ", ids)
    productList = getProducts(ids)
    return JsonResponse({'data': productList})

def addProduct(request):
    Sku = request.GET['Sku']  
    Vendor = request.GET['Vendor']  
    ProductName = request.GET['ProductName']  
    Description = request.GET['Description']  
    Class = request.GET['Class']  
    Band = request.GET['Band']  
    if Sku  == "" :
         return JsonResponse({'data': 'Failed to add Product - Empty Sku'}) 
    result = insertProduct(Sku, Vendor, ProductName, Description,Class, Band)  
    if result  == 1 :
         return JsonResponse({'data': 'Success'}) 
   
    return JsonResponse({'data': 'Failed to add Product'}) 

def deleteProduct(request):
    id =  request.GET['productId']  
    print("Delete ProductID :", id)
    result = removeProduct(id)  
    return JsonResponse({'data': result})    