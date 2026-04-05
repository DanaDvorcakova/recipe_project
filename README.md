Recipe Blog Project

Author:    Dana Dvorcakova
Date:      05/04/2026
Link:      https://recipe-project-2-gxqs.onrender.com
           https://github.com/DanaDvorcakova/recipe_project
Database:  recipe_project_db_2026
           postgresql://recipe_project_db_2026_user:hVJak420f03mUokUW4rwen3TUElp24jD@dpg-d6lkrmdm5p6s73evd8ng-a.frankfurt-postgres.render.com/recipe_project_db_2026

OVERVIEW

This is a Recipe Blog application built with Django. It allows users to browse, create, update, delete, comment, like and save recipes. The project features user authentication, post categorization, search functionality, and a dynamic system for liking and saving posts. Users can also comment on recipes and view the most liked posts.


FEATURES

User Authentication: Users can sign up, log in, and log out.
Forgot Password / Password Reset: Email verification
Recipe Management: Users can create, edit, and delete their recipes.
Like and Save Recipes: Users can like and save recipes they find interesting.
Comment System: Users can add comments to recipes.
Search: A live search bar allows users to search recipes by title or description.
Categories: Recipes can be filtered by categories.
Most Liked Recipes: Displays the most liked recipe on the sidebar.
Publish/Unpublish Posts: Users can publish or unpublish posts.


TECHNOLOGY USED

Django: The web framework used to build the backend and views, offering robust features for rapid web development.

Bootstrap 5: A front-end framework that provides responsive and modern UI components for building an attractive and mobile-friendly interface.

Font Awesome: A popular icon library used throughout the application for enhanced user experience and aesthetic appeal.

PostgreSQL: The database used to store recipe posts, comments, user data, and other application-related information. PostgreSQL is used in production, deployed on Render for better scalability and performance.

Python 3.13.12: The programming language used to develop the project, leveraging Django's power for backend development.

Render: A cloud platform used to deploy the application. Render hosts the web service and database (PostgreSQL) to ensure the app runs smoothly in production.

Python-dotenv: A Python package used to manage environment variables securely, especially for sensitive data like database credentials, using a .env file.


TEST CREDENTIAL 

Superuser (Admin credentials for full access):
   Username: `test_admin`
   Password: `securepassword123`

Test User (Regular user with limited access):
   Username: `test_user`
   Password: `testpassword123`


SETUP INSTRUCTIONS

Follow these steps to set up and run the project on your local machine.
1. Clone the Repository
Clone the repository to your local machine using:
git clone https://github.com/yourusername/recipe-blog.git
cd recipe-blog
2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies. Run the following commands:
python3 -m venv venv
Activate the virtual environment:
•	On Windows:
venv\Scripts\activate
3. Install Dependencies
Install the necessary Python packages by running:
pip install -r requirements.txt
4. Apply Migrations
Make sure your database is set up by running:
python manage.py migrate
5. Create a Superuser
To access the Django admin panel, create a superuser account by running:
python manage.py createsuperuser
Follow the prompts to set up the admin user.
6. Run the Development Server
Start the development server:
python manage.py runserver
The server will run at http://127.0.0.1:8000/. Open this URL in your browser to access the app.
7. Admin Panel
You can access the Django admin panel at http://127.0.0.1:8000/admin/ and log in with the superuser credentials you just created.


Project Structure

recipe_project:.
│   .env
│   db.sqlite3
│   manage.py
│   README.md
│
├───blog
│   │   admin.py
│   │   apps.py
│   │   context_processors.py
│   │   custom_filters.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_alter_post_category_alter_post_author_and_more.py
│   │   │   0003_alter_post_category.py
│   │   │   0004_post_likes_alter_post_category.py
│   │   │   0005_comment.py
│   │   │   0006_post_end_date_post_stakeholders_post_start_date_and_more.py
│   │   │   0007_delete_profile.py
│   │   │   0008_post_saved_by.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           0001_initial.cpython-313.pyc
│   │           0002_alter_post_category_alter_post_author_and_more.cpython-313.pyc
│   │           0003_alter_post_category.cpython-313.pyc
│   │           0004_post_likes_alter_post_category.cpython-313.pyc
│   │           0005_comment.cpython-313.pyc
│   │           0006_post_end_date_post_stakeholders_post_start_date_and_more.cpython-313.pyc
│   │           0007_delete_profile.cpython-313.pyc
│   │           0008_post_saved_by.cpython-313.pyc
│   │           __init__.cpython-313.pyc
│   │
│   ├───static
│   │   └───blog
│   │       ├───css
│   │       │       main.css
│   │       │
│   │       ├───images
│   │       │       background.jpg
            |       default_recipe_image.jpg
