from app import app, db
from app.models import Device, User

# print(app.config)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Device': Device, 'User': User}
