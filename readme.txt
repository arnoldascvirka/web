##################################

Arnoldas Cvirka 2022-10-11

WEB Flask project

##################################

• The project is launched with app.py.

• The project can save users and posts. 
• Passwords are hashed in SQL. 
• You can change the profile picture; the default is static/profile_pics/default.jpg. 
• After creating a post, by clicking on it with the appropriate user, you can delete or update your post. 
• By clicking on a user, you can see all of their posts. 
• An SMTP client is running (can be seen in the config.py file), which is used to send password reset emails with generated user tokens. 
• Routes are divided into corresponding folders; for example, all user routes like login and register are in the users folder.

If there's an error due to itsdangerous, you can install it via: pip install git+https://github.com/puiterwijk/flask-oidc.git@b10e6bf881a3fe0c3972e4093648f2b77f32a97c

This is because itsdangerous is a deprecated library.
