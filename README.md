# social-network

### Installation

Clone the repository
```
git clone https://github.com/akushyn/social-network.git
```

Install project dependencies
```
cd social-network
pip3 install -r requirements.txt
```

### Setup database

Install Postgres from official site.


### Flask-SQLAlchemy

Sample how to create model:

```
from app import db


class User(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)   
```

Query all objects
```
from app.models import User

# get list of all users in User model
users = db.session.query(User).all()

# or above equal to this 
users = User.query.all()
```

Get specific object
```
user_id = 1
user = User.get(user_id)
```

Get first object from query
```
first_user = db.session.query(User).first()
```

Get specific object, filters
```
# select user with id = 5
# below different ways to achieve selection

user_id = 5
user = db.session.query(User).get(user_id)   
user = db.session.query(User).filter(User.id == user_id).first()
user = db.session.query(User).filter_by(id=user_id).first()
user = User.query.filter(User.id == user_id).first()
user = User.query.filter_by(id=user_id).first()
```

Delete specific object
```
# delete a user by id
user_to_delete = db.session.query(User).filter_by(id=1).first()
db.session.delete(user_to_delete)
db.session.commit()

# delete a user by username
user_to_delete = session.query(User).filter_by(username='akushyn').first()
session.delete(user_to_delete)
session.commit()
```
More details see in [SQLAlchemy Documentation](https://www.sqlalchemy.org/)

### Flask-Migrate

Initialize migrations
```
flask db init
```

Create db migration: 
```
flask db migrate
``` 
or
```
flask db migrate -m 'add short message'
```

Upgrade database to head revision
```
flask db upgrade
```

Downgrade database revision
```
flask db downgrade
```
More details see in [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/en/latest/#)

### CLI commands

Generate `n` fake users
```
cd social-network
flask fake users 5
```