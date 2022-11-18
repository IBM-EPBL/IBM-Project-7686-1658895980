import re
import ibm_db
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

hostname = 'ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
uid = 'cfp74886'
pwd = 'QwlbzISB5dRZ5jjj'
driver = "{IBM DB2 ODBC DRIVER}"
db_name = 'bludb'
port = '31505'
protocol = 'TCPIP'
cert = "C:/Users/Tamil/Desktop/IBM/TEST/certi.crt"

dsn = (
    "DATABASE ={0};"
    "HOSTNAME ={1};"
    "PORT ={2};"
    "UID ={3};"
    "SECURITY=SSL;"
    "PROTOCOL={4};"
    "PWD ={6};"
).format(db_name, hostname, port, uid, protocol, cert, pwd)
connection = ibm_db.connect(dsn, "", "")
print()
# query = "SELECT username FROM users WHERE username=?"
# stmt = ibm_db.prepare(connection, query)
# ibm_db.bind_param(stmt, 1, username)
# ibm_db.execute(stmt)
# username = ibm_db.fetch_assoc(stmt)
# print(username)
app.secret_key = 'a'



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = " "
    if request.method == 'POST':
        username = request.form['uname']
        email_id = request.form['email']
        phone_no = request.form['phone_no']
        password = request.form['pass']
        query = "SELECT * FROM users WHERE username=?;"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if (account):

            msg = "Account already exists!"
            return render_template('register.html', msg=msg)
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
        #     msg = "Invalid email addres"
        # elif not re.match(r'[A-Za-z0-9+', username):
        #     msg = "Name must contain only characters and numbers"
        else:
            query = "INSERT INTO users values(?,?,?,?)"
            stmt = ibm_db.prepare(connection, query)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, email_id)
            ibm_db.bind_param(stmt, 3, phone_no)
            ibm_db.bind_param(stmt, 4, password)
            ibm_db.execute(stmt)
            msg = 'You have successfully Logged In!!'
            return render_template('login.html', msg=msg)
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('register.html', msg=msg)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ' '
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['pass']
        query = "select * from users where username=? and password=?"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in Successfully'
            return redirect(url_for("dashboard"))
        else:
            msg = 'Incorrect Username or Password'
            return render_template('login.html', msg=msg)
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('login.html', msg=msg)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form['uname']
        print(username)
        return render_template('welcome.html', username=username)
    else:
        return render_template('welcome.html', username=username)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    msg = " "
    if request.method == 'POST':
        pid = request.form['pid']
        pname = request.form['pname']
        rate = request.form['rate']
        quantity = request.form['quantity']
        brand = request.form['brand']
        category = request.form['category']
        img = request.form['img']

        query = "SELECT * FROM INVENTORYITEMS WHERE productID=?;"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, int(pid))
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if (account):
            msg = "Product ID already exists!"
            #------------------
        else:
            query = "INSERT INTO INVENTORYITEMS values(?,?,?,?,?,?,?)"
            stmt = ibm_db.prepare(connection, query)
            ibm_db.bind_param(stmt, 1, int(pid))
            ibm_db.bind_param(stmt, 2, pname)
            ibm_db.bind_param(stmt, 3, float(rate))
            ibm_db.bind_param(stmt, 4, int(quantity))
            ibm_db.bind_param(stmt, 5, brand)
            ibm_db.bind_param(stmt, 6, category)
            q = int(quantity)

            if(q > 0):
                ibm_db.bind_param(stmt, 7, True)
            else:
                ibm_db.bind_param(stmt, 7, False)
                
            ibm_db.execute(stmt)
            msg = 'You have successfully Added!'
            items = GetInventoryItems()
            return render_template('product.html',items=items, msg=msg )
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        items = GetInventoryItems()
        return render_template('product.html', items=items)



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    items = GetInventoryItems()
    items.reverse()
    pcount = len(items)
    orderlist = GetOrderList()
    orderlist.reverse()
    ocount = len(orderlist)
    return render_template('dashboard.html', items=items, pcount=pcount,orderlist=orderlist,ocount=ocount)

@app.route('/order', methods=['GET', 'POST'])
def order():
     msg = " "
     if request.method == 'POST':
        oid = request.form['oid']
        cname = request.form['cname']
        cno = request.form['cno']
        odate = request.form['odate']
        pname = request.form['pname']
        nitems = request.form['items']
        discount = request.form['discount']
        status = request.form['status']
        data = GetProductAmount(pname)
        amount = abs(((float(discount) / 100) * float(data['RATE'])) - float(data['RATE']))

        query = "INSERT INTO Orders values(?,?,?,?,?,?,?,?,?)"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, oid)
        ibm_db.bind_param(stmt, 2, odate)
        ibm_db.bind_param(stmt, 3, cname)
        ibm_db.bind_param(stmt, 4, cno)
        ibm_db.bind_param(stmt, 5, pname)
        ibm_db.bind_param(stmt, 6, nitems)
        ibm_db.bind_param(stmt, 7, discount)
        ibm_db.bind_param(stmt, 8, amount)
        ibm_db.bind_param(stmt, 9, status)
                
        ibm_db.execute(stmt)
        msg = 'You have successfully Added!'
        items = GetOrderList()
        data = GetProductName()
        return render_template('order.html',items=items, data=data)
     else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        items = GetOrderList()
        data = GetProductName()
        return render_template('order.html',items=items, data=data)

@app.route('/index')
def index():
    return render_template('index.html')

def GetInventoryItems():
    itemsdata = [] 
    query = "SELECT * FROM INVENTORYITEMS"
    stmt = ibm_db.prepare(connection, query)
    ibm_db.execute(stmt)
    items = ibm_db.fetch_assoc(stmt)
    i = 0
    while items != False:
        
        itemsdata.append(items)
        items = ibm_db.fetch_assoc(stmt)
        i = i+1
    return itemsdata

def GetOrderList():
    itemsdata = [] 
    query = "SELECT * FROM Orders"
    stmt = ibm_db.prepare(connection, query)
    ibm_db.execute(stmt)
    items = ibm_db.fetch_assoc(stmt)
    i = 0
    while items != False:    
        itemsdata.append(items)
        items = ibm_db.fetch_assoc(stmt)
        i = i+1
    
    return itemsdata

def GetProductAmount(pname):
    query = "select * from INVENTORYITEMS WHERE productName=?"
    stmt = ibm_db.prepare(connection, query)
    ibm_db.bind_param(stmt, 1, pname)
    ibm_db.execute(stmt)
    return ibm_db.fetch_assoc(stmt)

def GetProductName():

    query = "SELECT productName FROM INVENTORYITEMS;"
    stmt = ibm_db.prepare(connection, query)
    ibm_db.execute(stmt)
    return ibm_db.fetch_tuple(stmt)

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0')