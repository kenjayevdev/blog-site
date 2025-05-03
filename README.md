# Blog Site

🛠The following technologies were used in this project: HTML5, CSS3, Bootstrap, JavaScript, Python, Django, Django REST framework, Sqlite3

🔹What's on the site:
- Responsive web-site
- Add article
- Edit article
- Delete article
- Add portfolio
- User registration (SignUp)
- User login to the site with an opened account (LogIn)
- User logout (LogOut)
- Edit user account (Edit profile)
- User adds article (Add Post)
- User can add a photo to the profile (add photo)
- Write a comment (comment)
- Edit comment (edit)
- Delete comment (delete)
- View the number of comments (comment count)
- Search for article (search)
- Show the number of people who viewed the article (wiew count)
- View the time the article was added (add date)

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
