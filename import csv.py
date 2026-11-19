import csv
import datetime
import random
import os
##Import images
from PIL import Image
from IPython.display import display


# Function to register a new user
def register_user():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    address = input("Enter your address: ")
    telephone = input("Enter your telephone number: ")
    
#check the user from csv ile
    user_exists = False
    if os.path.exists('users.csv'):
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    print("Username already exists.")
                    user_exists = True
                    break

    if not user_exists:
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if os.stat('users.csv').st_size == 0:
                writer.writerow(['Username', 'Password', 'Address', 'Telephone'])
            writer.writerow([username, password, address, telephone])
        print("User registered successfully.")


# Function to login a user
def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if os.path.exists('users.csv'):
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    if row[1] == password:
                        print("Login successful!")
                        return username
                    else:
                        print("Invalid password.")
                        return None
    print("Invalid username.")
    return None


# Function to login admin
def admin_login():
    admin_key = input("Enter administrator key: ")
    if admin_key == "admin123":
        print("Admin login successful!")
        return True
    else:
        print("Invalid administrator key. Access denied.")
        return False
    
def rating():
        grade = int(input("Please give a grade about our system!!⭐⭐⭐⭐⭐ (1 until 5): "))
        stars = '⭐'*grade
        print(f"Thank you for grading our system for {stars} !!!")
        print("Thanks for !! Please Come Again Next Time!!")
#class for item, create instance object
class Item:
    def __init__(self, category, subcategory, name, quantity, price):
        self.category = category
        self.subcategory = subcategory
        self.name = name
        self.quantity = quantity
        self.price = price

class Cart:
    def __init__(self):
        self.items = []
        
    def is_empty(self):
        return len(self.items) == 0 #for check the cart condition before checkout if 0 return true value, avoid proceed checkout when cart is empty

    def add_to_cart(self, item, quantity):
        for cart_item in self.items:
            if cart_item['item'].name == item.name:
                if cart_item['item'].quantity >= cart_item['quantity'] + quantity:
                    cart_item['quantity'] += quantity
                    print(f"Added {quantity} {item.name}(s) to the cart successfully.")
                else:
                    print(f"Cannot add {quantity} {item.name}(s) to cart. Only {item.quantity - cart_item['quantity']} in stock.")
                return
        if item.quantity >= quantity:
            self.items.append({'item': item, 'quantity': quantity})
            print(f"Added {quantity} {item.name}(s) to the cart successfully.")
        else:
            print(f"Cannot add {quantity} {item.name}(s) to cart. Only {item.quantity} in stock.")

    def view_cart(self):
        total_sum = 0
        print("\n=== Shopping Cart ===")
        if not self.items:
            print("Your cart is empty.")
        else:   #view cart details
            for cart_item in self.items:
                item_name = cart_item['item'].name
                quantity = cart_item['quantity']
                unit_price = cart_item['item'].price
                total_price = quantity * unit_price
                total_sum += total_price 
                print(f"{quantity}x {item_name} @ RM{unit_price:.2f} each = RM{total_price:.2f}")
            print(f"Total for all item(s) is RM{total_sum:.2f}")
            
    def remove_from_cart(self, item_name, quantity):
        found_items = [cart_item for cart_item in self.items if item_name.lower() == cart_item['item'].name.lower()]
        if found_items:
            cart_item = found_items[0]
            if cart_item['quantity'] > quantity:
                cart_item['quantity'] -= quantity
                print(f"Removed {quantity} {item_name}(s) from the cart.")
            elif cart_item['quantity'] == quantity:
                self.items.remove(cart_item)
                print(f"Removed all {item_name}(s) from the cart.")
            else:
                print(f"Cannot remove {quantity} {item_name}(s). Not enough quantity in cart.")
        else:
            print(f"{item_name} is not in the cart.")


    def calculate_total(self):
        return sum(cart_item['quantity'] * cart_item['item'].price for cart_item in self.items)

    def clear_cart(self):
        self.items = []
        
        
