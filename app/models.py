from app import db


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    position = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Employee {self.id} - {self.full_name}"


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    parent_task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    parent_task = db.relationship('Task', remote_side=id, backref='sub_tasks')
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref=db.backref('tasks', lazy=True))
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean(), default=False, nullable=False)

    def __repr__(self):
        return f"Task {self.title}"
