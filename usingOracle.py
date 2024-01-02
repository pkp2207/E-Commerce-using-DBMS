import cx_Oracle
import datetime
from prettytable import PrettyTable

connection = cx_Oracle.connect("system", "12201mysql", "localhost:1521/xe")
today = datetime.date.today()
c1 = connection.cursor()


with open("CartDeletionTrigger.sql", "r") as script:
    trigger_script = script.read()
statements = trigger_script.split(';')
try:
    for statement in statements:
        if statement.strip():  # Skip empty statements
            c1.execute(statement)
    connection.commit()
    print("Script executed successfully.")
except cx_Oracle.Error as error:
    print(f"Error executing script: {error}")


def add_to_cart():
    ci = input("Enter cart id: ")
    c1.execute("SELECT Cart_id FROM  Cart_Ecommerce")
    cid_in_table = [row[0] for row in c1.fetchall()]
    if len(ci) > 6:
        print("The cart id must contain 6 or less characters.")
        return False
    if ci in cid_in_table:
        print(f"Cart id {ci} already exists in the table.")
        return False
    else:
        try:
            st = "insert into cart_ecommerce values('{}')".format(ci)
            c1.execute(st)
            connection.commit()
            print("Data added successfully.")
        except cx_Oracle.DataError as e:
            print("data error", e)


def add_to_category():
    c1.execute("SELECT CATEGORY_ID FROM CATEGORY_ECOMMERCE")
    cate_id_in_table = [row[0] for row in c1.fetchall()]
    cate_id = input("Enter category id: ")
    if len(cate_id) > 6:
        print("The category id must contain 6 or less characters.")
        return False
    if cate_id in cate_id_in_table:
        print(f"Category id {cate_id} already exists in the table.")
        return False
    c1.execute("SELECT CATEGORY_NAME FROM CATEGORY_ECOMMERCE")
    cate_name_in_table = [row[0] for row in c1.fetchall()]
    cate_name = input("Enter category name: ")
    if len(cate_name) > 30:
        print("The category name must contain 30 or less characters.")
        return False
    if cate_name in cate_name_in_table:
        print(f"Category {cate_name} already exists in the table.")
        return False
    try:
        st = "insert into category_ecommerce values('{}','{}')".format(cate_id, cate_name)
        c1.execute(st)
        connection.commit()
        print("Data added successfully.")
    except cx_Oracle.DataError as e:
        print("data error", e)


def add_to_customers():
    c1.execute("SELECT Customer_ID FROM CUSTOMERS_ECOMMERCE")
    cust_id_in_table = [row[0] for row in c1.fetchall()]
    cust_id = input("Enter customer id: ")
    if len(cust_id) > 10:
        print("The customer id must contain 10 or less characters.")
        return False
    if cust_id in cust_id_in_table:
        print(f"Customer id {cust_id} already exists in the table.")
        return False
    cust_name = input("Enter customer's name: ")
    if len(cust_name) > 25:
        print("The customer name must contain 25 or less characters.")
        return False
    cust_address = input("Enter address: ")
    if len(cust_address) > 50:
        print("The customer address must contain 50 or less characters.")
        return False
    pin = int(input("Enter pincode: "))
    ph_no = int(input("Enter phone number: "))
    if len(str(ph_no)) != 10:
        print("The phone number must contain 10 digits.")
        return False
    c_id = input("Enter cart id: ")
    c1.execute("SELECT CART_ID FROM CART_ECOMMERCE")
    cart_id_in_table = [row[0] for row in c1.fetchall()]
    if c_id not in cart_id_in_table:
        print("Such a cart id doesn't exist in the database.")
        return False
    try:
        c1.execute(f"insert into customers_ecommerce values('{cust_id}','{cust_name}','{cust_address}',{pin},{ph_no},'{c_id}')")
        connection.commit()
        print("Data added successfully.")
    except cx_Oracle.DataError as e:
        print("data error", e)


