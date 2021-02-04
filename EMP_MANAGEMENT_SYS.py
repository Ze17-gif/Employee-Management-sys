from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import sqlite3

#=========== Final code for Finals   
#===================== Creates Database and Table

def Connect():
        global conn
        global c
        # Create Database file
        conn = sqlite3.connect("DATA_BASE_EMP.dbP")
        # Create Cursor
        c = conn.cursor()
        #Create Table
        c.execute(""" CREATE TABLE IF NOT EXISTS tbl_employees 
                (id integer primary key AUTOINCREMENT,
                E_lastname text,                                                        
                E_firstname text,                                                       
                E_gender text,                                                          
                E_status text,                                                          
                E_address text,                                                         
                E_contact_number integer,                                               
                E_email text,                                                           
                E_department text,                                                      
                E_position text,                                                        
                E_salary integer                                                        
                )""")        
        c.execute("""CREATE TABLE IF NOT EXISTS Login_Register_TBL
                (username text,
                password text )""")

def Commit_close():
        #Commit changes 
        conn.commit()
        #Close connection        
        conn.close()
        

#====Designing Login window
def Login_screen():

    global main_screen
    global username_login_entry
    global password_login_entry
    main_screen = Tk()
    main_screen.geometry("500x350+550+250")
    main_screen.title("Employee Management System")
    main_screen.resizable(FALSE, FALSE)
    Label(text="EMPLOYEE MANAGEMENT SYSTEM", bg="gold", width="300", height="2", font=("Calibri", 13)).pack(pady=2)
 
    username_lbl= Label (main_screen,font=('arial',10, 'bold'), text="Username:",bd=7)
    username_lbl.pack()
    username_login_entry = Entry(main_screen, width=30,bd=7)
    username_login_entry.pack()

    password_lbl= Label (main_screen,font=('arial',10, 'bold'), text="Password:",bd=7)
    password_lbl.pack()
    password_login_entry = Entry(main_screen, width=30,bd=7, show= '•')  # (  alt numpad 7  '•' )
    password_login_entry.pack(pady=10)

    global reg_btn
    Button(text="Login", height="1", width="20", bd=7, command = login_verify).pack(pady=10)
    Label(text="Not registered yet? Please click the button below to register.", fg='RED' ).pack()
    reg_btn = Button(text="Register", height="1", width="20", bd=7, command=register)
    reg_btn.pack()

    main_screen.protocol("WM_DELETE_WINDOW")
    main_screen.mainloop()

#============ Register Button command

def activate_btn():
        reg_btn.config(state=ACTIVE)
        register_screen.destroy()

#========= registration window

def register():

    reg_btn.config(state=DISABLED)
    

    global register_screen
    global username_entry
    global password_entry
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250+650+250")
    register_screen.resizable(FALSE, FALSE) 

 
    Label(register_screen, text="REGISTRATION", bg="gold", width=300, height=2).pack()
    
    username_lable = Label(register_screen, text="Username:" ,font=("Calibri", 13))
    username_lable.pack()

    username_entry = Entry(register_screen, bd=7)
    username_entry.pack()

    password_lable = Label(register_screen, text="Password: " ,font=("Calibri", 13))
    password_lable.pack()

    password_entry = Entry(register_screen, show='•', bd=7) # (  alt numpad 7  '•' ) 
    password_entry.pack(pady=10)

    btn_rgn=Button(register_screen, text="Register",width=10, height=1, bd=7, command = register_user)
    btn_rgn.pack()
    register_screen.protocol("WM_DELETE_WINDOW", activate_btn)

#============= register_user command

def register_user():
    
    reg_user = username_entry.get()
    reg_pass = password_entry.get()

    Connect()
    c.execute("Select * FROM Login_Register_TBL WHERE username='"+ reg_user +"'") #AND password = '" + reg_pass + "'
    rows=c.fetchall()

    if not rows:
        c.execute("""
        INSERT INTO Login_Register_TBL 
                (username, password) 
        VALUES
                (:username, :password)""",[reg_user, reg_pass])
        conn.commit()   

        tk.messagebox.showinfo("Registration", "Registration success!")
        register_screen.destroy()
        reg_btn.config(state=ACTIVE)

    elif not reg_user or not reg_pass:
        tk.messagebox.showerror("Error","Please fill up all fields")
        register_screen.focus()

    else: # existing
        tk.messagebox.showerror("Registration", "Username already exists!")
        register_screen.focus_force()

