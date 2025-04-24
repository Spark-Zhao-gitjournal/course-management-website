from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, or_ #import for textual query
from sqlalchemy.sql import exists   #import for exists
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '84Br5667bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Person(db.Model):
    __tablename__ = 'Person'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable = False)
    notes = db.relationship('Notes', backref='author', lazy=True)

    def __repr__(self):
        return f"Person('{self.username}', '{self.email}')"

class Notes(db.Model):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable=False)

    def __repr__(self):
        return f"Notes('{self.title}', '{self.date_posted}')"

with app.app_context():
    db.create_all()

with app.app_context():
    # #Filtering in SQLAlchemy
    print('*******Filtering 1*******')
    user_details = db.session.query(Person).filter(Person.id == 2)
    print(user_details[0])
    for person in user_details:
        print(person.id, person.username, person.email)

    print('*******Filtering 2 with username containing ee*******')
    # person that has 'ee' in their name
    user_details = db.session.query(Person).filter(Person.username.like('%ee%'))
    for person in user_details:
        print(person.id, person.username, person.email)

    print('*******Filtering 3 with chaining*******')
    #chain multiple filters to create an AND effect
    user_details = db.session.query(Person).filter(Person.username.like('%student%')).filter(Person.email == 'student2@gmail.com')
    for person in user_details:
        print(person.id, person.username, person.email)

    #Counting in SQLAlchemy
    print('*******Counting*******')
    # SELECT Count(*)
    # FROM  person
    # WHERE id>3

    print(db.session.query(Person).filter(Person.id > 3).count())

    #order by in SQLAlchemy
    print('*******Order By*******')
    for person in db.session.query(Person).order_by(Person.id):
        print(person.username, person.email)

    # filtering in SQLAlchemy
    print('*******Filtering 4*******')
    r2 = db.session.query(Person).filter(Person.id>2)

    for person in r2:
        print(person.username)

    # IN operator 
    print('*******In Operator*******')
    # SELECT username
    # FROM  person
    # WHERE id IN (1, 2, 3)

    ids_to_select = ['1', '2', '3']
    r3 = db.session.query(Person).filter(Person.id.in_(ids_to_select)).all()
    for person in r3:
        print(person.username)

    # LIKE operator 
    r3 = db.session.query(Person).filter(Person.username.like('P%'))
    print('*******Like Method*******')
    for person in r3:
        print(person.username)

    # AND 
    print('*******AND*******')
    r4 = db.session.query(Person).filter(Person.username.like('P%'), Person.id.in_([1, 10]))
    for person in r4:
        print(person.username)

    # OR - needs an import
    print('*******OR*******')
    r4 = db.session.query(Person).filter(or_(Person.username.like('P%'), Person.username.like('S%')))
    for person in r4:
        print(person.username)

    # filtering using textual query SQLAlchemy - needs an import
    print('*******Filtering using textual query*******')
    r5 = db.session.query(Person).filter(text("id>2"))
    for person in r5:
        print(person.username)

    # join in SQLAlchemy
    print('*******Join*******')
    # SELECT Person.username, Notes.title
    # FROM  Notes LEFT JOIN Person 
    # WHERE Notes.person_id = Person.id

    results = db.session.query(Person, Notes).join(Notes).all()
    print(results)
    for person, note in results:
        print(person.username, note.title)

    # Another example with WHERE  in SQLAlchemy
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying-with-joins
    print('*******Another example with WHERE*******')
    r6 = db.session.query(Person, Notes).\
                filter(Person.id == Notes.id).\
                filter(Person.id > 1).\
                all()
    for person, note in r6:
        print(person.username, note.title)

    # Another join with EXISTS in SQLAlchemy
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying-with-joins

    print('*******Another join with EXISTS*******')
    # we need an import
    # The EXISTS keyword in SQL is a boolean operator which returns True if 
    # the given expression contains any rows. It may be used in many scenarios 
    # in place of joins, and is also useful for locating rows which do not 
    # have a corresponding row in a related table.
    # SELECT Perosn.username 
    # FROM Person
    # WHERE EXISTS (
    #     SELECT * 
    #     FROM Notes
    #     WHERE Notes.id = Person.id
    # )
    stmt = exists().where(Notes.id == Person.id)
    r7 = db.session.query(Person.username).filter(stmt)

    for username, in db.session.query(Person.username).filter(stmt):
        print(username)

    #raw Query
    print('*******Raw Query Execution*******')
    
    # The start of any SQLAlchemy application is an object called the Engine
    engine = create_engine('sqlite:///notes.db')
    sql = text('select * \
               from Notes JOIN Person \
               where Person.id = Notes.person_id AND Person.id = 1')
    with db.engine.connect() as conn:
        result = conn.execute(sql)
        for r in result:
            print('Title of the note is: ',r.title)
            print('Author of the note is: ',r.username)
        

@app.route('/')
@app.route('/home')
def home():
    pagename = 'CSCB20 Notes'
    return render_template('home.html', pagename = pagename)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user_name = request.form['Username']
        email = request.form['Email']
        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        reg_details = (
            user_name,
            email,
            hashed_password
        )
        add_users(reg_details)
        flash('registration successful! Please login now:')
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('Already logged in!!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        person = Person.query.filter_by(username = username).first()
        if not person or not bcrypt.check_password_hash(person.password, password):
            flash('Please check your login details and try again.', 'error')
            return render_template('login.html')
        else:
            log_details = (
            username,
            password
            )
            session['name'] = username
            session.permanent = True
            return redirect(url_for('home'))

@app.route('/notes', methods = ['GET', 'POST'])
def notes():
    if request.method == 'GET':
        query_notes_result = query_notes()
        return render_template('notes.html', query_notes_result=query_notes_result)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        note_details = (
            request.form['Note_ID'],
            request.form['Title'],
            request.form['Content'],
            request.form['Your_ID']
        )
        # print(note_details)
        add_notes(note_details)
        return render_template('add_success.html')

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('home'))

def query_notes():
    query_notes = Notes.query.all()
    return query_notes

def add_notes(note_details):
    note = Notes(id = note_details[0], title = note_details[1], content = note_details[2], person_id = note_details[3])
    db.session.add(note)
    db.session.commit()

def add_users(reg_details):
    user = Person(username = reg_details[0], email = reg_details[1], password = reg_details[2])
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)