def add_to_login_details():
    c1.execute("SELECT USERNAME FROM LOGIN_DETAILS_ECOMMERCE")
    username_in_table = [row[0] for row in c1.fetchall()]
    user_name = input("Enter username: ")
    if user_name in username_in_table:
        print("The username is already taken.")
        return False
    if len(user_name) > 30:
        print("The username must be 30 characters or less.")
        return False
    pw = input("Enter password: ")
    if len(pw) < 8:
        print("Password must be at least 8 characters long.")
        return False
    try:
        st = "insert into login_details_ecommerce values('{}','{}')".format(user_name, pw)
        c1.execute(st)
        connection.commit()
        print("Data added successfully")
    except cx_Oracle.DataError as e:
        print("data error", e)


def add_to_payment():
    c1.execute("SELECT USERNAME FROM LOGIN_DETAILS_ECOMMERCE")
    pay_id_in_table = [row[0] for row in c1.fetchall()]
    pay_id = input("Enter payment id: ")
    if pay_id in pay_id_in_table:
        print(f"The payment id {pay_id} already exists in the database.")
        return False
    if len(pay_id) > 7:
        print("The payment id must contain 7 or less characters.")
        return False
    pay_date = input("Enter payment date(YYYY-MM-DD): ")
    try:
        pay_datetime = datetime.datetime.strptime(pay_date, "%Y-%m-%d")
    except ValueError:
        print("Payment Date should be in the format YYYY-MM-DD.")
        return False
    if today.year < pay_datetime.year and today.month < pay_datetime.month and today.day < pay_datetime.day:
        print("Please enter appropriate Payment date.")
        return False
    pay_type = input("Enter payment type(cash/card/upi): ").lower()
    if pay_type not in ('cash', 'card', 'upi'):
        print("Payment type must be one of cash, card and upi.")
        return False
    cid = input("Enter customer id: ")
    c1.execute("SELECT CUSTOMER_ID FROM CUSTOMERS_ECOMMERCE")
    customer_id_in_table = [row[0] for row in c1.fetchall()]
    if cid not in customer_id_in_table:
        print(f"The customer id {cid} doesn't exist in the database.")
        return False
    cartid = int(input("Enter cart id: "))
    c1.execute("SELECT CART_ID FROM CART_ECOMMERCE")
    cart_id_in_table = [row[0] for row in c1.fetchall()]
    if cartid not in cart_id_in_table:
        print(f"The cart id {cartid} doesn't exist in the database.")
        return False
    tot_amt = float(input("Enter total amount: "))
    try:
        st = "insert into payment_ecommerce values('{}','{}','{}','{}',{},'{}')".format(pay_id, pay_date, pay_type,
                                                                                         cid, cartid, tot_amt)
        c1.execute(st)
        connection.commit()
        print("Data added successfully")
    except cx_Oracle.DataError as e:
        print("data error", e)


