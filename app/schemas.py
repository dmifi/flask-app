from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    """Employee response schema."""
    # id = fields.Int()
    full_name = fields.Str()
    position = fields.Str()


class TaskSchema(Schema):
    """Task response schema."""

    # id = fields.Int()
    full_name = fields.Str()
    position = fields.Str()
    parent_task_id = fields.Int()
    employee_id = fields.Int()
    deadline = fields.DateTime()
    status = fields.Bool()


class MessageSchema(Schema):
    """Message response schema."""

    message = fields.Str()