#for delivery info
class DeliveryDetails:
    def __init__(self,transactions_file, address=None, phone=None, delivery_date=None):
        self.address = address if address is not None else {}   #assign the object into set{} to carry values
        self.phone = phone if phone is not None else {}
        self.tracking_id = {}
        self.transactions = {}
        self.transactions_file = transactions_file

        ##set default dates if user didnt required
    def preferred_delivery_date(self):
 
        while True:
            delivery_date = input("Enter preferred delivery date (YYYY-MM-DD)(or press enter to skip): ")
            if not delivery_date:
        # Assume this is your date
                delivery_date = datetime.datetime.now()


        # Add 3 days to your date
                new_date = delivery_date + datetime.timedelta(days=3)
                delivery_date = new_date
                break
            try:
                delivery_date = datetime.datetime.strptime(delivery_date, "%Y-%m-%d").date()
                break
            except ValueError:  #wrong format
                print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
                

    def search_delivery_status(self, user, trackingID):
    # Load the transactions
        with open('transactions.csv', 'r') as file:
            reader = csv.reader(file)
            transactions = list(reader)
    #looping + selection for checking the tracking id to avoid list index out of range error
        for i, transaction in enumerate(transactions):
            if len(transaction) >= 10 and transaction[8] == trackingID:
                status = transaction[9]
                print(f"Delivery status for tracking ID {trackingID}: {status}")
                return status

        print(f"Delivery status for tracking ID {trackingID} not found.")
        return None


    def update_status(self, trackingID, new_status):
        self.trackingID = trackingID
        self.new_status = new_status
        transaction_found = False  

        with open('transactions.csv', 'r') as file:
            reader = csv.reader(file)
            transactions = list(reader)

        for i, transaction in enumerate(transactions):
            if len(transaction) >= 10:
                if transaction[8] == trackingID:
                    print("\n=== Update Status ===")
                    print(f"Previous Status: {transaction[9]}")
                    transaction[9] = new_status
                    print(f"Current Status: {new_status}")
                    transaction_found = True
                    break

        if not transaction_found:
            print(f"Invalid tracking ID: {trackingID}")

        with open(self.transactions_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transactions)

        if transaction_found:
            print("Status updated successfully.")