def add_to_product():
    pro_id = input("Enter product id: ")
    if len(pro_id) > 7:
        print("The product id must contain 7 or less characters.")
        return False
    pro_name = input("Enter product name : ")
    if len(pro_name) > 7:
        print("The product name must contain 30 or less characters.")
        return False
    pro_cate_id = input("Enter product category id : ")
    c1.execute("SELECT PRODUCT_CATEGORYID FROM PRODUCT_ECOMMERCE")
    cate_id_in_table = [row[0] for row in c1.fetchall()]
    if pro_cate_id not in cate_id_in_table:
        print(f"The category id {pro_cate_id} doesn't exist in the database.")
        return False
    pro_color = input("Enter color of product : ")
    if len(pro_color) > 15:
        print("The product color must contain 15 or less characters.")
        return False
    pro_size = input("Enter product size(XS,S,M,L,XL,XXL,XXXL,XXXXL) :").lower()
    if pro_size not in ('xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl', 'xxxxl'):
        print("Please enter a valid product size.")
        return False
    pro_gender = input("Enter gender (m/f): ").lower()
    if pro_gender not in ('m', 'f'):
        print("Please enter a valid gender.")
        return False
    pro_website_commission = int(input("Enter website commission : "))
    if pro_website_commission > 100 or pro_website_commission < 0:
        print("Please enter a valid percentage.")
        return False
    pro_cost = int(input("Enter Cost : "))
    pro_quantity = int(input("Enter Quantity : "))
    pro_seller_id = input("Enter seller id : ")
    c1.execute("SELECT SELLER_ID FROM SELLER_ECOMMERCE")
    seller_id_in_table = [row[0] for row in c1.fetchall()]
    if pro_seller_id not in seller_id_in_table:
        print(f"The seller id {pro_seller_id} doesn't exist in the database.")
        return False
    try:
        st = "insert into product_ecommerce('{}','{}','{}','{}','{}','{}',{},{},{},{})".format(pro_id,
                                                                                               pro_name, pro_cate_id,
                                                                                               pro_color,
                                                                                               pro_size, pro_gender,
                                                                                               pro_website_commission,
                                                                                               pro_cost,
                                                                                               pro_quantity,
                                                                                               pro_seller_id)
        c1.execute(st)
        connection.commit()
        print("Data added successfully")
    except cx_Oracle.DataError as e:
        print("data error", e)


def add_to_seller_ecommerce():
    seller_id = input("Enter seller id: ")
    c1.execute("SELECT SELLER_ID FROM SELLER_ECOMMERCE")
    seller_id_in_table = [row[0] for row in c1.fetchall()]
    if seller_id in seller_id_in_table:
        print(f"The seller id {seller_id} already exists in the database.")
        return False
    if len(seller_id) > 6:
        print("Seller id must contain 6 or less characters.")
    seller_name = input("Enter seller's name: ")
    if len(seller_name) > 20:
        print("Seller name must contain 20 or less characters.")
        return False
    seller_email = input("Enter Seller email_id: ")
    if "@" not in seller_email:
        print("Email must contain the @ symbol.")
        return False
    ph_no = int(input("Enter phone number: "))
    if len(str(ph_no)) != 10:
        print("The phone number must contain exactly 10 digits.")
        return False
    seller_address = input("Enter address: ")

    try:
        st = "insert into seller_ecommerce values('{}','{}','{}',{},'{}')".format(seller_id, seller_name,
                                                                                  seller_email, ph_no, seller_address)
        c1.execute(st)
        connection.commit()
        print("Data added successfully")
    except cx_Oracle.DataError as e:
        print("data error", e)


def print_table(table_name):
    c1.execute(f"SELECT * FROM {table_name}")
    table_data = c1.fetchall()
    if len(table_data) > 0:
        print(f"\n{table_name} Table:")
        table = PrettyTable()
        table.field_names = [desc[0] for desc in c1.description]
        for row in table_data:
            table.add_row(row)
        print(table)
    else:
        print(f"\n{table_name} Table is empty.")


def update_cart(cart_id):
    try:
        new_value = input("Enter new Cart_id: ")
        c1.execute(f"UPDATE Cart_Ecommerce SET Cart_id = :new_value WHERE Cart_id = :cart_id", {'new_value': new_value, 'cart_id': cart_id})
        connection.commit()
        print(f"Cart with Cart_id {cart_id} updated successfully.")

    except cx_Oracle.Error as error:
        print(f"Error updating cart: {error}")


