# using flask_restful
# import all relevant Libraries
from flask import *
from flask_restful import Resource, Api

# import pymysql for Dbase connection
import pymysql
import pymysql.cursors

# creating the flask app
app = Flask(__name__)

# creating an API object - Link the app to API Object
api = Api(app)

# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
# Below Employee inherits a Resource , hence implementing the 4 methods post, get.

class Employee(Resource):
# corresponds to the GET request.
# this function is called whenever there
# is a GET request for this resource
    def get(self):
        connection = pymysql.connect(host='modcomLab2.mysql.pythonanywhere-services.com', user='modcomLab2', password='code_knight@01', database='modcomLab2$default')
        cursor = connection.cursor()
        sql = "select*from employees"
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return jsonify({'message':'No Records'})
        else:
            employees = cursor.fetchall()
            return jsonify(employees)
    # Corresponds to POST request
    def post(self):
        data = request.json
        username = data['username']
        email = data['email']
        department = data['department']

        connection = pymysql.connect(host='modcomLab2.mysql.pythonanywhere-services.com', user='modcomLab2', password='code_knight@01', database='modcomLab2$default')

        cursor = connection.cursor()
        sql = "insert into employees (username,email,department)values(%s, %s, %s)"
        try:
            cursor.execute(sql, (username, email, department))
            connection.commit()
            return jsonify({'message': 'POST SUCCESS. RECORD SAVED'})
        except:
            connection.rollback()
            return jsonify({'message': 'POST FAILED. RECORD NOT SAVED'})

    # adding the defined resource/Class along with its corresponding url
api.add_resource(Employee, '/employees')
    # driver function

app.run(debug = True)