#============== Command Login button to continue to EMPLOYEE MANAGEMENT

def login_verify():

    global username_verify

    username_verify = username_login_entry.get()
    password_verify = password_login_entry.get()

    Connect()
    c.execute("Select * FROM Login_Register_TBL WHERE username='"+ username_verify +"' AND password = '" + password_verify + "' ")
    rows=c.fetchall() 

    if not username_verify or not password_verify: # checks if entry is empty 
        tk.messagebox.showerror("Error","Please fill up all fields.")

    elif not rows:
        tk.messagebox.showerror("Error", "Login failed.")


    else:
        main_screen.destroy()
        root_screen()

#=== Employee Management system
def root_screen():

 #=== Employee window (root)
    root = tk.Tk()

 #=== Name of the window
    root.title('Employee management system')

 #====================== Default size of the window ======================
    root.geometry("1170x670+150+50") #(W x H + X + Y (Coordinates)) (Smaller SIZE)
   
 #================ To Enable the Resize of the Window ====================
    root.resizable(FALSE, FALSE) #OFF


#======== Initialize to call the DataBase
    Connect() 

#==================================================================== FUNCTIONS in Root ==================================================================================

    #========= EXIT 

    def iExit():
            iExit=tk.messagebox.askyesno(title="Confirm", message="Confirm Exit?")
            
            if iExit == TRUE:
                    root.destroy()

    #====== ADD EMPLOYEE
    def add():
        Connect()
    
        data = ( E_lastname.get(), E_firstname.get(), E_gender_type.get(), E_status_type.get(),  E_address.get(), E_contact_number.get(),
                 E_email.get(), E_department_type.get(),  E_position__type.get(), E_salary_type.get()) 
        print(data)

        #=============== Checks if entry is empty
        if not data[0] or not data[1] or not data[2] or not data[3] or not data[4] or not data[5] or not data[6] or not data[7] or not data[8] or not data[9] :
            error="All fields need value"
            tk.messagebox.showerror("Error", error,)
        elif not  data[5].isnumeric():      
            error="invalid input in contact number"
            tk.messagebox.showerror("Error", error,)
        else:    

        #Save Data
            c.execute("""
            INSERT INTO tbl_employees 
                    (E_lastname,E_firstname,E_gender,E_status,E_address,E_contact_number,E_email,E_department,E_position,E_salary) 
            VALUES
                    (:E_lastname, :E_firstname, :E_gender_type, :E_status_type, :E_address, :E_contact_number, :E_email, :E_department_type, :E_position_type, :E_salary_type)""",data)
            conn.commit()   

            # Clear when Added
            E_lastname.delete(0, END)
            E_firstname.delete(0, END)
            E_gender_type.set('') 
            E_status_type.set('') 
            E_address.delete(0, END)
            E_contact_number.delete(0, END)
            E_email.delete(0, END)
            E_department_type.set('')  
            E_position__type.set('')  
            E_salary_type.set('') 
            print("Insert OK")
            DisplayData()

    #==========Displays DATA
    def DisplayData():
            Connect()
            # print("Connecting to DATA_BASE_EMP")

            #To display Data inside Tree View
            c.execute("Select id, E_lastname,E_firstname,E_gender,E_status,E_address,E_contact_number,E_email,E_department,E_position,E_salary FROM tbl_employees")
            rows = c.fetchall()
            for i in E_view_tree.get_children():
                    E_view_tree.delete(i)
            for data in rows:
                    E_view_tree.insert('', END ,values=data)
            
            conn.close()
            # print("Connection to DATA_BASE_EMP Closed")
            return

# ======== Initialize to call the DataBase
    # Connect()

