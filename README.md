### Prerequisites

1. **Python:** Ensure that Python is installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

2. **pip:** The package installer for Python. It is usually included with Python installations. You can check if it's installed by running `pip --version` in your terminal or command prompt.

3. **Django:** Install Django using pip. You can do this by running the following command:
    ```bash
    pip install django
    ```

4. **Google Account for Google Authentication:**
    - You will need a Google account to set up authentication.
    - Use the following Google account details for testing (replace with your own for production):
        - Email: pankajrathl@gmail.com
        - Password: your password
        - Folder Name: quicksand

    - I have given permission for authentication to the following email:
        - Email: mopasa@quicksand.co.in





### How to Install and run project


create virtual environment:
    python3 -m venv my_env

Activate virtual environment:
    source my_env/bin/activate

Use the below command to install the requirements.txt file if you face any issues
    pip3 install -r requirements.txt    

run project -
   python3 manage.py runserver


### User flow is :
    1. Home (url : http://127.0.0.1:8000/): 
        
    Home url show SignUp and Login functionality if you not not login

    2. SignUp (url : http://127.0.0.1:8000/singup/): 
    
    Users visit the signup page to register for the application.They provide necessary information such as name, and password.Upon successful submission, user data is stored in the database, and the user account is created.

    3. Login Page (url : http://127.0.0.1:8000/login/ )
       
    Users visit the signup page to register for the application. They provide necessary information such as username and password. Upon successful submission, user data is stored in the database, and the user account is created. Login Page:


    Authenticated users are redirected to the main application dashboard or landing page.
    Here, they can access various features and functionalities provided by the application.
    Actions After Login:

   4. after succesfully login you can access servives like -
       a. Upload file
       b. Delete File
       c. Show ALl Files
       d. Logout






