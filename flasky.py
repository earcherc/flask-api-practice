import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User

# Begin script by initialising app
app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


# To set the imports for flask shell automatically on init
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