│   │       │       image1.jpg
│   │       │       logo.jpg
│   │       │
│   │       └───js
│   │               main.js
│   │
│   ├───templates
│   │   └───blog
│   │           about.html
│   │           base.html
│   │           category_posts.html
│   │           home.html
│   │           post_confirm_delete.html
│   │           post_detail.html
│   │           post_form.html
│   │           post_list.html
│   │           saved_posts.html
│   │           user_posts.html
│   │
│   └───__pycache__
│           admin.cpython-313.pyc
│           apps.cpython-313.pyc
│           context_processors.cpython-313.pyc
│           forms.cpython-313.pyc
│           models.cpython-313.pyc
│           urls.cpython-313.pyc
│           views.cpython-313.pyc
│           __init__.cpython-313.pyc
│
├───media
│   │   CarrotCake.jpg
│   │   ChickenCurry.jpg
│   │   default.jpg
│   │   LentilSoup.jpg
│   │   MushroomSoup.jpg
│   │   SeafoodChowder
│   │   SeafoodChowder.jpg
│   │   StrawberryCheesecake.jpg
│   │   Tiramisu.jpg
│   │   TomatoBruschetta.jpg
│   │
│   ├───default_images
│   │       ChickenCurry_Nc5eea7.jpg
│   │       default_recipe_image.jpg
│   │       Tiramisu.jpg
│   │       TomatoBruschetta.jpg
│   │
│   ├───post_images
│   │       CarrotCake.jpg
│   │       ChickenCurry.jpg
│   │       ChickenCurry_cXpGkav.jpg
│   │       LentilSoup.jpg
│   │       MushroomSoup.jpg
│   │       SeafoodChowder
│   │       SeafoodChowder.jpg
│   │       Steak.jpg
│   │       Strawberry-Panna-Cotta-Feature.jpg
│   │       StrawberryCheesecake.jpg
│   │       Tiramisu.jpg
│   │       TomatoBruschetta.jpg
│   │
│   └───profile_pics
│           avatar-1.png
│           avatar-1_NBgVGaA.png
│           avatar-1_NBgVGaA_7GNhFox.png
│           avatar-2.png
│           avatar-2_Ll76gln.png
│           avatar-2_q5GeNsS.png
│           image.jpg
│           image1.jpg
│           image1_TBvjcqO.jpg
│           image_DKQ4p7P.jpg
│           image_dmXEOye.jpg
│
├───recipe_project
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │
│   └───__pycache__
│           settings.cpython-313.pyc
│           urls.cpython-313.pyc
│           wsgi.cpython-313.pyc
│           __init__.cpython-313.pyc
│
└───users
    │   admin.py
    │   apps.py
    │   forms.py
    │   models.py
    │   signals.py
    │   tests.py
    │   views.py
    │   __init__.py
    │
    ├───migrations
    │   │   0001_initial.py
    │   │   __init__.py
    │   │
    │   └───__pycache__
    │           0001_initial.cpython-313.pyc
    │           __init__.cpython-313.pyc
    │
    ├───templates
    │   └───users
    │           login.html
    │           logout.html
    │           password_reset.html
    │           password_reset_complete.html
    │           password_reset_confirm.html
    │           password_reset_done.html
    │           profile.html
    │           register.html
    │
    └───__pycache__
            admin.cpython-313.pyc
            apps.cpython-313.pyc
            forms.cpython-313.pyc
            models.cpython-313.pyc
            signals.cpython-313.pyc
            views.cpython-313.pyc
            __init__.cpython-313.pyc



USAGE

