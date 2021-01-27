import tkinter
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, Menu
from tkinter.ttk import Progressbar, Style
from time import sleep
from datetime import date, datetime, timedelta
import time
from win32printing import Printer
import tempfile
import os
import threading

conn = sqlite3.connect('GTgas.db')
conn.execute('''CREATE TABLE IF NOT EXISTS administration (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name varchar(22) NOT NULL, 
Phone varchar(11) NOT NULL,Amount INT(10) NOT NULL, Volume INT(10) NOT NULL, CP INT(10) NOT NULL, SP INT(11) NOT NULL, 
DOT DATE NOT NULL)''')
conn.execute('''CREATE TABLE IF NOT EXISTS LOGIN_Admins (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
username varchar(22) NOT NULL,password varchar(20) NOT NULL)''')
conn.execute('''CREATE TABLE IF NOT EXISTS info(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name varchar (20) NOT NULL,
Address varchar(20)NOT NULL,phone varchar(20) NOT NULL)''')
conn.execute(
    ''' CREATE TABLE IF NOT EXISTS LOGIN_Users(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name varchar(20) NOT NULL,password varchar(20) NOT NULL)''')
c = conn.cursor()
conn.commit()
"""
price=c.execute("SELECT SP FROM administration")
for p in price:
    row=p[0]
"""
times = time.asctime(time.localtime())

window = Tk()
window.title("Login Window")
window.geometry("300x300+800+200")
window.resizable(False, False)

var = StringVar()
kg = StringVar()
pri = StringVar()
trans = StringVar()

tabControl = ttk.Notebook(window)  # create Tab Control
admin = ttk.Frame(tabControl)  # create a tab
tabControl.add(admin, text='Admin')  # add the tab
tabControl.pack(expand=1, fill='both')  # pack to make it visible

user = ttk.Frame(tabControl)
tabControl.add(user, text="Sales")
tabControl.pack(expand=1, fill='both')

admin_name = ttk.Label(admin, text="Username")
admin_name.grid(row=0, column=0)
admin_name1 = ttk.Entry(admin)
admin_name1.grid(row=0, column=5, padx=10, pady=10)

admin_password = ttk.Label(admin, text="Password")
admin_password.grid(row=1, column=0)
admin_password1 = ttk.Entry(admin)
admin_password1.grid(row=1, column=5, padx=10, pady=10)
admin_password1.config(show='*')

user_name = ttk.Label(user, text="Username")
user_name.grid(row=0, column=0)
user_name1 = ttk.Entry(user)
user_name1.grid(row=0, column=5, padx=10, pady=10)

user_password = ttk.Label(user, text="Password")
user_password.grid(row=1, column=0)
user_password1 = ttk.Entry(user)
user_password1.grid(row=1, column=5, padx=10, pady=10)
user_password1.config(show='*')


