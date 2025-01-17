# FastAPI Todo App Assignment
A FastAPI Todo App Assignment

# Sample Setup (ubuntu 22.xx, python 3.12)
- Create a virtual environment using `python3.12-venv` module.
```bash
# Install module (globally)
sudo apt install python3.12-venv

# Generate virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install depdendency packages
pip install -r requirements.txt
```
- Configure `.env` file by creating a copy from `.env.sample`
- Setup a postgres docker container
```bash
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=<your-preferred-one> -d postgres:14
```
- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible. In case you want to use `SQLite` instead, please be sure to configure the `env.py` file in `alembic` folder to support `batch execution` since `SQLite` does not support `ALTER` command, which is needed to configure the foreign key and establish the indexes.
```bash
# Migrate to latest revison
alembic upgrade head

# Dowgragde to specific revision
alembic downgrade <revision_number>

# Downgrade to base (revert all revisions)
alembic downgrade base

# Create new revision
alembic revision -m <comment>
```
- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)
```bash
uvicorn main:app --reload
```

# Pip command

Create requirements.txt
```
pip freeze > requirements.txt
```