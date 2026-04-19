from models import User, db
admin = User(username='shriyans')
admin.set_password('paka')
db.session.add(admin)
db.session.commit()
print('Admin created!')
exit()