def new_widow1():
    global new_window
    new_window = Toplevel(window)
    new_window.title('Admin Section')
    new_window.resizable(False, False)
    new_window.geometry("1350x700")
    menuBar = Menu(new_window)  # creating menu bar
    new_window.config(menu=menuBar)

    filemenu = Menu(menuBar, tearoff=0)  # Add menu items
    filemenu.add_command(label='Save', command=save_btn)
    filemenu.add_separator()
    filemenu.add_command(label='change admin login', command=update_Pass)
    filemenu.add_separator()
    filemenu.add_command(label='change user login', command=update_pass1)
    filemenu.add_separator()
    filemenu.add_command(label='change info', command=infos)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=close)

    menuBar.add_cascade(label='File', menu=filemenu)

    viewmenu = Menu(menuBar, tearoff=0)
    viewmenu.add_command(label='Supplier', command=view)
    viewmenu.add_separator()
    viewmenu.add_command(label='transactions', command=view_tr)
    viewmenu.add_separator()

    menuBar.add_cascade(label='View', menu=viewmenu)

    editmenu = Menu(menuBar, tearoff=0)

    editmenu.add_command(label='Search', command=search_btn)
    editmenu.add_separator()
    editmenu.add_command(label='Clear Supplier Record', command=clear_Supplier_Record)
    editmenu.add_separator()
    editmenu.add_command(label='Clear sales Record', command=clear_sales_records)
    editmenu.add_separator()
    menuBar.add_cascade(label="Edit", menu=editmenu)

    global supplier_name1
    global amount_naira1
    global volume1
    global cost1
    global phone1
    global sell1
    global val3, val4, val5, val6, val7, val8

    supplier_name = ttk.Label(new_window, text="Supplier Name")
    supplier_name.place(x=0, y=0)
    supplier_name1 = ttk.Entry(new_window)
    supplier_name1.place(x=100, y=0)

    phone = ttk.Label(new_window, text="Phone no")
    phone.place(x=250, y=0)
    phone1 = ttk.Entry(new_window)
    phone1.place(x=350, y=0)

    amount_naira = ttk.Label(new_window, text="Amount(Naira)")
    amount_naira.place(x=500, y=0)
    amount_naira1 = ttk.Entry(new_window)
    amount_naira1.place(x=600, y=0)

    volume = ttk.Label(new_window, text="Litres Purchased")
    volume.place(x=0, y=50)
    volume1 = ttk.Entry(new_window)
    volume1.place(x=100, y=50)

    cost = ttk.Label(new_window, text="Cost price/litre")
    cost.place(x=250, y=50)
    cost1 = ttk.Entry(new_window)
    cost1.place(x=350, y=50)

    sell = ttk.Label(new_window, text="Selling price/litre")
    sell.place(x=500, y=50)
    sell1 = ttk.Entry(new_window)
    sell1.place(x=600, y=50)

    global treeview, treeview1
    frame1 = Frame(new_window, bd=4, relief=RIDGE)
    frame1.place(x=0, y=100, width=870, height=500)
    scroll_x = Scrollbar(frame1, orient=HORIZONTAL)
    scroll_y = Scrollbar(frame1, orient=VERTICAL)
    treeview = ttk.Treeview(frame1, columns=(1, 2, 3, 4, 5, 6, 7, 8), xscrollcommand=scroll_x.set,
                            yscrollcommand=scroll_y.set, show="headings", height="15")
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=treeview.xview)
    scroll_y.config(command=treeview.yview)
    treeview.place(x=0, y=80)

    treeview_label = ttk.Label(frame1, text="SUPPLIER DETAILS")
    treeview_label.place(x=350, y=0)
    treeview.column('1', width=8, anchor='center')
    treeview.column('2', width=110, anchor='center')
    treeview.column('3', width=110, anchor='center')
    treeview.column('4', width=110, anchor='center')
    treeview.column('5', width=150, anchor='center')
    treeview.column('6', width=110, anchor='center')
    treeview.column('7', width=110, anchor='center')
    treeview.column('8', width=130, anchor='center')
    treeview.heading("1", text="ID")
    treeview.heading("2", text="Name")
    treeview.heading("3", text="Phone No")
    treeview.heading("4", text="Amount(Naira)")
    treeview.heading("5", text="Volume(KG)")
    treeview.heading("6", text="Cost Price")
    treeview.heading("7", text="Selling price")
    treeview.heading("8", text="Date")

    frame2 = Frame(new_window, bd=4, relief=RIDGE)
    frame2.place(x=870, y=100, width=400, height=500)
    treeview_label1 = ttk.Label(frame2, text="SALES TRANSACTION")
    treeview_label1.place(x=100, y=0)
    scrollx = Scrollbar(frame2, orient=HORIZONTAL)
    scrolly = Scrollbar(frame2, orient=VERTICAL)
    treeview1 = ttk.Treeview(frame2, columns=(1, 2, 3, 4, 5), show="headings", height="15", xscrollcommand=scrollx.set,
                             yscrollcommand=scrolly.set)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=treeview1.xview)
    scrolly.config(command=treeview1.yview)

    treeview1.place(x=0, y=80)
    treeview1.column('1', width=20, anchor='center')
    treeview1.column('2', width=80, anchor='center')
    treeview1.column('3', width=80, anchor='center')
    treeview1.column('4', width=80, anchor='center')
    treeview1.column('5', width=90, anchor='center')
    treeview1.heading("1", text="ID")
    treeview1.heading("2", text="Price Per liter")
    treeview1.heading("3", text="litres")
    treeview1.heading("4", text="Total amount")
    treeview1.heading("5", text="Date")


