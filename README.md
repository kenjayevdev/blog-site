# Django DRF Template

Template Repository to Create Django &amp; DRF Project With Swagger

## Setup

- run `python -m venv venv` to create virtual environment
- run `venv\Scripts\activate` to activate the venv
- run `pip install -r requirements.txt` to install all required packages
- run `python changeProjectName <your project name>` to change project name with your project name
  - Example: `python changeProjectName myProject`
  - After change your project name, you can delete `changeProjectName.py` file
- create `.env` file and set your `SECRET_KEY` in the file.
- run `python manage.py makemigrations`
- run `python manage.py migrate`
- run `python manage.py spectacular --file schema.yml` to create schema file
- run `python manage.py runserver`
