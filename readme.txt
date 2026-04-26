================================================================================
        LOAN PREDICTION SYSTEM - NEW LAPTOP SETUP GUIDE
================================================================================

Project: Django Loan Prediction System with Machine Learning
Author: [Your Name]
Date: November 11, 2025

This guide will help you set up the Loan Prediction System on a new laptop
by copying the existing project files and configuring the environment.

================================================================================
                            PREREQUISITES
================================================================================

1. Python 3.10.9 
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. MySQL Server installed and running
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Remember your MySQL root password

3. Git (optional, for version control)
   - Download from: https://git-scm.com/downloads/

================================================================================
                    STEP 1: COPY PROJECT FILES
================================================================================

1. Copy the entire "loan_prediction_system" folder to your new laptop
   Location example: D:\loan_prediction_system\

2. Project structure should look like:
   loan_prediction_system/
   ├── accounts/
   ├── loans/
   ├── predictions/
   ├── dashboards/
   ├── simulator/
   ├── loan_system/
   ├── templates/
   ├── static/
   ├── media/
   ├── ml_models/
   ├── manage.py
   ├── requirements.txt
   └── loan_dataset.csv

================================================================================
                STEP 2: CREATE VIRTUAL ENVIRONMENT
================================================================================

1. Open Command Prompt or PowerShell as Administrator

2. Navigate to project folder:
   cd D:\loan_prediction_system

3. Create virtual environment:
   python -m venv venv

4. Activate virtual environment:
   
   For Windows (Command Prompt):
   venv\Scripts\activate
   
   For Windows (PowerShell):
   venv\Scripts\Activate.ps1
   
   For Mac/Linux:
   source venv/bin/activate

   NOTE: You should see (venv) at the beginning of your command prompt

================================================================================
                STEP 3: INSTALL DEPENDENCIES
================================================================================

1. With virtual environment activated, install packages:
   pip install -r requirements.txt

2. If requirements.txt is missing, install manually:
   pip install django==5.0
   pip install mysqlclient
   pip install djangorestframework
   pip install pillow
   pip install pandas
   pip install numpy
   pip install scikit-learn
   pip install joblib
   pip install matplotlib
   pip install seaborn

3. Verify installation:
   pip list

================================================================================
                STEP 4: SETUP MYSQL DATABASE
================================================================================

1. Open MySQL Command Line or MySQL Workbench

2. Create database:
   CREATE DATABASE loan_prediction_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

3. Create database user:
   CREATE USER 'loan_user'@'localhost' IDENTIFIED BY 'your_password';

4. Grant privileges:
   GRANT ALL PRIVILEGES ON loan_prediction_db.* TO 'loan_user'@'localhost';
   FLUSH PRIVILEGES;

5. Exit MySQL:
   exit;

================================================================================
            STEP 5: CONFIGURE DATABASE SETTINGS
================================================================================

1. Open: loan_system/settings.py

2. Update DATABASES section with your MySQL credentials:

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'loan_prediction_db',
           'USER': 'loan_user',
           'PASSWORD': 'your_password',  # <- UPDATE THIS
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }

3. Save the file

================================================================================
                STEP 6: RUN DATABASE MIGRATIONS
================================================================================

1. With virtual environment activated:
   
   python manage.py makemigrations
   python manage.py migrate

2. If you see errors, try:
   python manage.py makemigrations accounts
   python manage.py makemigrations loans
   python manage.py makemigrations predictions
   python manage.py makemigrations dashboards
   python manage.py makemigrations simulator
   python manage.py migrate

================================================================================
                STEP 7: CREATE ADMIN USER
================================================================================

1. Open Django shell:
   python manage.py shell

2. Run this Python code (copy entire block):

from accounts.models import User, UserProfile

# Create admin user
try:
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='Admin123@',
        user_type='admin',
        first_name='Admin',
        last_name='User'
    )
    print("✓ Admin user created successfully")
except:
    admin = User.objects.get(username='admin')
    admin.set_password('Admin123@')
    admin.user_type = 'admin'
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
    print("✓ Admin user updated")

# Create admin profile
UserProfile.objects.get_or_create(
    user=admin,
    defaults={
        'annual_income': 0,
        'credit_score': 850,
        'employment_status': 'Admin'
    }
)
print("✓ Admin profile created")
print("\nLogin credentials:")
print("Username: admin")
print("Password: Admin123@")

exit()

================================================================================
            STEP 8: VERIFY ML MODEL EXISTS
================================================================================

1. Check if file exists: ml_models/loan_model.pkl

2. If missing, train the model:
   cd predictions
   python train_model.py
   cd ..

   This will create:
   - loan_dataset.csv (10,000 sample records)
   - ml_models/loan_model.pkl (trained model)

================================================================================
                STEP 9: COLLECT STATIC FILES
================================================================================

1. Run static files collection:
   python manage.py collectstatic --noinput

2. This creates a "staticfiles" folder with all CSS, JS, and images

================================================================================
                STEP 10: START THE SERVER
================================================================================

1. Start development server:
   python manage.py runserver

2. You should see:
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.

3. Open your browser and go to:
   http://127.0.0.1:8000/

4. Login with credentials:
   Username: admin
   Password: Admin123@

================================================================================
                    VERIFICATION CHECKLIST
