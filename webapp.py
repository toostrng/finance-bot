from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import get_db, create_tables
from database import DatabaseManager
from datetime import datetime, timedelta
import json
from config import Config

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Create database tables
create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user/<int:telegram_id>', methods=['GET', 'POST'])
def user_endpoint(telegram_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    if request.method == 'GET':
        user = db_manager.get_user(telegram_id)
        if user:
            return jsonify({
                'id': user.id,
                'telegram_id': user.telegram_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'default_currency': user.default_currency
            })
        return jsonify({'error': 'User not found'}), 404
    
    elif request.method == 'POST':
        data = request.get_json()
        user = db_manager.get_or_create_user(
            telegram_id=telegram_id,
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        return jsonify({
            'id': user.id,
            'telegram_id': user.telegram_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'default_currency': user.default_currency
        })

@app.route('/api/user/<int:telegram_id>/currency', methods=['PUT'])
def update_user_currency(telegram_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    data = request.get_json()
    currency = data.get('currency')
    
    if currency not in Config.SUPPORTED_CURRENCIES:
        return jsonify({'error': 'Unsupported currency'}), 400
    
    success = db_manager.update_user_currency(telegram_id, currency)
    if success:
        return jsonify({'message': 'Currency updated successfully'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/user/<int:telegram_id>/wallets', methods=['GET', 'POST'])
def wallets_endpoint(telegram_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'GET':
        wallets = db_manager.get_user_wallets(user.id)
        return jsonify([{
            'id': wallet.id,
            'name': wallet.name,
            'currency': wallet.currency,
            'balance': wallet.balance,
            'is_active': wallet.is_active
        } for wallet in wallets])
    
    elif request.method == 'POST':
        data = request.get_json()
        wallet = db_manager.create_wallet(
            user_id=user.id,
            name=data['name'],
            currency=data['currency']
        )
        return jsonify({
            'id': wallet.id,
            'name': wallet.name,
            'currency': wallet.currency,
            'balance': wallet.balance
        })

@app.route('/api/user/<int:telegram_id>/wallets/<int:wallet_id>', methods=['DELETE'])
def delete_wallet(telegram_id, wallet_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    success = db_manager.delete_wallet(wallet_id, user.id)
    if success:
        return jsonify({'message': 'Wallet deleted successfully'})
    return jsonify({'error': 'Wallet not found'}), 404

@app.route('/api/user/<int:telegram_id>/income-sources', methods=['GET', 'POST'])
def income_sources_endpoint(telegram_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'GET':
        sources = db_manager.get_user_income_sources(user.id)
        return jsonify([{
            'id': source.id,
            'name': source.name,
            'description': source.description,
            'is_active': source.is_active
        } for source in sources])
    
    elif request.method == 'POST':
        data = request.get_json()
        source = db_manager.create_income_source(
            user_id=user.id,
            name=data['name'],
            description=data.get('description')
        )
        return jsonify({
            'id': source.id,
            'name': source.name,
            'description': source.description
        })

@app.route('/api/user/<int:telegram_id>/income-sources/<int:source_id>', methods=['DELETE'])
def delete_income_source(telegram_id, source_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    success = db_manager.delete_income_source(source_id, user.id)
    if success:
        return jsonify({'message': 'Income source deleted successfully'})
    return jsonify({'error': 'Income source not found'}), 404

@app.route('/api/user/<int:telegram_id>/expense-categories', methods=['GET', 'POST'])
def expense_categories_endpoint(telegram_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'GET':
        categories = db_manager.get_user_expense_categories(user.id)
        return jsonify([{
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'color': category.color,
            'icon': category.icon,
            'is_active': category.is_active
        } for category in categories])
    
    elif request.method == 'POST':
        data = request.get_json()
        category = db_manager.create_expense_category(
            user_id=user.id,
            name=data['name'],
            description=data.get('description'),
            color=data.get('color', '#3B82F6'),
            icon=data.get('icon', '💰')
        )
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'color': category.color,
            'icon': category.icon
        })

@app.route('/api/user/<int:telegram_id>/expense-categories/<int:category_id>', methods=['DELETE'])
def delete_expense_category(telegram_id, category_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    success = db_manager.delete_expense_category(category_id, user.id)
    if success:
        return jsonify({'message': 'Expense category deleted successfully'})
    return jsonify({'error': 'Expense category not found'}), 404

@app.route('/api/user/<int:telegram_id>/transactions', methods=['GET', 'POST'])
def transactions_endpoint(telegram_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'GET':
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        transactions = db_manager.get_user_transactions(user.id, limit, offset)
        
        return jsonify([{
            'id': t.id,
            'wallet_id': t.wallet_id,
            'wallet_name': t.wallet.name,
            'transaction_type': t.transaction_type,
            'amount': t.amount,
            'currency': t.currency,
            'description': t.description,
            'date': t.date.isoformat(),
            'income_source_id': t.income_source_id,
            'income_source_name': t.income_source.name if t.income_source else None,
            'expense_category_id': t.expense_category_id,
            'expense_category_name': t.expense_category.name if t.expense_category else None,
            'expense_category_color': t.expense_category.color if t.expense_category else None,
            'expense_category_icon': t.expense_category.icon if t.expense_category else None
        } for t in transactions])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Parse date
        date_str = data.get('date')
        if date_str:
            try:
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                date = datetime.utcnow()
        else:
            date = datetime.utcnow()
        
        transaction = db_manager.create_transaction(
            user_id=user.id,
            wallet_id=data['wallet_id'],
            transaction_type=data['transaction_type'],
            amount=float(data['amount']),
            currency=data['currency'],
            description=data.get('description'),
            date=date,
            income_source_id=data.get('income_source_id'),
            expense_category_id=data.get('expense_category_id')
        )
        
        return jsonify({
            'id': transaction.id,
            'wallet_id': transaction.wallet_id,
            'transaction_type': transaction.transaction_type,
            'amount': transaction.amount,
            'currency': transaction.currency,
            'description': transaction.description,
            'date': transaction.date.isoformat()
        })

@app.route('/api/user/<int:telegram_id>/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(telegram_id, transaction_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    success = db_manager.delete_transaction(transaction_id, user.id)
    if success:
        return jsonify({'message': 'Transaction deleted successfully'})
    return jsonify({'error': 'Transaction not found'}), 404

@app.route('/api/user/<int:telegram_id>/summary', methods=['GET'])
def user_summary(telegram_id):
    db = next(get_db())
    db_manager = DatabaseManager(db)
    
    user = db_manager.get_user(telegram_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    period_days = request.args.get('period', 30, type=int)
    summary = db_manager.get_user_summary(user.id, period_days)
    wallet_balances = db_manager.get_wallet_balances(user.id)
    
    return jsonify({
        'summary': summary,
        'wallet_balances': wallet_balances
    })

@app.route('/api/currencies', methods=['GET'])
def get_currencies():
    return jsonify(Config.SUPPORTED_CURRENCIES)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000) 