def update_category(category_id):
    try:
        print("Select attribute to update:")
        print("1. Category_id")
        print("2. Category_Name")
        # Add more attributes as needed

        choice = input("Enter your choice: ")

        if choice == "1":
            new_value = input("Enter new Category_id: ")
            c1.execute(f"UPDATE Category_ECommerce SET Category_id = :new_value WHERE Category_id = :category_id", {'new_value': new_value, 'category_id': category_id})
        elif choice == "2":
            new_value = input("Enter new Category_Name: ")
            c1.execute(f"UPDATE Category_ECommerce SET Category_Name = :new_value WHERE Category_id = :category_id", {'new_value': new_value, 'category_id': category_id})
        # Add more cases for other attributes
        else:
            print("Invalid choice. Please try again.")
            return

        connection.commit()
        print(f"Category with Category_id {category_id} updated successfully.")

    except cx_Oracle.Error as error:
        print(f"Error updating category: {error}")


def update_customer(customer_id):
    try:
        print("Select attribute to update:")
        print("1. Customer_id")
        print("2. Customer_Name")
        print("3. Address")
        print("4. Pincode")
        print("5. Phone_number")
        print("6. Cart_id")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_value = input("Enter new Customer_id: ")
            c1.execute(f"UPDATE Customers_Ecommerce SET Customer_id = :new_value WHERE Customer_id = :customer_id", {'new_value': new_value, 'customer_id': customer_id})
        elif choice == "2":
            new_value = input("Enter new Customer_Name: ")
            c1.execute(f"UPDATE Customers_Ecommerce SET Customer_Name = :new_value WHERE Customer_id = :customer_id", {'new_value': new_value, 'customer_id': customer_id})
        elif choice == "3":
            new_value = input("Enter new Address: ")
            c1.execute(f"UPDATE Customers_Ecommerce SET Address = :new_value WHERE Customer_id = :customer_id", {'new_value': new_value, 'customer_id': customer_id})
        elif choice == "4":
            new_value = input("Enter new Pincode: ")
            c1.execute(f"UPDATE Customers_Ecommerce SET Pincode = :new_value WHERE Customer_id = :customer_id", {'new_value': new_value, 'customer_id': customer_id})
        elif choice == "5":
            new_value = input("Enter new Phone_number: ")
            c1.execute(f"UPDATE Customers_Ecommerce SET Phone_number = :new_value WHERE Customer_id = :customer_id", {'new_value': new_value, 'customer_id': customer_id})
        elif choice == "6":
            new_value = input("Enter new Cart_id: ")
            c1.execute(f"UPDATE Customers_Ecommerce SET Cart_id = :new_value WHERE Customer_id = :customer_id", {'new_value': new_value, 'customer_id': customer_id})
        else:
            print("Invalid choice. Please try again.")
            return

        connection.commit()
        print(f"Customer with Customer_id {customer_id} updated successfully.")

    except cx_Oracle.Error as error:
        print(f"Error updating customer: {error}")


def update_login_details(username):
    try:
        print("Select attribute to update:")
        print("1. Username")
        print("2. User_Password")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_value = input("Enter new Username: ")
            c1.execute(f"UPDATE Login_Details_Ecommerce SET Username = :new_value WHERE Username = :username", {'new_value': new_value, 'username': username})
        elif choice == "2":
            new_value = input("Enter new User_Password: ")
            c1.execute(f"UPDATE Login_Details_Ecommerce SET User_Password = :new_value WHERE Username = :username", {'new_value': new_value, 'username': username})
        # Add more cases for other attributes
        else:
            print("Invalid choice. Please try again.")
            return

        connection.commit()
        print(f"Login details with Username {username} updated successfully.")

    except cx_Oracle.Error as error:
        print(f"Error updating login details: {error}")


