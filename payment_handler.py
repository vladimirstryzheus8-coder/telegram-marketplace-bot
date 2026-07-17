
# Payment System Module
from datetime import datetime
from database import db, Payment, WalletTransaction, Order, User
import uuid

class PaymentHandler:
    """Handle all payment-related operations"""
    
    @staticmethod
    def create_payment(user_id, order_id, amount, payment_type='opay', receipt_url=None):
        """Create a new payment record"""
        payment = Payment(
            id=str(uuid.uuid4()),
            user_id=user_id,
            order_id=order_id,
            amount=amount,
            payment_type=payment_type,
            status='pending',
            receipt_url=receipt_url
        )
        db.session.add(payment)
        db.session.commit()
        return payment
    
    @staticmethod
    def approve_payment(payment_id, notes=''):
        """Approve a pending payment"""
        payment = Payment.query.get(payment_id)
        if not payment:
            return False
        
        payment.status = 'approved'
        payment.notes = notes
        payment.updated_at = datetime.utcnow()
        
        # Update order status
        order = Order.query.get(payment.order_id)
        order.status = 'paid'
        
        # Create wallet transaction
        transaction = WalletTransaction(
            id=str(uuid.uuid4()),
            user_id=payment.user_id,
            amount=payment.amount,
            transaction_type='payment_approved',
            status='completed',
            reference=payment.id,
            description=f"Payment approved for order {order.order_number}"
        )
        
        db.session.add(transaction)
        db.session.commit()
        return True
    
    @staticmethod
    def reject_payment(payment_id, notes='Payment rejected by admin'):
        """Reject a pending payment"""
        payment = Payment.query.get(payment_id)
        if not payment:
            return False
        
        payment.status = 'rejected'
        payment.notes = notes
        payment.updated_at = datetime.utcnow()
        
        # Update order status
        order = Order.query.get(payment.order_id)
        order.status = 'cancelled'
        
        db.session.commit()
        return True
    
    @staticmethod
    def add_wallet_funds(user_id, amount, reference='', description=''):
        """Add funds to user wallet"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        user.wallet_balance += amount
        
        transaction = WalletTransaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=amount,
            transaction_type='deposit',
            status='completed',
            reference=reference,
            description=description or 'Wallet deposit'
        )
        
        db.session.add(transaction)
        db.session.commit()
        return True
    
    @staticmethod
    def deduct_wallet_balance(user_id, amount, description=''):
        """Deduct from user wallet"""
        user = User.query.get(user_id)
        if not user or user.wallet_balance < amount:
            return False
        
        user.wallet_balance -= amount
        
        transaction = WalletTransaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=amount,
            transaction_type='purchase',
            status='completed',
            description=description or 'Purchase'
        )
        
        db.session.add(transaction)
        db.session.commit()
        return True
    
    @staticmethod
    def get_pending_payments():
        """Get all pending payments"""
        return Payment.query.filter_by(status='pending').all()
    
    @staticmethod
    def get_user_transactions(user_id, limit=50):
        """Get user transaction history"""
        return WalletTransaction.query.filter_by(user_id=user_id).order_by(
            WalletTransaction.created_at.desc()
        ).limit(limit).all()