#============================================================ Employee Management FRAME GUI =============================================================================================

    #===MAIN WINDOW GUI

    MainFrame = Frame(root, bd= 10, relief=RIDGE)
    MainFrame.grid()

    TopFrame= Frame(MainFrame, bd=10, bg="gold",relief = RIDGE)
    TopFrame.pack(side=TOP)

 #================================================================= TITLE (TOP) FRAME =============================================================================================

    TopFrame_lbl= Label(TopFrame, text="Employee Management System" , bg="gold", font= ("arial", 25, 'bold'), width=37, justify = CENTER)
    TopFrame_lbl.grid(padx=150 )


 #==================================================================== MID FRAME =============================================================================================

    MidFrame_lbl=LabelFrame(MainFrame,bd=10, width=1350, height= 300,
            font=('arial',12 , 'bold'), text='Active User:'+ "[  " + username_verify + "  ]" , fg='#10EB2D',relief= RIDGE)  
    MidFrame_lbl.pack(padx=38, side=TOP)

    #==========     INSIDE MID FRAME  SearchFrame(SF)

    In_MID_SF_lbl=LabelFrame(MidFrame_lbl, bd=5, width=250, height=250,
            font=('arial', 12, 'bold'), text='Search Employee', relief= RIDGE)
    In_MID_SF_lbl.grid(row=0, column=2)

    #==========    INSIDE MID FRAME  CredentialsFrame(CF)

    In_MID_CF_lbl=LabelFrame(MidFrame_lbl, bd=5, width=875, height=250,
            font=('arial', 12, 'bold'), text='Input Employee Credentials', relief= RIDGE)
    In_MID_CF_lbl.grid(row=0, column=1)

#==================================================================== BOT FRAME =============================================================================================

    BotFrame_lbl=LabelFrame(MainFrame, bd=10, width=900, height= 400,
            font=('arial', 12, 'bold'), text='Employees Data', relief= RIDGE)
    BotFrame_lbl.pack(padx=38, side=TOP)

#============================================================== SF WIDGETS MID_FRAME 1 ===================================================================================

    E_id_label= Label (In_MID_SF_lbl,font=('arial',10, 'bold'), text="Employee I.D:",bd=7, height=2)
    E_id_label.grid(row=1, column=0)
    E_id = Entry(In_MID_SF_lbl, width=10,bd=7)
    E_id.grid(row=1, column=1)

#============================================================= CF WIDGETS MID_FRAME 1 ===============================================================================================


    E_lastname_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Surname:",bd=7)
    E_lastname_label.grid(row=1, column=0)
    E_lastname = Entry(In_MID_CF_lbl, width=20,bd=7)
    E_lastname.grid(row=1, column=1)

    E_firstname_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="First name:",bd=7)
    E_firstname_label.grid(row=2, column=0)
    E_firstname = Entry(In_MID_CF_lbl, width=20,bd=7)
    E_firstname.grid(row=2, column=1, padx=20)

    E_address_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Address:",bd=7)
    E_address_label.grid(row=3, column=0)
    E_address = Entry(In_MID_CF_lbl, width=20,bd=7)
    E_address.grid(row=3, column=1)    


    E_contact_text = StringVar()

    E_contact_number_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Cellphone number:",bd=7)
    E_contact_number_label.grid(row=4, column=0)
    E_contact_number = Entry(In_MID_CF_lbl, width=20,bd=7, textvariable = E_contact_text )
    E_contact_number.grid(row=4, column=1)

    # Function to limit characters inside Cellphone number
    def character_limit(E_contact_text):
        if len(E_contact_text.get()) > 0:
            E_contact_text.set(E_contact_text.get()[:11])


#============================================================= CF WIDGETS MID_FRAME 1 ======================================================================================

    E_email_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Email:",bd=7)
    E_email_label.grid(row=1, column=3)
    E_email = Entry(In_MID_CF_lbl, width=20,bd=7)
    E_email.grid(row=1, column=4)

    E_department_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Department:",bd=7)
    E_department_label.grid(row=2, column=3)

    E_department_type=ttk.Combobox(In_MID_CF_lbl,                    state='readonly',
            font=('arial',10, 'bold'),width=17)
    E_department_type['value']=('','Production','Research and Development', 'Marketing ', 'Purchasing', 'Human Resource Management', 'Accounting and Finance')
    E_department_type.current(0)
    E_department_type.grid(row=2, column=4)


    E_position_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Position:",bd=7)
    E_position_label.grid(row=3, column=3)

    E_position__type=ttk.Combobox(In_MID_CF_lbl,                    state='readonly',
            font=('arial',10, 'bold'),width=17)
    E_position__type['value']=('','Chief Executive Officer (CEO)','Chief Operating Officer (COO)',
                    'Assistant Manager','Marketing Manager','Chief Financial Officer','Production Manager',
                    'Operations Manager','Safety Manager','Accountant','Purchasing manager','Supervisor,'
                    'Professional staff',)
    E_position__type.current(0)
    E_position__type.grid(row=3,  column=4)

