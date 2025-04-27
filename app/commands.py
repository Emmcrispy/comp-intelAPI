import click
from app.extensions import db
from app.utils.user_utils import create_default_roles, seed_admin_user

def init_app(app):
    @app.cli.command("init-db")
    @click.argument("admin_username", default="admin")
    @click.argument("admin_password", default="adminpass")
    def init_db(admin_username, admin_password):
        """
        Drop all tables, recreate schema, and seed with roles and an admin user.
        """
        # Import models so SQLAlchemy knows about them
        import app.models.user
        import app.models.role
        import app.models.job

        click.echo("→ Dropping all tables...")
        db.drop_all()

        click.echo("→ Creating tables...")
        db.create_all()

        click.echo("→ Seeding roles...")
        create_default_roles()

        click.echo(f"→ Seeding admin user '{admin_username}'...")
        seed_admin_user(admin_username, admin_password)

        click.echo("✅ Database reset and seeded with roles + admin user.")
