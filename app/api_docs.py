from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint

from app import app
from app.schemas import TaskSchema, EmployeeSchema, MessageSchema


def create_tags(spec):
    """ Создаем теги.

    :param spec: объект APISpec для сохранения тегов
    """
    tags = [
        {'name': 'Employee', 'description': 'Сотрудники'},
        {'name': 'Task', 'description': 'Задачи'},
    ]

    for tag in tags:
        print(f"Добавляем тег: {tag['name']}")
        spec.tag(tag)


def load_docstrings(spec, app):
    """ Загружаем описание API.

    :param spec: объект APISpec, куда загружаем описание функций
    :param app: экземпляр Flask приложения, откуда берем описание функций
    """
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f'Загружаем описание для функции: {fn_name}')
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


def get_apispec(app):
    """ Формируем объект APISpec.

    :param app: объект Flask приложения
    """
    spec = APISpec(
        title="Task manager",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("Employee", schema=EmployeeSchema)
    spec.components.schema("Task", schema=TaskSchema)
    spec.components.schema("Message", schema=MessageSchema)

    create_tags(spec)

    load_docstrings(spec, app)

    return spec


SWAGGER_URL = '/docs'
API_URL = '/swagger'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Employees and Tasks'
    }
)

app.register_blueprint(swagger_ui_blueprint)
