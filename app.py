from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with your actual secret key
db = SQLAlchemy(app)


# Subject model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    link = db.Column(db.String(200), nullable=False)


# Initialize the database
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # Fetch all subjects from the database
    subjects = Subject.query.all()
    return render_template('index.html', subjects=subjects)


@app.route('/subject/<subject_name>')
def subject(subject_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    if subject:
        return redirect(subject.link)
    else:
        return "Subject not found", 404


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get the subject name and link from the form
        subject_name = request.form['subject_name']
        subject_link = request.form['subject_link']

        # Check if the subject name already exists
        existing_subject = Subject.query.filter_by(name=subject_name).first()
        if existing_subject:
            flash("Subject already exists!")
        else:
            # Add the new subject to the database
            new_subject = Subject(name=subject_name, link=subject_link)
            db.session.add(new_subject)
            db.session.commit()
            flash("Subject added successfully!")

        return redirect(url_for('admin'))  # Redirect to the admin page after form submission

    else:
        # Fetch all subjects from the database
        subjects = Subject.query.all()
        return render_template('admin.html', subjects=subjects)

@app.route('/modify/<int:subject_id>', methods=['GET', 'POST'])
def modify_subject(subject_id):
    # Fetch the subject by ID
    subject = Subject.query.get(subject_id)
    if subject:
        if request.method == 'POST':
            # Get the new subject name and link from the form
            new_subject_name = request.form['new_subject_name']
            new_subject_link = request.form['new_subject_link']
            # Update the subject record in the database
            subject.name = new_subject_name
            subject.link = new_subject_link
            db.session.commit()
            flash('Subject updated successfully!')
            return redirect(url_for('admin'))
        else:
            return render_template('modify.html', subject=subject)
    else:
        flash('Subject not found!')
        return redirect(url_for('admin'))



@app.route('/delete/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!')
    else:
        flash('Subject not found!')

    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)