def update_payment(payment_id):
    try:
        print("Select attribute to update:")
        print("1. Payment_id")
        print("2. Payment_date")
        print("3. Payment_type")
        print("4. Customer_id")
        print("5. Cart_id")
        print("6. total_amount")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_value = input("Enter new Payment_id: ")
            c1.execute(f"UPDATE Payment_Ecommerce SET Payment_id = :new_value WHERE Payment_id = :payment_id", {'new_value': new_value, 'payment_id': payment_id})
        elif choice == "2":
            new_value = input("Enter new Payment_date (YYYY-MM-DD): ")
            c1.execute(f"UPDATE Payment_Ecommerce SET Payment_date = TO_DATE(:new_value, 'YYYY-MM-DD') WHERE Payment_id = :payment_id", {'new_value': new_value, 'payment_id': payment_id})
        elif choice == "3":
            new_value = input("Enter new Payment_type: ")
            c1.execute(f"UPDATE Payment_Ecommerce SET Payment_type = :new_value WHERE Payment_id = :payment_id", {'new_value': new_value, 'payment_id': payment_id})
        elif choice == "4":
            new_value = input("Enter new Customer_id: ")
            c1.execute(f"UPDATE Payment_Ecommerce SET Customer_id = :new_value WHERE Payment_id = :payment_id", {'new_value': new_value, 'payment_id': payment_id})
        elif choice == "5":
            new_value = input("Enter new Cart_id: ")
            c1.execute(f"UPDATE Payment_Ecommerce SET Cart_id = :new_value WHERE Payment_id = :payment_id", {'new_value': new_value, 'payment_id': payment_id})
        elif choice == "6":
            new_value = input("Enter new total_amount: ")
            c1.execute(f"UPDATE Payment_Ecommerce SET total_amount = :new_value WHERE Payment_id = :payment_id", {'new_value': new_value, 'payment_id': payment_id})
        # Add more cases for other attributes
        else:
            print("Invalid choice. Please try again.")
            return

        connection.commit()
        print(f"Payment with Payment_id {payment_id} updated successfully.")

    except cx_Oracle.Error as error:
        print(f"Error updating payment: {error}")


