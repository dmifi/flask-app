import json

from flask import request, jsonify

from app import app
from app import db
from app.api_docs import get_apispec
from app.models import Employee, Task


@app.route('/employees', methods=['POST', 'GET'])
def manage_employee():
    """
    ---
    get:
      summary: Получить список всех сотрудников
      responses:
        '200':
          description: Список сотрудников
          content:
            application/json:
              schema: EmployeeSchema
      tags:
        - Employee
    post:
      summary: Создать нового сотрудника
      requestBody:
        content:
          application/json:
            schema: EmployeeSchema
      responses:
        '200':
          description: Сотрудник создан
          content:
            application/json:
              schema: MessageSchema
      tags:
        - Employee
    """
    if request.method == 'POST':
        data = request.get_json()
        print(request)
        print(request.data)
        print(data)
        new_employee = Employee(full_name=data['full_name'],
                                position=data['position'])
        db.session.add(new_employee)
        db.session.commit()
        return {
            "message": f"employee {new_employee.full_name} "
                       f"has been created successfully."}

    elif request.method == 'GET':
        employees = Employee.query.all()
        results = [
            {
                "full_name": employee.full_name,
                "position": employee.position,
            } for employee in employees]
        return jsonify({"count": len(results), "employees": results})


@app.route('/employee/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_employee(id):
    """
    ---
    get:
      summary: Получить данные сотрудника
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        '200':
          description: Данные сотрудника
          content:
            application/json:
              schema: MessageSchema
      tags:
        - Employee
    put:
      summary: Изменить данные сотрудника
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema: EmployeeSchema
      responses:
        '200':
          description: Данные сотрудника изменены
          content:
            application/json:
              schema: MessageSchema
      tags:
        - Employee
    delete:
      summary: Удалить сотрудника
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        '200':
          description: Сотрудник удален
          content:
            application/json:
              schema: MessageSchema

      tags:
        - Employee
    """
    employee = Employee.query.filter_by(id=id).first()

    if request.method == 'GET':
        results = {"full_name": employee.full_name,
                   "position": employee.position}
        return jsonify(results)

    elif request.method == 'PUT':
        data = request.get_json()
        employee.full_name = data['name']
        employee.position = data['model']
        db.session.add(employee)
        db.session.commit()
        return jsonify({"message": f"Employee {employee.full_name} "
                                   f"has been updated successfully."})

    elif request.method == 'DELETE':
        db.session.delete(employee)
        db.session.commit()
        return {"message": f"Employee {employee.full_name} "
                           f"has been deleted successfully."}


@app.route('/tasks', methods=['POST', 'GET'])
def manage_tasks():
    """
    ---
    get:
      summary: Получить список всех задач
      responses:
        '200':
          description: Список задач
          content:
            application/json:
              schema: TaskSchema
      tags:
        - Task
    post:
      summary: Создать новую задачу
      requestBody:
        content:
          application/json:
            schema: TaskSchema
      responses:
        '200':
          description: Задача создана
          content:
            application/json:
              schema: MessageSchema
      tags:
        - Task
    """
    if request.method == 'POST':
        data = request.get_json()
        new_task = Task(title=data['title'],
                        parent_task_id=data['parent_task_id'],
                        employee_id=data['employee_id'],
                        deadline=data['deadline'],
                        status=data['status'])
        db.session.add(new_task)
        db.session.commit()
        return {"message": f"Task {new_task.title} "
                           f"has been created successfully."}

    elif request.method == 'GET':
        tasks = Task.query.all()
        results = [
            {
                "id": task.id,
                "title": task.title,
                "parent_task_id": task.parent_task_id,
                "employee_id": task.employee_id,
                "deadline": task.deadline,
                "status": task.status
            } for task in tasks]
        return jsonify({"count": len(results), "tasks": results})


@app.route('/task/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_task(id):
    """
    ---
    get:
      summary: Получить данные задачи
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        '200':
          description: Данные задачи
          content:
            application/json:
              schema: MessageSchema
      tags:
        - Task
    put:
      summary: Изменить данные задачи
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema: TaskSchema
      responses:
        '200':
          description: Данные задачи изменены
          content:
            application/json:
              schema: MessageSchema
      tags:
        - Task
    delete:
      summary: Удалить задачу
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        '200':
          description: Задача удалена
          content:
            application/json:
              schema: MessageSchema
      tags:
        - Task
    """
    task = Task.query.filter_by(id=id).first()

    if request.method == 'GET':
        results = {"id": task.id,
                   "title": task.title,
                   "parent_task_id": task.parent_task_id,
                   "employee_id": task.employee_id,
                   "deadline": task.deadline,
                   "status": task.status}
        return jsonify(results)

    elif request.method == 'PUT':
        data = request.get_json()
        task.title = data['title']
        task.parent_task_id = data['parent_task_id']
        task.employee_id = data['employee_id']
        task.deadline = data['deadline']
        task.status = data['status']
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": f"Task {task.title} "
                                   f"has been updated successfully."})

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return {"message": f"Employee {task.title} "
                           f"has been deleted successfully."}


@app.route('/busy-employees', methods=['GET'])
def get_busy_employees():
    """
    ---
    get:
      summary: Получить список занятых сотрудников и их задач
      responses:
        '200':
          description: Список занятых сотрудников и их задач
          content:
            application/json:
              schema: EmployeeSchema
      tags:
        - Employee
    """
    employees = Employee.query.outerjoin(Task). \
        group_by(Employee.id). \
        filter(Employee.tasks). \
        order_by(db.func.count().filter(Task.status).desc())
    results = [
        {
            "id": employee.id,
            "full_name": employee.full_name,
            "position": employee.position,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "parent_task_id": task.parent_task_id,
                    "employee_id": task.employee_id,
                    "deadline": task.deadline,
                    "status": task.status
                }
                for task in employee.tasks],
        } for employee in employees]
    return jsonify({"count": len(results), "employees": results})


@app.route('/important-task', methods=['GET'])
def get_important_task():
    """
    ---
    get:
      summary: Получить список важных задач и сотрудников которые могу взять эти задачи
      responses:
        '200':
          description: Список важных задач и сотрудников которые могу взять эти задачи
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    task title:
                      type: string
                    deadline:
                      type: string
                    employees:
                      type: array
                      items:
                        type: string
      tags:
        - Task
    """
    tasks = Task.query.filter(Task.employee_id == None,
                              Task.parent_task != None).all()
    employees = Employee.query.all()
    minimal_tasks_count = min(
        [(len(employee.tasks)) for employee in employees])
    least_busy_employees = [
        employee.full_name for employee in employees if
        (len(employee.tasks)) == minimal_tasks_count]
    result = []
    for task in tasks:
        task_list = {
            'title': task.title,
            'deadline': task.deadline,
            'employee': []
        }
        result.append(task_list)
        for employee in employees:
            employee_less_busy = len(employee.tasks) < (
                    minimal_tasks_count + 2)
            for sub_task in employee.tasks:
                employee_busy_on_parent = sub_task.id == task.parent_task_id
                if employee_less_busy and employee_busy_on_parent:
                    list_emp = employee.full_name
                    task_list['employee'].append(list_emp)
        task_list['employee'].extend(least_busy_employees)
    return jsonify(result)


@app.route('/swagger')
def create_swagger_spec():
    return json.dumps(get_apispec(app).to_dict())