#============================================================= CF WIDGETS MID_FRAME 1 ======================================================================================
    E_gender_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Gender:",bd=7)
    E_gender_label.grid(row=1, column=5)

    E_gender_type=ttk.Combobox(In_MID_CF_lbl,                    state='readonly',  
            font=('arial',10, 'bold'),width=10)
    E_gender_type['value']=('','Male','Female')
    E_gender_type.current(0)
    E_gender_type.grid(row=1, column=6)


    E_status_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Civil status:",bd=7)
    E_status_label.grid(row=2, column=5)

    E_status_type=ttk.Combobox(In_MID_CF_lbl,                    state='readonly',
            font=('arial',10, 'bold'),width=10)
    E_status_type['value']=('','Married','Single','Divorced')
    E_status_type.current(0)
    E_status_type.grid(row=2, column=6)


    E_salary_label= Label (In_MID_CF_lbl,font=('arial',10, 'bold'), text="Salary grade:",bd=7)
    E_salary_label.grid(row=3, column=5)

    E_salary_type=ttk.Combobox(In_MID_CF_lbl,                    state='readonly',
            font=('arial',10, 'bold'),width=10)
    E_salary_type['value']=('','1','2','3','4','5','6','7','8','9')
    E_salary_type.current(0)
    E_salary_type.grid(row=3, column=6)

