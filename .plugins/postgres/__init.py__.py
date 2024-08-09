import click
import psycopg2

from psycopg2.sql import SQL, Identifier

DEFAULT_USER = "piku"
EXIST_DB = SQL("SELECT 1 from pg_database WHERE datname = %s")
CREATE_DB = SQL("CREATE DATABASE {}")
DROP_DB = SQL("DROP DATABASE {}")


@click.group()
def postgres():
    """Postgres command plugin"""
    pass


@postgres.command("postgres:create")
@click.argument("name")
def postgres_create(name):
    """Creates a database"""
    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user=DEFAULT_USER)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(EXIST_DB, (name,))
            exists = cur.fetchone()
        if exists:
            click.echo(f"Database '{name}' already exists.")
        else:
            with conn.cursor() as cur:
                cur.execute(CREATE_DB.format(Identifier(name)))
                click.echo(f"Database '{name}' created successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


def cli_commands():
    return postgres