def sales_win():
    global saleswin
    saleswin = Toplevel(window)
    saleswin.title("Payment platform")
    saleswin.geometry("800x800")
    saleswin.resizable(0, 0)

    global var, val, amount_per_litre_Entry, kg_Entry, total_Entry, val8, text1, total_sales, localtime1, price_naira_Entry, trans_Entry, del_sales

    amount_per_litre = ttk.Label(saleswin, text="Amount(per liter)")
    amount_per_litre.place(x=5, y=20)
    amount_per_litre_Entry = ttk.Entry(saleswin, textvariable=var)
    amount_per_litre_Entry.place(x=100, y=20)
    amount_per_litre_Entry.configure(state=DISABLED)
    # amount_per_litre_Entry.insert(0,var)

    amount_kg = ttk.Label(saleswin, text="Amount(KG)")
    amount_kg.place(x=5, y=60)
    kg_Entry = ttk.Entry(saleswin, textvariable=kg)
    kg_Entry.place(x=100, y=60)

    price_naira = ttk.Label(saleswin, text="Price")
    price_naira.place(x=10, y=120)
    price_naira_Entry = ttk.Entry(saleswin, textvariable=pri)

    price_naira_Entry.place(x=100, y=120)

    trans_label = ttk.Label(saleswin, text="Roll No")
    trans_label.place(x=5, y=180)
    trans_Entry = ttk.Entry(saleswin, textvariable=trans)
    trans_Entry.place(x=100, y=180)

    pay_button = ttk.Button(saleswin, text='Calculate', command=cal)
    pay_button.place(x=20, y=210)

    view_button = ttk.Button(saleswin, text='Save', command=saves)
    view_button.place(x=105, y=210)

    close_button = ttk.Button(saleswin, text='Print', command=iprint)
    close_button.place(x=200, y=210)

    print_button = ttk.Button(saleswin, text="Clear Boxes", command=clear_tr)
    print_button.place(x=300, y=210)

    close_button = ttk.Button(saleswin, text="Exit", command=close_tr)
    close_button.place(x=400, y=210)

    textbut_clear = ttk.Button(saleswin, text="clear Print", command=clear_print)
    textbut_clear.place(x=300, y=370)

    frame = ttk.LabelFrame(saleswin, text="Document to print")
    frame.place(x=0, y=350, width=305, height=250)

    scrolly = Scrollbar(frame, orient=VERTICAL)
    scrolly.pack(side=RIGHT, fill='y')

    text1 = Text(frame, font=('Courier ', 7, ''), width=55, height=20)
    text1.place(x=0, y=0)

    text1.configure(yscrollcommand=scrolly.set)
    scrolly.config(command=text1.yview)

    del_sales = ttk.Entry(saleswin)
    del_sales.place(x=270, y=10)
    del_salesbut = ttk.Button(saleswin, text="Search", command=sales_search)
    del_salesbut.place(x=400, y=10)
    del_salesbut = ttk.Button(saleswin, text="delete Transaction", command=del_sale)
    del_salesbut.place(x=490, y=10)


def sales_search():
    v2 = del_sales.get()
    sql = "SELECT * FROM Trans WHERE ID LIKE?"
    res = c.execute(sql, (v2,))
    for n in res:
        r1 = n[0]
        r2 = n[2]
        r3 = n[3]
    kg_Entry.insert(END, r2)
    price_naira_Entry.insert(END, r3)
    trans_Entry.insert(END, r1)


def del_sale():
    v1 = del_sales.get()
    sql = "DELETE FROM Trans WHERE ID LIKE?"
    c.execute(sql, (v1,))
    conn.commit()
    messagebox.showinfo("Delete Transaction", "Transaction deleted").format(v1)
    kg_Entry.delete(0, END)
    price_naira_Entry.delete(0, END)
    trans_Entry.delete(0, END)


def clear_print():
    text1.delete('1.0', 'end')


