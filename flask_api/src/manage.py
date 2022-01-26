from flask.cli import FlaskGroup
from services.main import main as main_blueprint
from services.auth import auth as auth_blueprint
from services.app import app, db


cli = FlaskGroup(app)


# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
app.register_blueprint(main_blueprint)


@cli.command("create_db")
# To create the Database and Tables.
def create_db():
    # db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
