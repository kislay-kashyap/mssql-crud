from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

import pymssql

server = 'server'
database = 'master'
username = 'sa'
password = 'Kislay631'

def create_connection():
    return pymssql.connect(server, username, password, database)
# 1. Create employee entry
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    query = "INSERT INTO Employee (name, age, phone, experience) VALUES (%s, %s, %s, %s);"
    dob = data['date_of_birth']
    today = datetime.today()
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (data['name'], age, data['phone'], data['experience']))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Employee created successfully"}), 201

# 2. Get details of an employee
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    query = "SELECT * FROM Employee WHERE id = %s;"
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    conn.close()

    if employee:
        employee_dict = {
            "id": employee[0],
            "name": employee[1],
            "age": employee[2],
            "phone": employee[3],
            "experience": employee[4]
        }
        return jsonify(employee_dict)
    else:
        return jsonify({"message": "Employee not found"}), 404

# 3. Get details of all employees
@app.route('/employees', methods=['GET'])
def get_all_employees():
    query = "SELECT * FROM Employee;"
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    employees = cursor.fetchall()
    conn.close()

    employee_list = []
    for employee in employees:
        employee_dict = {
            "id": employee[0],
            "name": employee[1],
            "age": employee[2],
            "phone": employee[3],
            "experience": employee[4]
        }
        employee_list.append(employee_dict)
    
    return jsonify(employee_list)

# 4. Delete an employee entry
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    query = "DELETE FROM Employee WHERE id = %s;"
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (employee_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Employee deleted successfully"}), 200

# 5. Update the details of an employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.json
    query = "UPDATE Employee SET name = %s, age = %s, phone = %s, experience = %s WHERE id = %s;"
    dob = data['date_of_birth']
    today = datetime.today()
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (data['name'], age, data['phone'], data['experience'], employee_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Employee updated successfully"}), 200

# 6. Update a particular detail of an employee
@app.route('/employees/<int:employee_id>/<attribute>', methods=['PATCH'])
def update_employee_detail(employee_id, attribute):
    data = request.json
    if attribute in ["name", "phone", "experience"]:
        query = f"UPDATE Employee SET {attribute} = %s WHERE id = %s;"
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query, (data[attribute], employee_id))
        conn.commit()
        conn.close()
        
        return jsonify({"message": f"Employee {attribute} updated successfully"}), 200
    elif attribute == 'date_of_birth':
        query = f"UPDATE Employee SET age = %s WHERE id = %s;"
        dob = data['date_of_birth']
        today = datetime.today()
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query, (age, employee_id))
        conn.commit()
        conn.close()
        
        return jsonify({"message": f"Employee {attribute} updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid attribute"}), 400

if __name__ == '__main__':
    app.run(debug=True)
