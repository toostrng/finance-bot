from sqlalchemy.orm import Session
from models import User, Wallet, IncomeSource, ExpenseCategory, Transaction
from datetime import datetime, timedelta
from typing import List, Optional
import json

class DatabaseManager:
    def __init__(self, db: Session):
        self.db = db
    
    # User operations
    def get_or_create_user(self, telegram_id: int, username: str = None, first_name: str = None, last_name: str = None) -> User:
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def get_user(self, telegram_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()
    
    def update_user_currency(self, telegram_id: int, currency: str) -> bool:
        user = self.get_user(telegram_id)
        if user:
            user.default_currency = currency
            self.db.commit()
            return True
        return False
    
    # Wallet operations
    def create_wallet(self, user_id: int, name: str, currency: str) -> Wallet:
        wallet = Wallet(user_id=user_id, name=name, currency=currency)
        self.db.add(wallet)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet
    
    def get_user_wallets(self, user_id: int) -> List[Wallet]:
        return self.db.query(Wallet).filter(Wallet.user_id == user_id, Wallet.is_active == True).all()
    
    def update_wallet_balance(self, wallet_id: int, amount: float) -> bool:
        wallet = self.db.query(Wallet).filter(Wallet.id == wallet_id).first()
        if wallet:
            wallet.balance += amount
            self.db.commit()
            return True
        return False
    
    def delete_wallet(self, wallet_id: int, user_id: int) -> bool:
        wallet = self.db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user_id).first()
        if wallet:
            wallet.is_active = False
            self.db.commit()
            return True
        return False
    
    # Income source operations
    def create_income_source(self, user_id: int, name: str, description: str = None) -> IncomeSource:
        income_source = IncomeSource(user_id=user_id, name=name, description=description)
        self.db.add(income_source)
        self.db.commit()
        self.db.refresh(income_source)
        return income_source
    
    def get_user_income_sources(self, user_id: int) -> List[IncomeSource]:
        return self.db.query(IncomeSource).filter(IncomeSource.user_id == user_id, IncomeSource.is_active == True).all()
    
    def delete_income_source(self, source_id: int, user_id: int) -> bool:
        source = self.db.query(IncomeSource).filter(IncomeSource.id == source_id, IncomeSource.user_id == user_id).first()
        if source:
            source.is_active = False
            self.db.commit()
            return True
        return False
    
    # Expense category operations
    def create_expense_category(self, user_id: int, name: str, description: str = None, color: str = "#3B82F6", icon: str = "💰") -> ExpenseCategory:
        category = ExpenseCategory(
            user_id=user_id, 
            name=name, 
            description=description, 
            color=color, 
            icon=icon
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_user_expense_categories(self, user_id: int) -> List[ExpenseCategory]:
        return self.db.query(ExpenseCategory).filter(ExpenseCategory.user_id == user_id, ExpenseCategory.is_active == True).all()
    
    def delete_expense_category(self, category_id: int, user_id: int) -> bool:
        category = self.db.query(ExpenseCategory).filter(ExpenseCategory.id == category_id, ExpenseCategory.user_id == user_id).first()
        if category:
            category.is_active = False
            self.db.commit()
            return True
        return False
    
    # Transaction operations
    def create_transaction(self, user_id: int, wallet_id: int, transaction_type: str, amount: float, 
                          currency: str, description: str = None, date: datetime = None,
                          income_source_id: int = None, expense_category_id: int = None) -> Transaction:
        if date is None:
            date = datetime.utcnow()
        
        transaction = Transaction(
            user_id=user_id,
            wallet_id=wallet_id,
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            description=description,
            date=date,
            income_source_id=income_source_id,
            expense_category_id=expense_category_id
        )
        
        self.db.add(transaction)
        
        # Update wallet balance
        if transaction_type == 'income':
            self.update_wallet_balance(wallet_id, amount)
        else:
            self.update_wallet_balance(wallet_id, -amount)
        
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def get_user_transactions(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.user_id == user_id)\
                   .order_by(Transaction.date.desc())\
                   .limit(limit).offset(offset).all()
    
    def get_transactions_by_period(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Transaction]:
        return self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).order_by(Transaction.date.desc()).all()
    
    def delete_transaction(self, transaction_id: int, user_id: int) -> bool:
        transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()
        if transaction:
            # Revert wallet balance
            if transaction.transaction_type == 'income':
                self.update_wallet_balance(transaction.wallet_id, -transaction.amount)
            else:
                self.update_wallet_balance(transaction.wallet_id, transaction.amount)
            
            self.db.delete(transaction)
            self.db.commit()
            return True
        return False
    
    # Analytics and reports
    def get_user_summary(self, user_id: int, period_days: int = 30) -> dict:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=period_days)
        
        transactions = self.get_transactions_by_period(user_id, start_date, end_date)
        
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expense = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        
        # Group by category
        expenses_by_category = {}
        for t in transactions:
            if t.transaction_type == 'expense' and t.expense_category:
                cat_name = t.expense_category.name
                if cat_name not in expenses_by_category:
                    expenses_by_category[cat_name] = 0
                expenses_by_category[cat_name] += t.amount
        
        # Group by income source
        income_by_source = {}
        for t in transactions:
            if t.transaction_type == 'income' and t.income_source:
                source_name = t.income_source.name
                if source_name not in income_by_source:
                    income_by_source[source_name] = 0
                income_by_source[source_name] += t.amount
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_income': total_income - total_expense,
            'expenses_by_category': expenses_by_category,
            'income_by_source': income_by_source,
            'transaction_count': len(transactions)
        }
    
    def get_wallet_balances(self, user_id: int) -> List[dict]:
        wallets = self.get_user_wallets(user_id)
        return [
            {
                'id': wallet.id,
                'name': wallet.name,
                'currency': wallet.currency,
                'balance': wallet.balance
            }
            for wallet in wallets
        ] 