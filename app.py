
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

students = [
    {'ID': 1, 'Name': 'Alice', 'Grade': '3'},
    {'ID': 2, 'Name': 'Bob', 'Grade': '5'}
]
    
@app.route('/')
def hello_world():
    return 'Hello, Student Service!'

@app.route('/student/<int:id>')
def student(id):
    students_by_id = [student for student in students if student["ID"] == id]
    student_info = None
    if len(students_by_id) > 0:
        student_info = students_by_id[0]
    return jsonify(student_info)

# Endpoint to add a new student
@app.route('/students', methods=['POST'])
def add_student():
    # Parse the 'done' status from request, default to False if it's not provided
    name = request.json.get('Name', '')
    grade = request.json.get('Grade', '')

    # Create a new student object
    new_student = {
        'ID': len(students) + 1,  # Set ID as the next number in sequence
        'Name': name, 
        'Grade': grade  
    }

    # Add the new student to the students list
    students.append(new_student)

    # Return the added student with a status code indicating resource creation
    return jsonify({'student': new_student}), 201

# Endpoint to update an existing student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    # Initialize the student variable as None
    student_update = None
    # Loop through the students list
    for student in students:
        if student["ID"] == int(student_id):  # If the student with the given ID is found
            student_update = student
            break
    # If student is not found after looping
    if student_update is None:
        return jsonify({'error': 'Student not found'}), 404
    # Update student attributes with data from the request, use existing value if not provided
    student_update['Name'] = request.json.get('Name', student_update['Name'])
    student_update['Grade'] = request.json.get('Grade', student_update['Grade'])
    # Return the updated student
    return jsonify({'student': student_update})

# Endpoint to delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students  # Reference the global students list
    # Initialize the student variable as None
    student_del = None
    # Loop through the students list
    for student in students:
        if student["ID"] == student_id:  # If the usstudenter with the given ID is found
            student_del = student
            break
    # If student is not found after looping
    if student_del is None:
        return jsonify({'error': 'Student not found'}), 404
    # Remove the found student from the students list
    students.remove(student_del)
    # Return a success message
    return jsonify({'result': 'Student deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5000)