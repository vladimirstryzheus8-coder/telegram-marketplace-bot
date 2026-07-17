"""Database initialization script"""
from flask import Flask
from database import db, User, Category, Product
from config import config
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if data already exists
        if Category.query.first():
            print("⚠️ Database already contains data. Skipping sample data insertion.")
            return
        
        # Create sample categories
        categories_data = [
            {'name': 'Software & Apps', 'description': 'Digital software and applications', 'icon': '💻'},
            {'name': 'E-Books', 'description': 'Digital books and publications', 'icon': '📚'},
            {'name': 'Courses', 'description': 'Online courses and training', 'icon': '🎓'},
            {'name': 'Music & Audio', 'description': 'Digital music and audio files', 'icon': '🎵'},
            {'name': 'Templates', 'description': 'Design templates and graphics', 'icon': '🎨'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(
                id=str(uuid.uuid4()),
                name=cat_data['name'],
                description=cat_data['description'],
                icon=cat_data['icon']
            )
            categories.append(category)
            db.session.add(category)
        
        db.session.commit()
        print(f"✅ Created {len(categories)} categories")
        
        # Create sample products
        products_data = [
            {
                'category': categories[0],
                'name': 'Premium VPN Access',
                'description': '1 Year Premium VPN subscription with unlimited bandwidth',
                'price': 2999.99,
                'stock': 100,
                'delivery_type': 'auto'
            },
            {
                'category': categories[1],
                'name': 'Python Programming Guide',
                'description': 'Complete guide to Python programming for beginners',
                'price': 499.99,
                'stock': 50,
                'delivery_type': 'auto'
            },
            {
                'category': categories[2],
                'name': 'Web Development Masterclass',
                'description': 'Learn HTML, CSS, JavaScript, and React in 30 days',
                'price': 4999.99,
                'stock': 200,
                'delivery_type': 'auto'
            },
            {
                'category': categories[3],
                'name': 'Exclusive Music Pack',
                'description': '500+ Royalty-free music tracks for content creators',
                'price': 1999.99,
                'stock': 75,
                'delivery_type': 'auto'
            },
            {
                'category': categories[4],
                'name': 'UI/UX Design Templates',
                'description': '100+ Professional UI templates for web and mobile',
                'price': 999.99,
                'stock': 150,
                'delivery_type': 'auto'
            },
        ]
        
        for prod_data in products_data:
            product = Product(
                id=str(uuid.uuid4()),
                category_id=prod_data['category'].id,
                name=prod_data['name'],
                description=prod_data['description'],
                price=prod_data['price'],
                stock=prod_data['stock'],
                delivery_type=prod_data['delivery_type']
            )
            db.session.add(product)
        
        db.session.commit()
        print(f"✅ Created {len(products_data)} sample products")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\nYou can now run the bot and admin panel.")

if __name__ == '__main__':
    init_db()
