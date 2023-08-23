from flask import Flask, request, jsonify, make_response
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

import pymssql

server = 'server'
database = 'master'
username = 'sa'
password = 'Kislay631'

def create_connection():
    return pymssql.connect(server, username, password, database)
# 1. Route to handle creation, sorting, and filtering
@app.route('/employees', methods=['POST'])
def manage_employees():
    data = request.json
    
    # Check if the 'operation' key is present in the request body
    if 'operation' in data:
        operation = data['operation'].lower()
        
        # Check the value of the 'operation' key to determine the action
        if operation == 'create':
            # Create a new employee (similar to the existing POST route logic)
            if 'name' in data and 'date_of_birth' in data and 'phone' in data and 'experience' in data:
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
            else:
                return jsonify({"message": "Invalid request format for employee creation"}), 400
        
        elif operation == 'filter_sort':
            # Retrieve employee data from the database
            query = "SELECT * FROM Employee;"
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            employees = cursor.fetchall()
            conn.close()
            
            columns = ["id", "name", "age", "phone", "experience"]
            df = pd.DataFrame(employees, columns=columns)
            
            # Apply filtering based on filter_criteria from the request body
            filter_criteria = data.get('filter_criteria', {})
            if 'age_greater_than' in filter_criteria:
                df = df[df['age'] > filter_criteria['age_greater_than']]
            if 'experience_equal_to' in filter_criteria:
                df = df[df['experience'] == filter_criteria['experience_equal_to']]
            
            # Apply sorting based on sort_criteria from the request body
            sort_criteria = data.get('sort_criteria', {})
            if 'sort_column' in sort_criteria and 'sort_order' in sort_criteria:
                sort_column = sort_criteria['sort_column']
                sort_order = sort_criteria['sort_order']
                df = df.sort_values(by=sort_column, ascending=(sort_order == 'asc'))
            
            return df.to_json(orient='records')
        
        else:
            return jsonify({"message": "Invalid operation in request body"}), 400
    
    else:
        return jsonify({"message": "Missing 'operation' key in request body"}), 400



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
    

# 7. Generate a report and save as CSV
@app.route('/employees/report', methods=['GET'])
def generate_and_save_report():
    query = "SELECT * FROM Employee;"

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    employees = cursor.fetchall()
    conn.close()

    columns = ["id", "name", "age", "phone", "experience"]
    df = pd.DataFrame(employees, columns=columns)

    # Generate a report (for demonstration, you can customize this)
    report_df = df[['name', 'age', 'experience']]

    # Save the report as a CSV file locally
    report_filename = 'employee_report.csv'
    report_df.to_csv(report_filename, index=False)

    # Check if the file exists and return a message
    if os.path.exists(report_filename):
        return jsonify({"message": f"Report generated and saved as {report_filename}"}), 200
    else:
        return jsonify({"message": "Failed to generate the report"}), 500



if __name__ == '__main__':
    app.run(debug=True)