1. Home Page
•	Displays a list of all available recipes, including details like title, image, and brief description.
•	Allows users to search for recipes by title, description, or ingredients using the live search bar at the top of the page.
•	Displays the most liked recipe in the sidebar.
2. Recipe Detail Page
•	Displays an individual recipe's full details, including the title, description, ingredients, preparation steps, and image.
•	Users can like recipes to show appreciation, and the like count will be updated accordingly.
•	Users can leave comments on recipes, sharing their thoughts or modifications they made.
•	Users can save recipes to their profile by clicking the "Save" button. Saved recipes can be easily accessed from the saved recipes page.
3. Create/Update/Delete Recipes
•	Create New Recipe: Logged-in users can create a new recipe by filling out a form with details like title, description, ingredients, instructions, and an optional image.
•	Update Existing Recipe: Users can update their own recipes by modifying any of the details via the "Update" button on the recipe detail page.
•	Delete Recipe: The author of a recipe can delete it. Upon deletion, users will receive a confirmation message.
•	Draft and Publish: Recipes can be saved as drafts (invisible to the public) or published (visible to everyone). A user can publish a draft or unpublish a published recipe.
•	Permission Restrictions:
   o	Authors (the creators of a post) can update or delete their recipes.
   o	Contributors (users who contribute to a post but are not the authors) can update but not delete a post.
4. Publish/Unpublish Recipes
•	Authors can toggle the publish status of their recipes:
  o	Publish: Recipes that are published are visible to all users.
  o	Unpublish: Recipes that are unpublished are only visible to the author and do not appear on the public list of recipes.
•	The publish/unpublish option is accessible in the recipe detail page under "Manage Recipe."
5. User Profile
•	Users can view and edit their profiles, including updating their avatar image, and other personal information.
•	The profile page shows:
  o	A list of saved recipes that the user has bookmarked for later use.
  o	Recent activity such as recently published or updated recipes.
•	Users can access their profile page by clicking on their username in the navbar or the user dropdown.
6. Admin Panel
•	Admin users have full control over the site and can manage users, posts, and comments from the Django admin panel.
Admins can:
  o	Create, update, or delete posts and user accounts.
  o	Manage and approve comments left on recipes.
  o	Monitor user activity and system performance.
•	Access the admin panel at /admin by logging in with the superuser credentials created during the setup.


Deployment on Render with PostgreSQL

1. Set Up PostgreSQL on Render
1.1 Create a PostgreSQL Database on Render

Go to the Render Dashboard.

Click on New > Database > PostgreSQL.

Choose the appropriate region and settings for your database.

After the database is created, Render will provide a Database URL which looks like this:

postgres://username:password@host:port/database_name

1.2 Configure PostgreSQL in Your Django Project

Install PostgreSQL Dependencies:
In your project directory, activate your virtual environment and install the PostgreSQL driver:

pip install psycopg2

Update settings.py for PostgreSQL:
Open settings.py in your recipe_project folder, and replace the default SQLite database configuration with PostgreSQL settings. Modify the DATABASES configuration like this:

import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

This configuration uses environment variables to securely handle sensitive data, such as database credentials.

1.3 Create .env File for Environment Variables

Create a .env file at the root of your project to store your database credentials and other sensitive information. An example .env file:

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432

Make sure to replace the placeholders (your_database_name, your_database_user, etc.) with the actual values provided by Render when you created the PostgreSQL database.

1.4 Install python-dotenv

To load environment variables from the .env file, you need to install the python-dotenv package:

pip install python-dotenv

This package will automatically load the environment variables when the application starts.

1.5 Apply Migrations

After setting up the database, you will need to run the migrations to create the necessary tables:

python manage.py migrate

2. Deploy the Application on Render
2.1 Create a New Web Service on Render

Go to the Render Dashboard and click New > Web Service.

Select your GitHub repository that contains your project.

Choose the Python environment and the correct branch (usually main or master).

Set the Build Command to:

pip install -r requirements.txt

Set the Start Command to:

gunicorn recipe_project.wsgi:application

2.2 Configure Environment Variables on Render

In the Environment Variables section on Render, add the same environment variables as in your .env file:

DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

These variables will be used to configure the connection to your PostgreSQL database in the settings.py file.

2.3 Deploy the Application

Click Create Web Service to deploy your application. Render will automatically:

Pull your code from GitHub.

Install dependencies.

Set up the PostgreSQL database.

Start the app.

2.4 Access Your Application

Once the deployment is complete, Render will provide a URL where your app is hosted (e.g., https://your-app-name.onrender.com).





