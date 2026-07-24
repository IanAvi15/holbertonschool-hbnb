from app import create_app
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='admin@hbnb.io').first()
    print("User found:", user)
    print("Password hash:", user.password if user else None)
    if user:
        print("Password check:", user.verify_password('AdminPass123'))
