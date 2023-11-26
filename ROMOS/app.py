from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {
    'user1': {'username': 'user1', 'password': 'pass1'},
    # Add more users as needed
}
def load_inventory():
    inventory = {}
    with open('inventory.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = row['ItemID']
            inventory[item_id] = {
                'category': row['CategoryName'],
                'name': row['ItemName'],
                'sap_code': row['SapCode'],
                'short_code': row['ItemShortCode'],
                'short_code1': row['ItemShortCode1'],
                'description': row['ItemDescription'],
                'expose_to_online': row['ExposeToOnline'],
                'online_display_name': row['OnlineDisplayName'],
                'is_favorite': row['IsFavorite'],
                'base_price': float(row['ItemBasePrice']),
                'container_charge': float(row['ContainerCharge']),
                'zomato': row['Zomato'],
                'available': row['Available']
            }
    return inventory

inventory = load_inventory()

#@app.route('/')
#def index():
#    return render_template('index.html', inventory=inventory)

# Mock data for user accounts


# Shopping cart data
carts = {}

@app.route('/')
def index():
    return render_template('index.html', inventory=inventory)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    # Clear the user's shopping cart on logout
    username = request.args.get('username')
    if username in carts:
        del carts[username]
    return redirect(url_for('index'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    username = request.form['username']
    ItemID = request.form['ItemID']
    quantity = int(request.form['quantity'])
    
    if username not in carts:
        carts[username] = {}
        
    if ItemID in carts[username]:
        carts[username][ItemID] += quantity
    else:
        carts[username][ItemID] = quantity
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