def update_win():
    global updatewin
    updatewin = Toplevel(new_window)
    updatewin.title("Edit your Data")
    updatewin.geometry("800x500")

    global supplier_name1_update, phone1_update, amount_naira1_update
    global volume1_update, cost1_update, sell1_update
    supplier_name_update = ttk.Label(updatewin, text="Supplier name")
    supplier_name_update.grid(row=0, column=0)
    supplier_name1_update = ttk.Entry(updatewin)
    supplier_name1_update.grid(row=0, column=5, padx=10, pady=10)

    phone_update = ttk.Label(updatewin, text="Phone no")
    phone_update.grid(row=1, column=0)
    phone1_update = ttk.Entry(updatewin)
    phone1_update.grid(row=1, column=5, padx=10, pady=10)

    amount_naira_update = ttk.Label(updatewin, text="Amount(Naira)")
    amount_naira_update.grid(row=2, column=0)
    amount_naira1_update = ttk.Entry(updatewin, text="Amount(Naira)")
    amount_naira1_update.grid(row=2, column=5, padx=10, pady=10)

    volume_update = ttk.Label(updatewin, text="Litres")
    volume_update.grid(row=3, column=0)
    volume1_update = ttk.Entry(updatewin)
    volume1_update.grid(row=3, column=5, padx=10, pady=10)

    cost_update = ttk.Label(updatewin, text="Cost price per litre")
    cost_update.grid(row=4, column=0)
    cost1_update = ttk.Entry(updatewin)
    cost1_update.grid(row=4, column=5, padx=10, pady=10)

    sell_update = ttk.Label(updatewin, text="Selling price per litre")
    sell_update.grid(row=5, column=0)
    sell1_update = ttk.Entry(updatewin)
    sell1_update.grid(row=5, column=5, padx=10, pady=10)

    search_but = ttk.Button(updatewin, text="OK", command=search_ok)
    search_but.grid(row=0, column=15, padx=5, pady=5)
    search_but1 = ttk.Button(updatewin, text="Update", command=update_db)
    search_but1.grid(row=0, column=17)
    search_but1 = ttk.Button(updatewin, text="Delete", command=delete)
    search_but1.grid(row=0, column=20)

    global search_ent, search
    search_label = ttk.Label(updatewin, text="Enter phone")
    search_label.grid(row=0, column=10)
    search_ent = ttk.Entry(updatewin)
    search_ent.grid(row=0, column=12)
    search_ent.focus_set()
    search = search_ent.get()
    global treeview


def create_admin():
    val1 = admin_name1.get()
    val2 = admin_password1.get()
    sql = "INSERT INTO 'LOGIN_Admins'(username,password)VALUES(?,?)"
    c.execute(sql, (val1, val2))
    messagebox.showinfo("Admin", "Account created")


def login_account():
    val1 = admin_name1.get()
    val2 = admin_password1.get()
    sql = c.execute("SELECT *FROM LOGIN_Admins")
    sel = sql.fetchall()
    conn.commit()
    row2 = []
    row1 = []
    for x in sel:
        row1 = x[1]
        row2 = x[2]

    if val1 == 'gtgas' and val2 == 'admin':
        new_widow1()
    elif val1 != row1 or val2 != row2:
        messagebox.showerror("Login Error", "Wrong Username or password")
    else:
        pass
        admin_password1.delete(0, END)


def create_admin1():
    val1 = user_name1.get()
    val2 = user_password1.get()
    sql = "INSERT INTO 'LOGIN_Users'(name,password)VALUES('gtgas','admin')"
    c.execute(sql)
    messagebox.showinfo("Admin", "Account created")


# create_admin1()


def login_account1():
    val1 = user_name1.get()
    val2 = user_password1.get()
    row1 = []
    row2 = []
    sql = c.execute("SELECT *FROM LOGIN_Users")
    sel = sql.fetchall()
    conn.commit()
    # global row1, row2
    for x in sel:
        row1 = x[1]
        row2 = x[2]
    if val1 == 'gtgas' and val2 == 'admin':
        refresh()
        sales_win()
    elif val1 != row1 or val2 != row2:
        messagebox.showerror("Login Error", "Wrong Username or password")
    else:
        pass
    user_password1.delete(0, END)


def update_Pass():
    global up, ad_name1, ad_pass1
    up = Toplevel(new_window)
    up.title("Change Login Details")
    up.geometry("300x300")
    ad_name = ttk.Label(up, text="username")
    ad_name.grid(row=0, column=5)
    ad_name1 = ttk.Entry(up)
    ad_name1.grid(row=0, column=10, padx=5, pady=5)

    ad_pass = ttk.Label(up, text="password")
    ad_pass.grid(row=5, column=5)
    ad_pass1 = ttk.Entry(up)
    ad_pass1.grid(row=5, column=10)

    ad_Butt = ttk.Button(up, text="Change", command=up_pass)
    ad_Butt.grid(row=8, column=10)


