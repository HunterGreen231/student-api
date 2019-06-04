from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    special_skill = db.Column(db.String(40), nullable=False)

    def __init__(self, first_name, last_name, birthday, special_skill):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.special_skill = special_skill

class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "birthday", "special_skill")

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@app.route("/students", methods=["GET"])
def get_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result.data)

@app.route("/add-student", methods=["POST"])
def add_student():
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        birthday = request.json["birthday"]
        special_skill = request.json["special_skill"]

        record = Student(first_name, last_name, birthday, special_skill)

        db.session.add(record)
        db.session.commit()

        student = Student.query.get(record.id)
        return student_schema.jsonify(student)

if __name__ == "__main__":
        app.debug = True
        app.run()