class POS:
    def __init__(self):
        self.items = []
        self.transactions = {}
        self.load_items()
        self.load_transactions()
        self.delivery_details={}
        self.delivery_detail = DeliveryDetails(transactions_file='your_transactions_file')
        
        self.transaction_id = 0
        self.category_images = {
            "Household": os.path.join('images', 'Household.jpeg'),
            "Education": os.path.join('images', 'Education.jpeg'),
            "Electronic": os.path.join('images', 'Electronic.jpeg'),
            "Health": os.path.join('images', 'Health.jpeg'),
            "Beauty": os.path.join('images', 'Beauty.jpeg'),
             "Toys": os.path.join('images', 'Toys.jpeg'),
            "Sports": os.path.join('images', 'Sport.jpeg'), 
        } ##access images from the path 
        self.promotion_codes = {
            'DIS10': 0.1,  # 10% discount
            'DIS15': 0.15,  # 15% discount
            # Add more promotion codes and their corresponding discounts here
        }
    def discount(self, code):
        return self.promotion_codes.get(code, 0)
    def load_items(self):
        try:
            with open('items.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                self.items = [Item(row[0], row[1], row[2], int(row[3]), float(row[4])) for row in reader if len(row) >= 5]
        except FileNotFoundError:
            print("The items.csv file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_items(self):
        with open('items.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Category', 'Subcategory', 'Item', 'Quantity', 'Price'])
            for item in self.items:
                writer.writerow([item.category, item.subcategory, item.name, item.quantity, item.price])

    def search_item(self, search_name):
        found_items = [item for item in self.items if search_name.lower() in item.name.lower()]
        if found_items:
            for i, item in enumerate(found_items):
                print(f"{i + 1}. {item.name} (Qty: {item.quantity}, Price: RM{item.price:.2f})")
            return found_items
        else:
            print("No results found.")
            return []

    def view_items_by_category(self):
        categories = {}
        category_images = {}  ##provide the empty dict to save images

        for item in self.items:
            categories.setdefault(item.category, {}).setdefault(item.subcategory, []).append(item)

        while True:
            print("\nAvailable Categories:")
            for i, category in enumerate(categories.keys()):
                print(f"{i + 1}. {category}")
            print(f"{len(categories) + 1}. Go Back")

            try:
                category_choice = int(input("Select a category: "))
                if category_choice == len(categories) + 1:
                    break
                selected_category = list(categories.keys())[category_choice - 1]
                
                # Display the image for the selected category
                #same name of images as the selected_category
                if selected_category in self.category_images:
                    image_path = self.category_images[selected_category]
                    image = Image.open(image_path)
                    display(image)

                print(f"\nSubcategories in {selected_category}:")
                for i, subcategory in enumerate(categories[selected_category].keys()):
                    print(f"{i + 1}. {subcategory}")
                print(f"{len(categories[selected_category]) + 1}. Go Back")

                subcategory_choice = int(input("Select a subcategory: "))
                if subcategory_choice == len(categories[selected_category]) + 1: #automatic assume the choice from length of the file  
                    continue
                selected_subcategory = list(categories[selected_category].keys())[subcategory_choice - 1]

                print(f"\nItems in {selected_subcategory} ({selected_category}):")
                for item in categories[selected_category][selected_subcategory]:
                    print(f"{item.name.ljust(20)} (Qty: {str(item.quantity).rjust(3)}, Price: RM{item.price:7.2f})")

            except (ValueError, IndexError):
                print("Invalid choice. Please select a valid option.")

    def inventory_alerts(self):
        print("\nInventory Alerts:")
        header = f"{'Item Name'.ljust(15)} | {'Stock Remaining'.rjust(15)}" #aligment adjustment for left and right
        print(header)
        print('-' * len(header))
        low_stock_items = [item for item in self.items if item.quantity < 5]

        if low_stock_items:
            for item in low_stock_items:
                print(f"{item.name.ljust(15)} | {str(item.quantity).rjust(15)} left")
        else:
            print("No items are low in stock.")
        print("-" * len(header))
        print("Inventory check complete.")

    def update_inventory(self, cart):
        for cart_item in cart.items:
            for item in self.items:
                if item.name == cart_item['item'].name:
                    item.quantity -= cart_item['quantity']
        self.save_items()  #invoke ,update and assign back the values 
        
    #generate ids    
    def generate_transaction_id(self):
    # Generate a unique transaction ID
        while True:
            transaction_id = f'TSX{random.randint(100, 9999)}'
            tracking_id = f'TK{random.randint(100, 9999)}'
            if transaction_id not in self.transactions:
                return transaction_id
    def generate_tracking(self):
   # Generate a unique tracking ID
        while True:
            tracking_id = f'TK{random.randint(100, 9999)}'
            if tracking_id not in self.transactions:
                return tracking_id

    def checkout(self, user_id, cart):
        if cart.is_empty():  #it will skipped if cart is not empty
            print("Your cart is empty. Add items before proceeding to checkout.")
            return
        transaction_id = self.generate_transaction_id()
        total_sum = cart.calculate_total()
        cart.view_cart()
        tracking_number=self.generate_tracking()
        print("Please follow the instructions below to complete your payment.")
        phone_number = input("Enter phone number: ")
        delivery_address = input("Enter delivery address: ")
        delivery_date=self.delivery_detail.preferred_delivery_date()
        promo_code = input("Enter promotion code (or press enter to skip): ")
        while promo_code and promo_code not in self.promotion_codes:
            print("Invalid promotion code.")
            promo_code = input("Please enter your promotion code again (or press enter to skip): ")

        discount = self.discount(promo_code)
        total_sum -= total_sum * discount


        if self.process_payment(total_sum):
            self.update_inventory(cart)
            receipt = self.generate_receipt(user_id,cart, total_sum)
            self.save_transaction(user_id, cart, total_sum, delivery_address, phone_number, delivery_date, transaction_id,tracking_number) #invole all requires arguments into the save_transactions and save into csv file
            cart.clear_cart()
            self.load_transactions()
            print(f"Checkout successful.Thank you for your purchase!")
            print(receipt)

        else:
            print("Checkout canceled.")

        
    def process_payment(self, total):
        print(f"Your total is RM{total:.2f}")
        print("Payment methods:")
        print("1. Cash")
        print("2. Credit Card")
        while True:
            try:
                payment_method = int(input("Select payment method: "))
                if payment_method in [1, 2]:
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
            except ValueError:
                print("Invalid choice. Please select a valid option.")

        if payment_method == 1:
            while True:
                try:
                    cash_received = float(input("Enter cash amount: RM"))
                    if cash_received >= total:
                        change = cash_received - total
                        print(f"Change: RM{change:.2f}")
                        break
                    else:
                        print("Insufficient amount. Please provide enough cash.")
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
        elif payment_method == 2:
            card_number = input("Enter credit card number: ")
            print("Processing credit card payment...")
            # Simulating payment processing delay
            import time
            time.sleep(2)
            print("Credit card payment successful.")
        return True

#######################################################
    def generate_receipt(self, user_id, cart, total_sum):
        receipt = []
        user_transactions = [trans for trans in self.transactions.values() if str(trans['user_id']) == user_id] #using loaded data.
        receipt.append("===== Transaction Receipt =====")
        receipt.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        receipt.append("--------------------------------")
        receipt.append("Qty | Item Name          |  Unit Price | Total Price")
        receipt.append("--------------------------------")
        for cart_item in cart.items:
            item_name = cart_item['item'].name
            unit_price = cart_item['item'].price
            quantity = cart_item['quantity']
            total_price = unit_price * quantity
            receipt.append(f"{str(quantity).rjust(3)} | {item_name.ljust(18)} | RM{unit_price:9.2f} | RM{total_price:10.2f}")
        receipt.append("--------------------------------")
        if user_transactions:
            transaction = user_transactions[0]  # Assuming only one transaction for the given user ID
            receipt.append(f"Transaction ID: {transaction['transaction_id']}")
            receipt.append(f"Tracking ID: {transaction['tracking_number']}")
        receipt.append(f"Total Amount Due: RM{total_sum:.2f}")
        receipt.append("===== Thank you for shopping with us! =====")
    
        return "\n".join(receipt)

    
####save into csv file
    def save_transaction(self, user_id, cart, total_sum, delivery_address, phone_number, delivery_date, transaction_id, tracking_number):
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        status = 'Pending'

        items = [{'name': cart_item['item'].name, 'quantity': cart_item['quantity'], 'price': cart_item['item'].price} for cart_item in cart.items]
        items_str = '; '.join([f"{item['name']} (Quantity: {item['quantity']}, Price: {item['price']:.2f})" for item in items])

        transaction = {
            'transaction_id': transaction_id,
            'user_id': user_id,
            'items': items_str,
            'total': total_sum,
            'date_time': date_time,
            'delivery_address': delivery_address,
            'phone_number': phone_number,
            'delivery_date': delivery_date,
            'tracking_number': tracking_number,
            'status': status
        }

        with open('transactions.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if os.stat('transactions.csv').st_size == 0:
                writer.writerow(['Transaction ID', 'User ID', 'Date Time', 'Items', 'Total', 'Delivery Address', 'Phone Number', 'Delivery Date', 'Tracking Number', 'Status'])
            writer.writerow([transaction_id, user_id, date_time, items_str, total_sum, delivery_address, phone_number, delivery_date, tracking_number, status])

    def load_transactions(self):
        transactions={}
        if os.path.exists('transactions.csv'):
            with open('transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transaction_id = row['Transaction ID']
                    items = [dict(zip(['name', 'quantity', 'price'], item.split(':'))) for item in row['Items'].split(';')]
                    for item in items:
                        self.transactions[transaction_id] = {
                        'transaction_id': row['Transaction ID'],
                        'user_id': row['User ID'],
                        'date_time': row['Date Time'],
                        'items': items,
                        'total': float(row['Total']),
                        'delivery_address': row['Delivery Address'],
                        'phone_number': row['Phone Number'],
                        'delivery_date': row['Delivery Date'],
                        'tracking_number': row['Tracking Number'],
                        'status': row['Status']
                    }
        else:
            print("The transactions.csv file was not found.")
        return transactions 

    def view_user_transactions(self, user_id):
        print(f"Transaction history for user: {user_id}")

    # Filter transactions for the given user_id
        user_transactions = [trans for trans in self.transactions.values() if str(trans['user_id']) == user_id] #using loaded data.

        if user_transactions:
            for transaction in user_transactions:
                print(f"Date Time: {transaction['date_time']}")
                print("Items:")

                for item in transaction['items']:
                    if isinstance(item, dict) and all(key in item for key in ['name', 'quantity', 'price']): #parsing the items
                        price = float(item['price']) if isinstance(item['price'], str) and item['price'].replace('.', '', 1).isdigit() else item['price']
                        price_str = f"RM{price:.2f}" if isinstance(price, float) else f"RM{price}"
                        print(f" - {item['name']} (Quantity: {item['quantity']}, Price: {price_str})")
                    else:
                        print(f" - {item}")

                print(f"Total: RM{transaction['total']:.2f}")
                print(f"Delivery Address: {transaction['delivery_address']}")
                print(f"Phone Number: {transaction['phone_number']}")
                print(f"Delivery Date: {transaction['delivery_date']}")
                print(f"Transaction ID: {transaction['transaction_id']}")
                print(f"Tracking ID: {transaction['tracking_number']}")
                print("--------------------------------")
        else:
            print("No transactions found for this user.")

    
        
    def update_personal_details(self, username):
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            users = list(reader)

        for user in users:
            if user[0] == username:
                print("\n=== Update Personal Details ===")
                new_address = input(f"Current address: {user[2]}\nNew address: ")
                new_phone = input(f"Current phone number: {user[3]}\nNew phone number: ")
                user[2] = new_address if new_address else user[2]
                user[3] = new_phone if new_phone else user[3]
                break

        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)

        print("Personal details updated successfully.")


        
#inheritance from the parent class POS to access the load_transaction function
class ReportGenerator(POS):
    def __init__(self, transactions_file):
        super().__init__()
        self.transactions_file = transactions_file
        self.transactions = self.load_transactions()  #is to make sure the transaction will always be accessed and update during access the transaction csv file 
        
    def generate_total_sales_report(self):
        try:
            total_sales = 0
            with open('transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        total_sales += float(row['Total'])
                    except ValueError:
                        pass
            print(f"Total Sales for the Month: RM{total_sales:.2f}")
        except FileNotFoundError:
            # Fix: Use actual filename instead of undefined variable
            print("File 'transactions.csv' not found.")
        except KeyError:
            # Fix: Update error message to match actual file
            print("Column 'Total' not found in transactions.csv.")
    


    def generate_top_sales_report(self):
        sales_data = {}

        with open('transactions.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                items_string = row['Items']
                items = items_string.split('; ')
                for item_string in items:
                    #using try and except to test and assign the items' row into single object
                    try:
                        #separate the items if they joint tgt based on quantity and split it by price to display the single item and its price
                        item_parts = item_string.split(' (Quantity: ')
                        item_name = item_parts[0]
                        quantity_price_parts = item_parts[1].rstrip(')').split(', Price: ')
                        quantity = int(quantity_price_parts[0])
                        price = float(quantity_price_parts[1])

                        if item_name in sales_data:
                            sales_data[item_name]['quantity'] += quantity
                            sales_data[item_name]['total'] += quantity * price
                        else:
                            sales_data[item_name] = {'quantity': quantity, 'total': quantity * price}
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing item: {item_string}, Error: {e}")
                        continue
#by using sorted()  to arrange the top sales item
        sorted_sales_data = sorted(sales_data.items(), key=lambda x: x[1]['total'], reverse=True)

        print("\nTop Sales Report:")
        print(f"{'Item Name'.ljust(20)} | {'Quantity Sold'.rjust(13)} | {'Total Sales (RM)'.rjust(15)}")
        print("-" * 50)
        for item_name, data in sorted_sales_data:
            print(f"{item_name.ljust(20)} | {str(data['quantity']).rjust(13)} | RM{data['total']:15.2f}")
        print("-" * 50)
        print("Top sales report generated successfully.")


def main():
    pos = POS()
    report = ReportGenerator('transactions.csv')
    user = 'example_user_id'
    delivery_details = DeliveryDetails('transactions.csv')
    
    while True:
        print("\n=== POS System Menu ===")
        print("1. Register User")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            user = login_user()
            if user:
                cart = Cart()
                while True:
                    print("\n=== POS User Menu ===")
                    print("1. View Items by Category")
                    print("2. Search for an Item")
                    print("3. Add Item to Cart")
                    print("4. View Cart")
                    print("5. Remove Item from Cart")
                    print("6. Checkout")
                    print("7. View Transaction History")
                    print("8. Check Delivery Status")
                    print("9. Update Personal Details")
                    print("10. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        pos.view_items_by_category()
                    elif user_choice == "2":
                        search_name = input("Enter item name to search: (or press enter to view all items)")
                        pos.search_item(search_name)
                    elif user_choice == "3":
                        search_name = input("Enter item name to add to cart: ")
                        found_items = pos.search_item(search_name)
                        if found_items:
                            try:
                                item_index = int(input("Enter the number of the item to add: ")) - 1
                                if 0 <= item_index < len(found_items):
                                    quantity = int(input("Enter the quantity to add: "))
                                    cart.add_to_cart(found_items[item_index], quantity)
                                else:
                                    print("Invalid item number.")
                            except ValueError:
                                print("Invalid input.")
                    elif user_choice == "4":
                        cart.view_cart()
                    elif user_choice == "5":
                        item_name = input("Enter the name of the item to remove from cart: ")
                        quantity = int(input("Enter the quantity to remove: "))  # Ask for the quantity
                        cart.remove_from_cart(item_name,quantity)
                    elif user_choice == "6":
                        pos.checkout(user, cart)
                    elif user_choice == "7":
                        pos.view_user_transactions(user)
                    elif user_choice == "8":
                        tracking_id = input("Enter the Tracking ID:")
                        status = delivery_details.search_delivery_status(user, tracking_id)
                    elif user_choice == "9":
                        pos.update_personal_details(user)
                    elif user_choice == "10":
                        rating()
                        break
                    else:
                        print("Invalid choice. Please select a valid option.")
        elif choice == "3":
            if admin_login():
                while True:
                    print("\n=== Admin Menu ===")
                    print("1. Inventory Alerts")
                    print("2. Delivery Status Update")
                    print("3. Generate Total Sales Report")
                    print("4. Generate Top Sales Report")
                    print("5. Logout")
                    admin_choice = input("Enter your choice: ")
                    if admin_choice == "1":
                        pos.inventory_alerts()
                    elif admin_choice == "2":
                        transaction_id = input("Enter the tracking number to update status: ")
                        new_status = input("Enter the new delivery status (Pending/Failed/Successful) :")
                        delivery_details.update_status(transaction_id, new_status)
                    elif admin_choice == "3":
                        report.generate_total_sales_report()
                    elif admin_choice == "4":
                        report.generate_top_sales_report()
                    elif admin_choice == "5":
                        print("Logout Successfully")
                        break
                    else:
                        print("Invalid choice. Please select a valid option.")
        elif choice == "4":
            print("Exiting POS system.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

            
if __name__ == "__main__":
    main()