def update_pass1():
    global up, us_name1, us_pass1
    up = Toplevel(new_window)
    up.title("Change Login Details")
    up.geometry("300x300")
    us_name = ttk.Label(up, text="username")
    us_name.grid(row=0, column=5)
    us_name1 = ttk.Entry(up)
    us_name1.grid(row=0, column=10, padx=5, pady=5)

    us_pass = ttk.Label(up, text="password")
    us_pass.grid(row=5, column=5)
    us_pass1 = ttk.Entry(up)
    us_pass1.grid(row=5, column=10)

    us_Butt = ttk.Button(up, text="Change", command=up_pass1)
    us_Butt.grid(row=8, column=10)


def up_pass():
    v1 = ad_name1.get()
    v2 = ad_pass1.get()
    sql = "UPDATE LOGIN_Admins SET username=?,password=? WHERE ID =2"
    upd = c.execute(sql, (v1, v2))
    conn.commit()
    messagebox.showinfo("Success", "Login Details Changed")


def up_pass1():
    v1 = us_name1.get()
    v2 = us_pass1.get()
    sql = "UPDATE LOGIN_Users SET name=?,password=? WHERE ID =1"
    upd = c.execute(sql, (v1, v2))
    conn.commit()
    messagebox.showinfo("Success", "Login Details Changed")


def validation():
    return val3 == "" or val4 == "" or val5 == "" or val6 == "" or val7 == '' or val8 == ''


def msgs():
    msg1 = messagebox.showinfo("Missing Value", "Enter Supplier Info")


def alert():
    msg = messagebox.askquestion("Save Record", "Are you sure you want to save")


def save_btn():
    l = time.asctime(time.localtime())
    global val3, val4, val5, val6, val7, val8, msg
    val3 = supplier_name1.get()
    val4 = str(phone1.get())
    val5 = (amount_naira1.get())
    val6 = (volume1.get())
    val7 = (cost1.get())
    val8 = sell1.get()
    if validation():
        msgs()
    elif messagebox.askquestion("Save Record", "Are you sure you want to save") == 'yes':
        sql = "INSERT INTO 'administration'(Name,Phone,Amount,Volume,CP,SP,DOT)VALUES(?,?,?,?,?,?,?) "
        c.execute(sql, (val3, str(val4), val5, val6, val7, val8, l))
        messagebox.showinfo("supplier", "Record saved")
        supplier_name1.delete(0, END)
        phone1.delete(0, END)
        amount_naira1.delete(0, END)
        volume1.delete(0, END)
        cost1.delete(0, END)
        sell1.delete(0, END)
        conn.commit()
        refresh()
    elif alert == 'no':
        pass
    else:
        pass


def refresh():
    price = c.execute("SELECT SP FROM administration")
    for p in price:
        row = p[0]
    try:
        var.set(row)
    except:
        pass


def view():
    records = treeview.get_children()
    for elements in records:
        treeview.delete(elements)
    c.execute("SELECT * FROM administration")
    result = c.fetchall()
    for r in result:
        row = r[1]
        row1 = r[2]
        row2 = r[3]
        row3 = r[4]
        row4 = r[5]
        row5 = r[6]
        treeview.insert("", 'end', values=r)


def search_btn():
    update_win()


def search_ok():
    global search
    search = search_ent.get()
    val21 = supplier_name1_update.get()
    val22 = phone1_update.get()
    val23 = amount_naira1_update.get()
    val24 = volume1_update.get()
    val25 = cost1_update.get()
    val26 = sell1_update.get()
    sql = "SELECT * FROM administration WHERE Phone LIKE ?"
    res = c.execute(sql, (search,))
    for r in res:
        row = r[1]
        row1 = r[2]
        row2 = r[3]
        row3 = r[4]
        row4 = r[5]
        row5 = r[6]
        print(row, row1)
        supplier_name1_update.insert(END, row)
        phone1_update.insert(END, row1)
        amount_naira1_update.insert(END, row2)
        volume1_update.insert(END, row3)
        cost1_update.insert(END, row4)
        sell1_update.insert(END, row5)