================================================================================

✓ Python installed and in PATH
✓ Virtual environment created and activated
✓ All packages installed (pip list shows django, mysqlclient, etc.)
✓ MySQL database created
✓ Database migrations completed
✓ Admin user created
✓ ML model file exists (ml_models/loan_model.pkl)
✓ Static files collected
✓ Server runs without errors
✓ Can login to admin dashboard

================================================================================
                        URL STRUCTURE
================================================================================

Home/Login:                 http://127.0.0.1:8000/
Admin Dashboard:            http://127.0.0.1:8000/dashboards/admin/
User Dashboard:             http://127.0.0.1:8000/dashboards/user/
Apply for Loan:             http://127.0.0.1:8000/loans/apply/
Check Eligibility:          http://127.0.0.1:8000/loans/check-eligibility/
Financial Simulator:        http://127.0.0.1:8000/simulator/run/
Admin Analytics:            http://127.0.0.1:8000/dashboards/admin/analytics/
Django Admin Panel:         http://127.0.0.1:8000/admin/

================================================================================
                    COMMON ISSUES & SOLUTIONS
================================================================================

ISSUE 1: "mysqlclient" installation fails
SOLUTION: 
   - Install Visual C++ Build Tools from Microsoft
   - Or use: pip install pymysql
   - Then in settings.py __init__.py add:
     import pymysql
     pymysql.install_as_MySQLdb()

ISSUE 2: "No module named 'django'"
SOLUTION: 
   - Make sure virtual environment is activated (venv)
   - Run: pip install django==5.0

ISSUE 3: "OperationalError: (2003, "Can't connect to MySQL server")"
SOLUTION:
   - Verify MySQL service is running
   - Check username/password in settings.py
   - Ensure database 'loan_prediction_db' exists

ISSUE 4: "TemplateDoesNotExist" errors
SOLUTION:
   - Ensure templates folder exists in project root
   - Check templates/accounts/, templates/loans/, etc. exist
   - Verify TEMPLATES setting in settings.py has correct DIRS

ISSUE 5: "User has no profile" error
SOLUTION:
   - Run in Django shell:
     from accounts.models import User, UserProfile
     for user in User.objects.all():
         UserProfile.objects.get_or_create(user=user)

ISSUE 6: Model prediction not working
SOLUTION:
   - Check ml_models/loan_model.pkl exists
   - If missing, run: python predictions/train_model.py

ISSUE 7: Static files (CSS/JS) not loading
SOLUTION:
   - Run: python manage.py collectstatic --clear
   - Check STATIC_URL and STATIC_ROOT in settings.py

================================================================================
                    CREATE TEST USER (OPTIONAL)
================================================================================

To create a regular test user for testing:

python manage.py shell

from accounts.models import User, UserProfile

user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='Test123@',
    first_name='Test',
    last_name='User',
    user_type='user'
)

UserProfile.objects.create(
    user=user,
    annual_income=60000,
    credit_score=720,
    existing_loans=5000,
    employment_status='Employed'
)

print("Test user created!")
print("Username: testuser")
print("Password: Test123@")

exit()

================================================================================
                    PROJECT FEATURES
================================================================================

USER FEATURES:
- User registration and login
- Update financial profile
- Apply for loans (Personal, Home, Car, Education, Business)
- Check loan eligibility with AI prediction
- Track loan application status
- Financial behavior simulator ("What if" scenarios)
- View loan history

ADMIN FEATURES:
- Admin dashboard with statistics
- Review and approve/reject loan applications
- View all registered users
- Advanced analytics with interactive charts
- Monitor system performance
- AI-powered prediction insights

TECHNICAL FEATURES:
- Machine Learning loan prediction model (Random Forest)
- 94%+ accuracy on loan approval predictions
- Real-time data visualization with Chart.js
- Secure authentication system
- MySQL database backend
- Bootstrap 5 responsive UI
- RESTful API architecture

================================================================================
                    BACKUP REMINDER
================================================================================

IMPORTANT: Before moving to production or new setup:

1. Export database:
   mysqldump -u loan_user -p loan_prediction_db > backup.sql

2. Backup these folders:
   - media/ (uploaded files)
   - ml_models/ (trained models)
   - loan_dataset.csv (training data)

3. Keep requirements.txt updated:
   pip freeze > requirements.txt

================================================================================
                    DEVELOPMENT TIPS
================================================================================

1. Always activate virtual environment before working:
   venv\Scripts\activate

2. Check for migrations after model changes:
   python manage.py makemigrations
   python manage.py migrate

3. Run tests before deployment:
   python manage.py test

4. View Django logs:
   python manage.py runserver
   (Check terminal output for errors)

5. Access Django admin for quick data management:
   http://127.0.0.1:8000/admin/

6. Debug mode: Keep DEBUG = True in development
   For production, set DEBUG = False

================================================================================
                    DEACTIVATE VIRTUAL ENVIRONMENT
================================================================================

When you're done working:
   deactivate

================================================================================
                        SUPPORT & CONTACT
================================================================================

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- MySQL documentation: https://dev.mysql.com/doc/
- Scikit-learn docs: https://scikit-learn.org/

Project Version: 1.0
Last Updated: November 11, 2025

================================================================================
                            END OF README
================================================================================
