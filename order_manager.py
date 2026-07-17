# Order Management Module
from datetime import datetime
from database import db, Order, OrderItem, Product, Delivery, User
import uuid

class OrderManager:
    """Handle all order-related operations"""
    
    @staticmethod
    def create_order(user_id, items_data):
        """
        Create a new order
        items_data: list of {'product_id': id, 'quantity': qty}
        """
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Calculate total
        total_amount = 0
        for item in items_data:
            product = Product.query.get(item['product_id'])
            if product:
                total_amount += product.price * item['quantity']
        
        # Create order
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            status='pending',
            total_amount=total_amount
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order items
        for item in items_data:
            product = Product.query.get(item['product_id'])
            if product:
                order_item = OrderItem(
                    id=str(uuid.uuid4()),
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item['quantity'],
                    price=product.price
                )
                db.session.add(order_item)
        
        db.session.commit()
        return order
    
    @staticmethod
    def mark_as_delivered(order_id, delivery_content=''):
        """Mark order as delivered"""
        order = Order.query.get(order_id)
        if not order:
            return False
        
        order.status = 'delivered'
        order.updated_at = datetime.utcnow()
        
        # Create delivery record
        delivery = Delivery(
            id=str(uuid.uuid4()),
            order_id=order_id,
            delivery_content=delivery_content,
            is_delivered=True,
            delivered_at=datetime.utcnow()
        )
        db.session.add(delivery)
        db.session.commit()
        return True
    
    @staticmethod
    def auto_deliver_order(order_id, delivery_content):
        """Auto-deliver digital product"""
        return OrderManager.mark_as_delivered(order_id, delivery_content)
    
    @staticmethod
    def get_user_orders(user_id):
        """Get all user orders"""
        return Order.query.filter_by(user_id=user_id).order_by(
            Order.created_at.desc()
        ).all()
    
    @staticmethod
    def get_order_details(order_id):
        """Get detailed order information"""
        order = Order.query.get(order_id)
        if not order:
            return None
        
        return {
            'order': order,
            'items': OrderItem.query.filter_by(order_id=order_id).all(),
            'payment': order.payment,
            'delivery': Delivery.query.filter_by(order_id=order_id).first()
        }
    
    @staticmethod
    def cancel_order(order_id):
        """Cancel an order"""
        order = Order.query.get(order_id)
        if not order:
            return False
        
        order.status = 'cancelled'
        order.updated_at = datetime.utcnow()
        db.session.commit()
        return True
    
    @staticmethod
    def get_pending_orders():
        """Get all pending orders"""
        return Order.query.filter_by(status='pending').all()
