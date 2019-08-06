#SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#SQL CONFIGURATION
engine = create_engine('postgresql://postgres:651596XY@localhost:5432/userdata')
db = scoped_session(sessionmaker(bind=engine))

user_login = 'maciek'
passw = 'adminex'

a = db.execute("SELECT * FROM users WHERE login = :login", {"login": user_login.lower()}).fetchall()[0]
print(a.id)