def update_product(product_id):
    try:
        print("Select attribute to update:")
        print("1. Product_id")
        print("2. Product_Name")
        print("3. Product_Categoryid")
        print("4. Color")
        print("5. P_Size")
        print("6. Gender")
        print("7. Website_Commission")
        print("8. Cost")
        print("9. Quantity")
        print("10. Seller_id")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_value = input("Enter new Product_id: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Product_id = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "2":
            new_value = input("Enter new Product_Name: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Product_Name = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "3":
            new_value = input("Enter new Product_Categoryid: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Product_Categoryid = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "4":
            new_value = input("Enter new Color: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Color = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "5":
            new_value = input("Enter new P_Size: ")
            c1.execute(f"UPDATE Product_Ecommerce SET P_Size = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "6":
            new_value = input("Enter new Gender: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Gender = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "7":
            new_value = input("Enter new Website_Commission: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Website_Commission = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "8":
            new_value = input("Enter new Cost: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Cost = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "9":
            new_value = input("Enter new Quantity: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Quantity = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        elif choice == "10":
            new_value = input("Enter new Seller_id: ")
            c1.execute(f"UPDATE Product_Ecommerce SET Seller_id = :new_value WHERE Product_id = :product_id", {'new_value': new_value, 'product_id': product_id})
        else:
            print("Invalid choice. Please try again.")
            return

        connection.commit()
        print(f"Product with Product_id {product_id} updated successfully.")

    except cx_Oracle.Error as error:
        print(f"Error updating product: {error}")


def update_seller(seller_id):
    try:
        print("Select attribute to update:")
        print("1. Seller_id")
        print("2. Name")
        print("3. Email_id")
        print("4. Phone_number")
        print("5. Address")
        # Add more attributes as needed

        choice = input("Enter your choice: ")

        if choice == "1":
            new_value = input("Enter new Seller_id: ")
            c1.execute(f"UPDATE Seller_Ecommerce SET Seller_id = :new_value WHERE Seller_id = :seller_id", {'new_value': new_value, 'seller_id': seller_id})
        elif choice == "2":
            new_value = input("Enter new Name: ")
            c1.execute(f"UPDATE Seller_Ecommerce SET Name = :new_value WHERE Seller_id = :seller_id", {'new_value': new_value, 'seller_id': seller_id})
        elif choice == "3":
            new_value = input("Enter new Email_id: ")
            c1.execute(f"UPDATE Seller_Ecommerce SET Email_id = :new_value WHERE Seller_id = :seller_id", {'new_value': new_value, 'seller_id': seller_id})
        elif choice == "4":
            new_value = input("Enter new Phone_number: ")
            c1.execute(f"UPDATE Seller_Ecommerce SET Phone_number = :new_value WHERE Seller_id = :seller_id", {'new_value': new_value, 'seller_id': seller_id})
        elif choice == "5":
            new_value = input("Enter new Address: ")
            c1.execute(f"UPDATE Seller_Ecommerce SET Address = :new_value WHERE Seller_id = :seller_id", {'new_value': new_value, 'seller_id': seller_id})
        # Add more cases for other attributes
        else:
            print("Invalid choice. Please try again.")
            return

        connection.commit()
        print(f"Seller with Seller_id {seller_id} updated successfully.")

    except cx_Oracle.Error as error:
        print(f"Error updating seller: {error}")


def print_search(table_name, key):
    input_key = input(f"Enter {key} to be searched: ")
    c1.execute(f"SELECT * FROM {table_name} where {key}='{input_key}'")
    table_data = c1.fetchall()
    if len(table_data) > 0:
        print(f"\n{table_name} Table:")
        table = PrettyTable()
        table.field_names = [desc[0] for desc in c1.description]
        for row in table_data:
            table.add_row(row)
        print(table)
    else:
        print(f"\n{key} {input_key} doesn't exist in the table {table_name}.")


def search():
    print("Select a table to search from: ")
    print("1. Cart")
    print("2. Category")
    print("3. Customers")
    print("4. Sellers")
    print("5. Products")
    print("6. Payment")
    ch = int(input("Which table do you want to search in?: "))
    if ch == 1:
        print_search("cart_ecommerce", "Cart_id")
    elif ch == 2:
        print_search("category_ecommerce", "Category_id")
    elif ch == 3:
        print_search("customers_ecommerce", "Customer_id")
    elif ch == 4:
        print_search("seller_ecommerce", "Seller_id")
    elif ch == 5:
        print_search("cart_ecommerce", "Product_id")
    elif ch == 6:
        print_search("cart_ecommerce", "Payment_id")
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
    print("\n")


def delete(user_key, table_name, key):
    c1.execute(f"SELECT {key} FROM {table_name}")
    keys_in_table = [row[0] for row in c1.fetchall()]
    if user_key not in keys_in_table:
        print(f"The mentioned {key} {user_key} doesn't exist in the database.")
        return False
    try:
        c1.execute(f"DELETE FROM {table_name} WHERE {key} = :user_key", {'user_key': user_key})
        connection.commit()
        print(f"Entry with {key} {user_key} deleted successfully.")
    except cx_Oracle.Error as error:
        print(f"Error deleting entry from {table_name} table: {error}")
    print("\n")


def display_table_menu():
    print("1. Cart_Ecommerce")
    print("2. Customers_Ecommerce")
    print("3. Seller_Ecommerce")
    print("4. Category_ECommerce")
    print("5. Product_Ecommerce")
    print("6. Login_Details_Ecommerce")
    print("7. Payment_Ecommerce")
    print("\n")


def delete_entry():
    print("Select a table to delete from:")
    display_table_menu()

    choice = input("Enter the number of the table: ")

    if choice == '1':
        cart_id = input("Enter Cart_id to delete: ")
        delete(cart_id, "cart_ecommerce", "Cart_id")
    elif choice == '2':
        customer_id = input("Enter Customer_id to delete: ")
        delete(customer_id, "CUSTOMERS_ECOMMERCE", "CUSTOMER_ID")
    elif choice == '3':
        seller_id = input("Enter Seller_id to delete: ")
        delete(seller_id, "SELLER_ECOMMERCE", "SELLER_ID")
    elif choice == '4':
        category_id = input("Enter Category_id to delete: ")
        delete(category_id, "CATEGORY_ECOMMERCE", "CATEGORY_ID")
    elif choice == '5':
        product_id = input("Enter Product_id to delete: ")
        delete(product_id, "PRODUCT_ECOMMERCE", "PRODUCT_ID")
    elif choice == '6':
        username = input("Enter Username to delete: ")
        delete(username, "LOGIN_DETAILS_ECOMMERCE", "USERNAME")
    elif choice == '7':
        payment_id = input("Enter Payment_id to delete: ")
        delete(payment_id, "PAYMENT_ECOMMERCE", "PAYMENT_ID")
    else:
        print("Invalid choice. Please enter a number between 1 and 7.")
    print("\n")


def verify():
    us = input("Enter username: ")
    pw = input("Enter password: ")
    c1.execute("SELECT * FROM LOGIN_DETAILS_ECOMMERCE")
    username_in_table = [row for row in c1.fetchall()]
    if (us, pw) in username_in_table:
        print("Welcome to our e-commerce website database management system!\n")
        return True
    else:
        print("Invalid username/password.")
        return False


def print_menu():
    print("1. Add a new record.")
    print("2. Search for a particular record.")
    print("3. Delete a record.")
    print("4. Display a table.")
    print("5. Update a record.")
    print("6. Exit.")
    print("\n")


if verify():
    while True:
        print_menu()
        main_choice = input("Enter your choice: ")
        if main_choice == '1':
            print("Select a table to add a record into: ")
            display_table_menu()
            ch_table = int(input("Choose a number: "))
            if ch_table == 1:
                add_to_cart()
            elif ch_table == 2:
                add_to_customers()
            elif ch_table == 3:
                add_to_seller_ecommerce()
            elif ch_table == 4:
                add_to_category()
            elif ch_table == 5:
                add_to_product()
            elif ch_table == 6:
                add_to_login_details()
            elif ch_table == 7:
                add_to_payment()
            else:
                print("Please choose a valid number between 1 and 7.")
            print("\n")
        elif main_choice == '2':
            search()
        elif main_choice == '3':
            delete_entry()
        elif main_choice == '4':
            print("Select a table to be displayed")
            display_table_menu()
            ch_table = int(input("Choose a number: "))
            if ch_table == 1:
                print_table("Cart_Ecommerce")
            elif ch_table == 2:
                print_table("Customers_Ecommerce")
            elif ch_table == 3:
                print_table("Seller_Ecommerce")
            elif ch_table == 4:
                print_table("Category_Ecommerce")
            elif ch_table == 5:
                print_table("Product_Ecommerce")
            elif ch_table == 6:
                print_table("Login_details_Ecommerce")
            elif ch_table == 7:
                print_table("Payment_Ecommerce")
            else:
                print("Please choose a valid number between 1 and 7.")
        elif main_choice == '5':
            print("Select the table which you want to update: ")
            display_table_menu()
            ch_table = int(input("Select the table which you want to update: "))
            if ch_table == 1:
                id = input("Enter cart id whose record you want to update: ")
                update_cart(id)
            elif ch_table == 2:
                id = input("Enter customer id whose record you want to update: ")
                update_customer(id)
            elif ch_table == 3:
                id = input("Enter seller id whose record you want to update: ")
                update_seller(id)
            elif ch_table == 4:
                id = input("Enter category id whose record you want to update: ")
                update_category(id)
            elif ch_table == 5:
                id = input("Enter product id whose record you want to update: ")
                update_product(id)
            elif ch_table == 6:
                id = input("Enter username whose record you want to update: ")
                update_login_details(id)
            elif ch_table == 7:
                id = input("Enter payment id whose record you want to update: ")
                update_payment(id)
            else:
                print("Please enter a number between 1 and 7")
        elif main_choice == '6':
            exit()
        else:
            print("Please choose a number between 1 and 6.")

