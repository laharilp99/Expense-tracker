from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import userdb
from db import categorydb, categorywrite
from db import expensedb, categorydb
import json
from db import totalbalance,totalbalncedb
from db import expensedb,handledelete


app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return redirect(url_for('register'))  # Redirects to the 'register' route

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        user = userdb.find_user_by_userid(userid)

        if user:
            flash('Username already exists.')
        else:
            userdb.insert_user(userid, password)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        user = userdb.find_user_by_userid(userid)

        if user and user['password'] == password:
            session['user_id'] = user['slno']
            session['userid'] = user['userid']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')




@app.route('/category', methods=['GET', 'POST'])
def category():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        categorywrite.handle_category_form(request)

    categories = categorydb.get_all_categories()
    return render_template('category.html', categories=categories)




@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        totalbalncedb.handle_category_form(request)

    balance= totalbalance.get_balance()
   


    return render_template('totalbalance.html', balance=balance)



# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         category = request.form['category']
#         amountspent = request.form['amountspent']
#         if category and amountspent:
#             expensedb.insert_expense(category, int(amountspent),user)
#             flash("Expense added.")

#     categories = categorydb.get_all_categories()
#     recent_expenses = expensedb.get_recent_expenses()
#     summary = expensedb.get_expense_summary_by_category()
#     most_expensive_category=expensedb.get_most_used_category()
#     indivisual_data=expensedb.get_expense_summary_by_category_wihtout_groups()
#     mainbalance = totalbalance.get_main_balance()  # This is now just an int like 5000
   

#     # Calculate total spent
#     total_spent = sum(expense[1] for expense in summary) if summary else 0

#     chart_labels = [item[0] for item in summary]
#     chart_data = [item[1] for item in summary]

#     return render_template('dashboard.html',
#                            userid=session['userid'],
#                            categories=categories,
#                            recent_expenses=recent_expenses,
#                            summary=summary,
#                            mainbalance=mainbalance,
#                            most_expensive_category=most_expensive_category,
#                            total_spent=total_spent,
#                            indivisual_data=indivisual_data,
#                            chart_labels=json.dumps(chart_labels),
#                            chart_data=json.dumps(chart_data))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    print(session['userid'])

    if request.method == 'POST':
        # 🔁 Handle Deletion
        delete_id = request.form.get('slno')
        print("delete_id",delete_id)
        if delete_id:
            handledelete.handle_category_form(delete_id)
            flash("Entry deleted.", "info")
            return redirect(url_for('dashboard'))  # Refresh the page

        # 🧾 Handle New Expense
        category = request.form.get('category')
        amountspent = request.form.get('amountspent')
        if category and amountspent:
            expensedb.insert_expense(category, int(amountspent),session['userid'])
            flash("Expense added.")

    # 🔄 Load all required data
    categories = categorydb.get_all_categories()
    recent_expenses = expensedb.get_recent_expenses()
    summary = expensedb.get_expense_summary_by_category(session['userid'])
    most_expensive_category = expensedb.get_most_used_category(session['userid'])
    indivisual_data = expensedb.get_expense_summary_by_category_wihtout_groups(session['userid'])

    mainbalance = totalbalance.get_main_balance()

    total_spent = sum(expense[1] for expense in summary) if summary else 0
    chart_labels = [item[0] for item in summary]
    chart_data = [item[1] for item in summary]

    return render_template('dashboard.html',
                           userid=session['userid'],
                           categories=categories,
                           recent_expenses=recent_expenses,
                           summary=summary,
                           mainbalance=mainbalance,
                           most_expensive_category=most_expensive_category,
                           total_spent=total_spent,
                           indivisual_data=indivisual_data,
                           chart_labels=json.dumps(chart_labels),
                           chart_data=json.dumps(chart_data))




@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