#============================================================= TREE_VIEW BOT_FRAME =========================================================================================
    global E_view_tree
    scrollbary=Scrollbar(BotFrame_lbl, orient=VERTICAL)
    scrollbarx=Scrollbar(BotFrame_lbl, orient=HORIZONTAL)
 
    # shows='tree', The Display of the DATA records
    
    E_view_tree=ttk.Treeview(BotFrame_lbl, height=15, 
    columns=('ID','Surname', 'Firstname','Gender', 'Status', 'Address', 'Contact number', 'Email', 'Department', 'Posiotn', 'Salary grade', ), show='headings') #show heading to hide #0 or column 0

    # # Set the heading (Attribute Names)
    E_view_tree.heading('#1', text='ID',anchor=W,)
    E_view_tree.heading('#2', text='Surname',anchor=W)
    E_view_tree.heading('#3', text='Firstname',anchor=W)
    E_view_tree.heading('#4', text='Gender',anchor=W)
    E_view_tree.heading('#5', text='Status',anchor=W)
    E_view_tree.heading('#6', text='Address',anchor=W)
    E_view_tree.heading('#7', text='Cellphone number',anchor=W)
    E_view_tree.heading('#8', text='Email',anchor=W)
    E_view_tree.heading('#9', text='Department',anchor=W)
    E_view_tree.heading('#10', text='Position',anchor=W)
    E_view_tree.heading('#11', text='Salary grade',anchor=W)

    # # Specify attributes of the columns
    E_view_tree.column('#1', width=50, minwidth=30,  anchor=W, stretch=NO) # stret             
    E_view_tree.column('#2', width=75, minwidth=50,  anchor=W, stretch=NO)              
    E_view_tree.column('#3', width=75, minwidth=50,  anchor=W, stretch=NO)              
    E_view_tree.column('#4', width=50, minwidth=30,  anchor=W, stretch=NO)              
    E_view_tree.column('#5', width=50, minwidth=30,  anchor=W, stretch=NO)              
    E_view_tree.column('#6', width=100, minwidth=50, anchor=W, stretch=NO)              
    E_view_tree.column('#7', width=100, minwidth=50, anchor=W, stretch=NO)              
    E_view_tree.column('#8', width=140, minwidth=50, anchor=W, stretch=NO)              
    E_view_tree.column('#9', width=150, minwidth=50, anchor=W, stretch=NO)              
    E_view_tree.column('#10', width=150, minwidth=50,anchor=W, stretch=NO)              
    E_view_tree.column('#11', width=90, minwidth=30, anchor=W, stretch=NO)             

    scrollbary.config(command=E_view_tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    E_view_tree.config(yscrollcommand=scrollbary.set)


    scrollbarx.config(command=E_view_tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    E_view_tree.config(xscrollcommand=scrollbarx.set)

    E_view_tree.pack(side=TOP)
    E_view_tree.treeview = E_view_tree


##========================================================= Update Button/Delete Button process ======================================================================================

 #============ Check if Valid ID in Deleting

    def del_update():
        id_record= E_id.get() 
    #     print((len(id_record)==0))
    #     print(not id_record.isnumeric())
        if (len(id_record)==0) or not id_record.isnumeric():
                tk.messagebox.showerror("Error", "Please input valid employee ID",)
        else:
                check_del_id()
 #=========== Check if ID exists to delete

    def check_del_id():
        id_record= E_id.get()

        Connect()
        # To check if ID is existing
        c.execute("Select * FROM tbl_employees WHERE id = "+ id_record)

        # Get data and check if value exists 
        rows =c.fetchall()
        if not rows:
            print("empty data")
            tk.messagebox.showerror("Error", "Employee ID not found. PLease input Valid Employee ID",)
        else:
            do_delete()
 #=============deletes the data

    def do_delete():
            Connect()
            Msg_box = tk.messagebox.askyesno("Warning", "Confirm Delete?",)

            if Msg_box == TRUE:
               c.execute("DELETE from tbl_employees WHERE id="+ E_id.get())
               print ("Employee deleted")
            else:
            print("Employee not deleted")
            return
            Commit_close()
            DisplayData()


 #========================================== CHECK IF ID IS VALID TO BE EDITED

 #=========== Checking if empty or not int

    def show_update():
        id_record= E_id.get() 
        print((len(id_record)==0))
        print(not id_record.isnumeric())
        if (len(id_record)==0) or not id_record.isnumeric():
                tk.messagebox.showerror("Error", "Please input valid employee ID",)
        else:
                check_id()
                
 #=========== Check if ID exists

    def check_id():
        id_record= E_id.get()

        Connect()
        # To check if ID is existing
        c.execute("Select * FROM tbl_employees WHERE id = "+ id_record)

        # Get data and check if value exists 
        rows =c.fetchall()
        if not rows:
            print("empty data")
            tk.messagebox.showerror("Error", "Employee ID not found. PLease input Valid Employee ID",)
        else:
            doupdate()
    
 #============ Procceed to the new window to Update record

    def doupdate():
        id_record= E_id.get()
        confirm_edt=tk.messagebox.askyesno("Confirmation", "Edit employee Number " + id_record + " records?")
        if confirm_edt == FALSE:
            return            

        else:  #========= Window Edit(Bind in root)
            Disable_btn()
            id_record= E_id.get()    
            
            global edit
            edit = Toplevel (root)
            edit.title('Update Employee record')
            edit.geometry("1030x200+400+330") #(W x H + ( X + Y Coordinates) )
            edit.resizable(FALSE, FALSE)  
            # Connect to the data base
            Connect()
            c.execute("Select E_lastname,E_firstname,E_gender,E_status,E_address,E_contact_number,E_email,E_department,E_position,E_salary FROM tbl_employees WHERE id = "+ id_record)
            rows =c.fetchall()
            data=rows[0]
            
        #===========GUI in EDIT WINDOWS
            Ed_MainFrame=Frame(edit, bd= 10, relief=RIDGE)
            Ed_MainFrame.grid()

            Ed_TopFrame= Frame(Ed_MainFrame,bd=10, relief=RIDGE)
            Ed_TopFrame.pack(side=TOP)

        #============= Gui Editing

            Ed_MidFrame_lbl=LabelFrame(Ed_MainFrame,bd=10, width=950, height= 350,
            font=('arial',12 , 'bold'), text='Employee ID:[ ' + id_record+ ' ]', fg='#10EB2D',relief= RIDGE)  
            Ed_MidFrame_lbl.pack(padx=38, side=TOP)


        #============= Gui Editing 1
            Edt_lastname_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Surname:",bd=7)
            Edt_lastname_label.grid(row=1, column=0)
            Edt_lastname = Entry(Ed_MidFrame_lbl, width=30,bd=7)
            Edt_lastname.grid(row=1, column=1)

            Edt_firstname_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="First name:",bd=7)
            Edt_firstname_label.grid(row=2, column=0)
            Edt_firstname = Entry(Ed_MidFrame_lbl, width=30,bd=7)
            Edt_firstname.grid(row=2, column=1, padx=20)

            Edt_address_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Address:",bd=7)
            Edt_address_label.grid(row=3, column=0)
            Edt_address = Entry(Ed_MidFrame_lbl, width=30,bd=7)
            Edt_address.grid(row=3, column=1)


            Edt_contact_text = StringVar()

            Edt_contact_number_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Contact number:",bd=7)
            Edt_contact_number_label.grid(row=4, column=0)
            Edt_contact_number = Entry(Ed_MidFrame_lbl, width=30,bd=7, textvariable = Edt_contact_text)
            Edt_contact_number.grid(row=4, column=1)


            # Function to limit characters inside Cellphone number
            def character_limit_edt(Edt_contact_text):
                if len(Edt_contact_text.get()) > 0:
                    Edt_contact_text.set(Edt_contact_text.get()[:11])

        #============= Gui Editing 2
            Edt_email_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Email:",bd=7)
            Edt_email_label.grid(row=1, column=3)
            Edt_email = Entry(Ed_MidFrame_lbl, width=30,bd=7)
            Edt_email.grid(row=1, column=4)

            Edt_department_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Department:",bd=7)
            Edt_department_label.grid(row=2, column=3)

            Edt_department_type=ttk.Combobox(Ed_MidFrame_lbl,                    state='readonly',           #textvariable= Edt_gender 
                    font=('arial',10, 'bold'),width=27)
            Edt_department_type['value']=(data[7],'','Production','Research and Development', 'Marketing ', 'Purchasing', 'Human Resource Management', 'Accounting and Finance')
            Edt_department_type.current(0)
            Edt_department_type.grid(row=2, column=4)


            Edt_position_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Positzion:",bd=7)
            Edt_position_label.grid(row=3, column=3)

            Edt_position__type=ttk.Combobox(Ed_MidFrame_lbl,                    state='readonly',           #textvariable= Edt_gender 
                    font=('arial',10, 'bold'),width=27)
            Edt_position__type['value']=(data[8],'','Chief Executive Officer (CEO)','Chief Operating Officer (COO)',
                            'Assistant Manager','Marketing Manager','Chief Financial Officer','Production Manager',
                            'Operations Manager','Safety Manager','Accountant','Purchasing manager','Supervisor,'
                            'Professional staff',)
            Edt_position__type.current(0)
            Edt_position__type.grid(row=3,  column=4)


        #================== Gui Editing 3 
            

            Edt_gender_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Gender:",bd=7,)
            Edt_gender_label.grid(row=1, column=5)

            Edt_gender_type=ttk.Combobox(Ed_MidFrame_lbl,                    state='readonly',           #textvariable= E_gender 
                    font=('arial',10, 'bold'),width=10)
            Edt_gender_type['value']=(data[2],'','Male','Female')
            Edt_gender_type.current(0)
            Edt_gender_type.grid(row=1, column=6)


            Edt_status_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Civil status:",bd=7)
            Edt_status_label.grid(row=2, column=5)

            Edt_status_type=ttk.Combobox(Ed_MidFrame_lbl,                    state='readonly',           #textvariable= E_gender  24:19
                    font=('arial',10, 'bold'),width=10)
            Edt_status_type['value']=(data[3],'','Married','Single','Divorced')
            Edt_status_type.current(0)
            Edt_status_type.grid(row=2, column=6)


            Edt_salary_label= Label (Ed_MidFrame_lbl,font=('arial',10, 'bold'), text="Salary grade:",bd=7)
            Edt_salary_label.grid(row=3, column=5)

            Edt_salary_type=ttk.Combobox(Ed_MidFrame_lbl,                    state='readonly',           #textvariable= E_gender 
                    font=('arial',10, 'bold'),width=10)
            Edt_salary_type['value']=(data[9],'', '1','2','3','4','5','6','7','8','9')
            Edt_salary_type.current(0)
            Edt_salary_type.grid(row=3, column=6)


        #================== Insert Data in the Entries
            # data=rows[0]
            print(data)
            Edt_lastname.insert(0, data[0])
            Edt_firstname.insert(0, data[1])
            Edt_address.insert(0, data[4])
            Edt_contact_number.insert(0, data[5])
            Edt_email.insert(0, data[6])


        #===== Functions inside Edting ( do_update() )

            def Edt_Exit():
                Edt_Exit=tk.messagebox.askyesno(title="Employee Records", message="Cancel Edit?")
                if Edt_Exit == TRUE:
                    Enable_btn()
                    edit.destroy()
                        
                else:
                    edit.focus_force()
                    

            def edt_close():
                    Edt_Exit()
            edit.protocol("WM_DELETE_WINDOW", edt_close)

            def Save_edt_Data():
                
                    Connect()
                    print(data)
                    edit_data = ( Edt_lastname.get(), Edt_firstname.get(), Edt_gender_type.get(), Edt_status_type.get(),  Edt_address.get(), Edt_contact_number.get(), Edt_email.get(), Edt_department_type.get(), Edt_position__type.get(), Edt_salary_type.get())
                    if not edit_data[0] or not edit_data[1] or not edit_data[2] or not edit_data[3] or not edit_data[4] or not edit_data[5] or not edit_data[6] or not edit_data[7] or not edit_data[8] or not edit_data[9] :
                        
                        error="All fields need value"
                        tk.messagebox.showerror("Error", error,)
                        edit.focus_force()

                    elif not edit_data[5].isnumeric():      
                        error="invalid input in contact number"
                        tk.messagebox.showerror("Error", error,)
                        edit.focus_force()

                    else:
                        c.execute("""UPDATE tbl_employees SET
                            E_lastname = :E_lastname,
                            E_firstname = :E_firstname,
                            E_gender = :E_gender,
                            E_status = :E_status,
                            E_address = :E_address,
                            E_contact_number = :E_contact_number,
                            E_email = :E_email,
                            E_department = :E_department,
                            E_position = :E_position,
                            E_salary = :E_salary
                            
                            WHERE id = :oid""", 
                            {
                            'E_lastname': Edt_lastname.get(),
                            'E_firstname': Edt_firstname.get(),
                            'E_gender': Edt_gender_type.get(),
                            'E_status': Edt_status_type.get(),
                            'E_address': Edt_address.get(),
                            'E_contact_number': Edt_contact_number.get(),
                            'E_email': Edt_email.get(),
                            'E_department': Edt_department_type.get(),
                            'E_position': Edt_position__type.get(),
                            'E_salary': Edt_salary_type.get(),
                            'oid': id_record

                        })

                        Commit_close()
                        DisplayData()
                        Enable_btn()
                        edit.protocol("WM_DELETE_WINDOW", on_closing)
                        edit.destroy()

                    
        #================== Buttons in Edit_window

        ##==========Add Button
            btn_add=Button(Ed_MidFrame_lbl, bd=7, text="Update Record", command=Save_edt_Data)
            btn_add.grid(row=4, column=4, columnspan=1, pady=10, padx= 10, ipadx=50 )

        #==========EXIT Button
            btn_exit=Button(Ed_MidFrame_lbl, bd=7, text="Cancel Edit", command=Edt_Exit)
            btn_exit.grid(row=4, column=5,columnspan=2, pady=10, padx= 10,ipadx=70)

        #==========To limit the characters inside Cellphone number
            Edt_contact_text.trace("w", lambda *args: character_limit(Edt_contact_text))

#============================================================== End of update windows ==================================================================================

#============================================================== BUTTONS in MAIN FRAME  =================================================================================

 ##============================================================= CF MID_FRAME BUTTON  ======================================================================================

    ##==========Add Button
    btn_add=Button(In_MID_CF_lbl, bd=7, text="Add Employee", command=add)
    btn_add.grid(row=4, column=4, columnspan=1, pady=10, padx= 10, ipadx=50 )# columnspan=1, pady=10, padx= 10, ipadx=50)

    #==========EXIT Button
    btn_exit=Button(In_MID_CF_lbl, bd=7, text="Exit", command=iExit)
    btn_exit.grid(row=4, column=5,columnspan=2, pady=10, padx= 10,ipadx=70)# columnspan=1, pady=10, padx= 10, ipadx=50)
 ##============================================================= SF MID_FRAME BUTTON  ======================================================================================

    ##==========UPDATE Button
    def Disable_btn():    
        btn_update.configure(state=DISABLED)

    def Enable_btn():
        btn_update.configure(state=ACTIVE)

    ##==========DELETE Button
    btn_delete=Button(In_MID_SF_lbl, bd=7, text="Delete Record", command=del_update, state=ACTIVE) #command=delete)
    btn_delete.grid(row=3, column=0, columnspan=2, pady=7, padx= 10, ipadx=50)

     ##==========Update Button
    btn_update=Button(In_MID_SF_lbl, bd=7, text="Update Record", command=show_update)
    btn_update.grid(row=2, column=0, columnspan=2, pady=9, padx= 10, ipadx=50)


#=============================================================================

    Commit_close()

    #======== Calls the function To display data automatically when program runs
    DisplayData()

    def on_closing():
        iExit()
    #== Ask to exit when [X] button is clicked    
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # To limit the characters inside Cellphone number
    E_contact_text.trace("w", lambda *args: character_limit(E_contact_text))

    #Call all the code inside root
    root.mainloop()
    
#====== Runs the whole program
Login_screen()
