from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, HardwareItem
from users import User
from auth import init_login, setup_auth_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_login(app)
setup_auth_routes(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/inventory')
@login_required
def index():
    items = HardwareItem.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        new_item = HardwareItem(
        type=request.form['type'],
        model=request.form['model'],
        serial=request.form['serial'],
        location=request.form['location'],
        status=request.form['status'],
        custom_type_detail=request.form.get('custom_type_detail', None)
    )

        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html')
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    item = HardwareItem.query.get(item_id)
    if request.method == 'POST':
        item.type = request.form['type']
        item.model = request.form['model']
        item.serial = request.form['serial']
        item.location = request.form['location']
        item.status = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>')
@login_required
def delete_item(item_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    item = HardwareItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/stats')
@login_required
def stats():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    from collections import Counter
    items = HardwareItem.query.all()
    categories = [item.type for item in items]
    stats = dict(Counter(categories))
    return render_template('stats.html', stats=stats)

@app.route('/export_csv')
@login_required
def export_csv():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    import csv
    from flask import Response
    items = HardwareItem.query.all()
    def generate():
        data = ['ID,Type,Model,Serial,Location,Status\n']
        for item in items:
            row = f'{item.id},{item.type},{item.model},{item.serial},{item.location},{item.status}\n'
            data.append(row)
        return ''.join(data)
    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=hardware_inventory.csv"})

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    return render_template('admin.html')
