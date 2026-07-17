# Statistics and Reporting Module
from database import db, User, Order, Payment, Product, Category, WalletTransaction
from sqlalchemy import func
from datetime import datetime, timedelta

class Statistics:
    """Generate marketplace statistics"""
    
    @staticmethod
    def get_dashboard_stats():
        """Get main dashboard statistics"""
        return {
            'total_users': User.query.count(),
            'total_orders': Order.query.count(),
            'pending_payments': Payment.query.filter_by(status='pending').count(),
            'approved_payments': Payment.query.filter_by(status='approved').count(),
            'total_revenue': db.session.query(func.sum(Order.total_amount)).scalar() or 0,
            'total_products': Product.query.count(),
            'total_categories': Category.query.count()
        }
    
    @staticmethod
    def get_daily_revenue(days=30):
        """Get daily revenue for last N days"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.session.query(
            func.date(Order.created_at).label('date'),
            func.sum(Order.total_amount).label('revenue'),
            func.count(Order.id).label('orders')
        ).filter(
            Order.created_at >= start_date,
            Order.status == 'paid'
        ).group_by(func.date(Order.created_at)).all()
        
        return results
    
    @staticmethod
    def get_top_products(limit=10):
        """Get best-selling products"""
        results = db.session.query(
            Product.name,
            func.sum(OrderItem.quantity).label('total_sold'),
            func.sum(Order.total_amount).label('revenue')
        ).join(OrderItem).join(Order).filter(
            Order.status == 'paid'
        ).group_by(Product.id).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(limit).all()
        
        return results
    
    @staticmethod
    def get_user_statistics():
        """Get user statistics"""
        return {
            'total_users': User.query.count(),
            'users_with_orders': db.session.query(func.count(func.distinct(Order.user_id))).scalar() or 0,
            'avg_wallet_balance': db.session.query(func.avg(User.wallet_balance)).scalar() or 0,
            'total_wallet_balance': db.session.query(func.sum(User.wallet_balance)).scalar() or 0
        }
    
    @staticmethod
    def get_payment_statistics():
        """Get payment statistics"""
        return {
            'total_payments': Payment.query.count(),
            'approved': Payment.query.filter_by(status='approved').count(),
            'pending': Payment.query.filter_by(status='pending').count(),
            'rejected': Payment.query.filter_by(status='rejected').count(),
            'opay_payments': Payment.query.filter_by(payment_type='opay').count(),
            'wallet_payments': Payment.query.filter_by(payment_type='wallet').count(),
            'total_amount': db.session.query(func.sum(Payment.amount)).scalar() or 0
        }

from database import OrderItem
