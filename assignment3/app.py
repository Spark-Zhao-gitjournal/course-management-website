from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import desc, func, and_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_type}')"

class Remark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Remark('{self.user_id}', '{self.timestamp}')"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructor_id = db.Column(db.Integer, nullable=False)
    teaching_likes = db.Column(db.Text, nullable=False)
    teaching_improvements = db.Column(db.Text, nullable=False)
    lab_likes = db.Column(db.Text, nullable=False)
    lab_improvements = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Feedback('{self.user_id}', '{self.instructor_id}', '{self.timestamp}')"

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    assignment_grade = db.Column(db.Float, nullable=True)
    midterm_exam_grade = db.Column(db.Float, nullable=True)
    lab_grade = db.Column(db.Float, nullable=True)
    final_exam_grade = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Grades('{self.student_id}', '{self.username}', '{self.timestamp}')"


@app.route('/')
def home():
    return redirect(url_for('loginpage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['userType']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please use a different email address.', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('loginpage'))
    return render_template('register.html')

@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            if user.user_type == 'student':
                return redirect(url_for('student', username=username))
            elif user.user_type == 'instructor':
                return redirect(url_for('instructor', username=username))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('loginpage.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('loginpage'))

@app.route('/student/<username>')
def student(username):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('loginpage'))
    
    current_user = User.query.filter_by(username=username).first()
    student_grades = Grades.query.filter_by(student_id=current_user.id).order_by(desc(Grades.timestamp)).first()
    instructors = User.query.filter_by(user_type='instructor').all()
    return render_template('student.html', current_user=current_user, student_grades=student_grades, instructors=instructors)

@app.route('/instructor/<username>')
def instructor(username):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('loginpage'))
    
    
    current_user = User.query.filter_by(username=username).first()

    latest_grades_subquery = db.session.query(func.max(Grades.timestamp).label('latest_timestamp')).group_by(Grades.student_id).subquery()

    
    student_grades = db.session.query(Grades).join(latest_grades_subquery, and_(Grades.timestamp == latest_grades_subquery.c.latest_timestamp)).order_by(desc(Grades.timestamp)).all()

    
    instructor_feedback = Feedback.query.filter_by(instructor_id=current_user.id).all()

    all_students = User.query.filter_by(user_type='student').all()

    all_remark_requests = Remark.query.all()
    
    return render_template('instructor.html', current_user=current_user, student_grades=student_grades, instructor_feedback=instructor_feedback, all_students=all_students, all_remark_requests=all_remark_requests)


@app.route('/submit_remark_request', methods=['POST'])
def submit_remark_request():
    if request.method == 'POST':
        user_id = session.get('user_id') 
        username = session.get('username')
        reason = request.form['remark_reason']
        
        
        new_remark = Remark(user_id=user_id, username=username, reason=reason)
        
        
        db.session.add(new_remark)
        
        
        db.session.commit()
        
        
        flash('Remark request submitted successfully!', 'success')
        current_user = User.query.get(user_id)
        return redirect(url_for('student', username=current_user.username))


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        user_id = session.get('user_id')  
        instructor_id = request.form['instructor']
        teaching_likes = request.form['teaching_likes']
        teaching_improvements = request.form['teaching_improvements']
        lab_likes = request.form['lab_likes']
        lab_improvements = request.form['lab_improvements']
        
        
        new_feedback = Feedback(user_id=user_id, instructor_id=instructor_id, teaching_likes=teaching_likes, 
                                teaching_improvements=teaching_improvements, lab_likes=lab_likes, 
                                lab_improvements=lab_improvements)
        
        
        db.session.add(new_feedback)
        
        
        db.session.commit()
        
        
        flash('Feedback submitted successfully!', 'success')
        current_user = User.query.get(user_id)
        return redirect(url_for('student', username=current_user.username))


@app.route('/enter_marks', methods=['POST'])
def enter_marks():
    if request.method == 'POST':
        user_id = session.get('user_id')
        student_id = request.form['student']
        assignment_grade = request.form.get('assignment', None)
        midterm_exam_grade = request.form.get('midterm_exam', None)
        lab_grade = request.form.get('labs', None)
        final_exam_grade = request.form.get('final_exam', None)
        
        student = User.query.get(student_id)
        student_username = student.username

        if assignment_grade == '':
            assignment_grade = None
        if midterm_exam_grade == '':
            midterm_exam_grade = None
        if lab_grade == '':
            lab_grade = None
        if final_exam_grade == '':
            final_exam_grade = None

        new_grades = Grades(
            student_id=student_id,
            username=student_username,
            assignment_grade=assignment_grade,
            midterm_exam_grade=midterm_exam_grade,
            lab_grade=lab_grade,
            final_exam_grade=final_exam_grade
        )
        db.session.add(new_grades)
        db.session.commit()
        
        current_user = User.query.get(user_id)
        return redirect(url_for('instructor', username=current_user.username))
    


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/courseteam')
def courseteam():
    return render_template('courseteam.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

@app.route('/anonfeedback')
def anonfeedback():
    return render_template('anonfeedback.html')

@app.route('/piazza')
def piazza():
    return render_template('piazza.html')

@app.route('/markus')
def markus():
    return render_template('markus.html')

@app.route('/labs')
def labs():
    return render_template('labs.html')







if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