def update_db():
    val21 = supplier_name1_update.get()
    val22 = phone1_update.get()
    val23 = amount_naira1_update.get()
    val24 = volume1_update.get()
    val25 = cost1_update.get()
    val26 = sell1_update.get()
    if val21 == "" or val22 == "" or val23 == "" or val24 == "" or val25 == '' or val26 == '':
        messagebox.showinfo("Update", "no record updated")
    elif messagebox.askquestion("Update Record", "Do you want to update?") == 'yes':
        sql1 = "UPDATE administration SET Name=?, Phone=?, Amount=?, Volume=?,CP=?,SP=? WHERE Phone LIKE ?"
        c.execute(sql1, (val21, val22, val23, val24, val25, val26, search_ent.get()))
        conn.commit()
        messagebox.showinfo("Update", "Record successfully updated")
        supplier_name1_update.delete(0, END)
        phone1_update.delete(0, END)
        amount_naira1_update.delete(0, END)
        volume1_update.delete(0, END)
        cost1_update.delete(0, END)
        sell1_update.delete(0, END)


def delete():
    if messagebox.askquestion("Delete Record", "Are you sure you want to delete?") == 'yes':
        sql = "DELETE FROM administration WHERE Phone LIKE ?"
        c.execute(sql, (search_ent.get(),))
        conn.commit()
        messagebox.showinfo("ShowInfo", "Record deleted")
        supplier_name1_update.delete(0, END)
        phone1_update.delete(0, END)
        amount_naira1_update.delete(0, END)
        volume1_update.delete(0, END)
        cost1_update.delete(0, END)
        sell1_update.delete(0, END)
    else:
        pass


def deleting():
    try:
        treeview.item(treeview.selection())['values'][0]
    except IndexError as e:
        messagebox.showinfo("Delete Record", "Please select record")
        return
    name = treeview.item(treeview.selection())['text']
    query = "DELETE FROM administration WHERE ID = ?"
    conn.execute(query, (name,))
    messagebox.showinfo("Delete Record", "Record Deleted")
    view()


def updating():
    pass


def clear_sales_records():
    if messagebox.askquestion("DELETE RECORDS", "All records will be cleared!!!") == 'yes':
        c.execute("DELETE FROM Trans")
        conn.commit()
        messagebox.showinfo("DELETE", "All records deleted")
    else:
        pass


def clear_Supplier_Record():
    if messagebox.askquestion("DELETE RECORDS", "All records will be cleared!!!") == 'yes':
        c.execute("DELETE FROM administration")
        conn.commit()
        messagebox.showinfo("DELETE", "All records deleted")
    else:
        pass


def delete_tr():
    try:
        treeview1.selection()['values'][0]
    except IndexError as e:
        messagebox.showinfo("Delete Record", "Please select record")
        return
    # for selected_item in treeview
    name = treeview1.selection()['text']
    query = "DELETE FROM Trans WHERE ID = ?"
    conn.execute(query, (name,))
    conn.commit()
    view_tr()


def view_tr():
    records = treeview1.get_children()
    for elements in records:
        treeview1.delete(elements)
    c.execute("SELECT * FROM Trans")
    result = c.fetchall()
    for s in result:
        treeview1.insert("", 'end', values=s)


def ids():
    try:
        res = c.execute("SELECT ID FROM Trans")
        result = res.fetchall()
        for i in result:
            trans_Entry.get()
            trans.set(i)
    except:
        pass


def cal():
    global amount
    try:
        summ = amount_per_litre_Entry.get()
        amount = kg_Entry.get()
        prices = price_naira_Entry.get()
        if amount:
            price_val = int(amount) * int(summ)
            pri.set(price_val)
        if prices:
            kg_val = int(prices) / int(summ)
            rou = round(kg_val, 2)
            kg.set(rou)
    except:
        pass


def saves():
    summ = amount_per_litre_Entry.get()
    amount = kg_Entry.get()
    prices = price_naira_Entry.get()

    if messagebox.askquestion("Save", "Do you want to Save?") == 'yes':
        sql_insert = "INSERT INTO 'Trans'(Amount_per_litre,Amount_Kg,price,DOT)VALUES(?,?,?,?)"
        c.execute(sql_insert, (summ, amount, prices, times))
        conn.commit()
        messagebox.showinfo("Save", "Transaction Saved!")
        ids()
        iview()
        # iprint()
        # clear_tr()
    else:
        pass


