from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

server = 'server,1433'
database = 'master'
username = 'sa'
password = 'Kislay631'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=no;UID='+username+';PWD='+password)
cursor = cnxn.cursor()

# 1. Create employee entry
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    query = "INSERT INTO Employees (name, date_of_birth, phone, experience) VALUES (?, ?, ?, ?);"
    dob = data['date_of_birth']
    cursor.execute(query, (data['name'], data['date_of_birth'], data['phone'], data['experience']))
    cnxn.commit()
    return jsonify({"message": "Employee created successfully"}), 201

# 2. Get details of an employee
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    query = "SELECT * FROM Employees WHERE id = ?;"
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    if employee:
        employee_dict = {
            "id": employee.id,
            "name": employee.name,
            "date_of_birth": employee.date_of_birth,
            "phone": employee.phone,
            "experience": employee.experience
        }
        return jsonify(employee_dict)
    else:
        return jsonify({"message": "Employee not found"}), 404

# 3. Get details of all employees
@app.route('/employees', methods=['GET'])
def get_all_employees():
    query = "SELECT * FROM Employees;"
    cursor.execute(query)
    employees = cursor.fetchall()
    employee_list = []
    for employee in employees:
        employee_dict = {
            "id": employee.id,
            "name": employee.name,
            "date_of_birth": employee.date_of_birth,
            "phone": employee.phone,
            "experience": employee.experience
        }
        employee_list.append(employee_dict)
    return jsonify(employee_list)

# 4. Delete an employee entry
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    query = "DELETE FROM Employees WHERE id = ?;"
    cursor.execute(query, (employee_id,))
    cnxn.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200

# 5. Update the details of an employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.json
    query = "UPDATE Employees SET name = ?, date_of_birth = ?, phone = ?, experience = ? WHERE id = ?;"
    cursor.execute(query, (data['name'], data['date_of_birth'], data['phone'], data['experience'], employee_id))
    cnxn.commit()
    return jsonify({"message": "Employee updated successfully"}), 200

# 6. Update a particular detail of an employee
@app.route('/employees/<int:employee_id>/<attribute>', methods=['PATCH'])
def update_employee_detail(employee_id, attribute):
    data = request.json
    if attribute in ["name", "date_of_birth", "phone", "experience"]:
        query = f"UPDATE Employees SET {attribute} = ? WHERE id = ?;"
        cursor.execute(query, (data[attribute], employee_id))
        cnxn.commit()
        return jsonify({"message": f"Employee {attribute} updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid attribute"}), 400

if __name__ == '__main__':
    app.run(debug=True)