def clear_tr():
    amounts = kg_Entry.get()
    prices = price_naira_Entry.get()
    kg_Entry.delete(0, END)
    price_naira_Entry.delete(0, END)
    trans_Entry.delete(0, END)


def close():
    if close:
        closes = messagebox.askquestion("Quit", "Are yo sure you want to close")
    if closes == 'yes':
        new_window.destroy()

    elif closes == 'no':
        pass


def close_tr():
    saleswin.destroy()


def infos():
    info = Toplevel(new_window)
    info.title("Organisation Information")
    info.geometry("500x500")
    global name1_info, ad_info, ph_info1
    name_info = ttk.Label(info, text="Organsation Name")
    name_info.grid(row=0, column=0)
    name1_info = ttk.Entry(info)
    name1_info.grid(row=0, column=5, padx=5, pady=5)

    ad_info = Text(info, width=20, height=10)
    ad_info.grid(row=5, column=5)
    # ad_info1 = ttk.Entry(info)
    # ad_info1.grid(row=5, column=10,padx=10,pady=10)

    ph_info = ttk.Label(info, text="Phone Number")
    ph_info.grid(row=8, column=0)
    ph_info1 = ttk.Entry(info)
    ph_info1.grid(row=8, column=5, padx=10, pady=10)

    info_button = ttk.Button(info, text="Ok", command=upinfo)
    info_button.grid(row=15, column=5)


def getinfo():
    v1 = name1_info.get()
    v2 = ad_info.get("1.0", "end")
    v3 = ph_info1.get()

    sql = "INSERT INTO 'info'(Name,Address,phone)VALUES(?,?,?)"
    c.execute(sql, (v1, v2, v3))
    conn.commit()
    messagebox.showinfo("Organisational info", "Saved")


def upinfo():
    v4 = name1_info.get()
    v5 = ad_info.get("1.0", "end")
    v6 = ph_info1.get()
    sql = "UPDATE info SET Name=?,Address=?,phone=? WHERE ID=1"
    c.execute(sql, (v4, v5, v6))
    conn.commit()
    messagebox.showinfo("Organisational info", "Saved")


def iview():
    r1 = []
    r2 = []
    r3 = []
    l = time.asctime(time.localtime())
    tranc_id = trans_Entry.get()
    print_amount = amount_per_litre_Entry.get()
    print_kg = kg_Entry.get()
    print_total = price_naira_Entry.get()
    c.execute("SELECT *FROM info")
    res = c.fetchall()

    for i in res:
        r1 = i[1]
        r2 = i[2]
        r3 = i[3]
    text1.insert(END, r1)
    text1.insert(END, '\n')
    text1.insert(END, r2)
    text1.insert(END, '\n')
    text1.insert(END, r3)
    text1.insert(END, '\n')
    text1.insert(END, "Roll No: ")
    text1.insert(END, tranc_id, '\n')
    text1.insert(END, "\nAmount per liter:")
    text1.insert(END, print_amount)
    text1.insert(END, "\nKilogram:")
    text1.insert(END, print_kg)
    text1.insert(END, "\nPrice:")
    text1.insert(END, print_total)
    text1.insert(END, "\nDate:")
    text1.insert(END, l, '\n')
    # text1.insert(END, "\nTime:")
    # text1.insert(END, tt, '\n'+'\n')
    text1.insert(END, "\n\n\n")

    if text1 == 1:
        pass


def iprint():
    if messagebox.askquestion("Print", "Do you want to print?") == 'yes':
        font = {'height': 10, 'width': 0, }

        with Printer(linegap=1, printer_name='XP-80C', auto_page=True) as printer:
            q = text1.get("1.0", "end-1c")
            printer.text(q, font_config=font)
            printer.new_page()


    else:
        pass


# create_admin=ttk.Button(admin,text = "create Account",command=create_admin)
# create_admin.grid(row=6,column=6)
# create_user=ttk.Button(user,text = "create Account", command = create_admin1 )
# create_user.grid(row=6,column=6)
login = ttk.Button(admin, text="Login", command=login_account)
login.grid(row=3, column=6)
user_login = ttk.Button(user, text="Login", command=login_account1)
user_login.grid(row=3, column=6)

window.mainloop()
