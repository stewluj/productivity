Hi, and here I will be explaining the design choices I made to make my app.

1. Flask. First of all, I decided to use Flask as the main base for launching this application. This is because I have the most familiarity with this framework through week 9, and also thought that it was simpler and more lightweight compared to similar competitors like Django. I create this Flask app in main.py, but I actually define the specfications of create_app() in __init__.py. Main.py acts as the entry point for running my application, whereas init works on creating and configuring the application factory. The reason why I did this is because the seperation makes it easier to scale the application. As I have a lot of componenets, I think having just an app.py would get quite cluttered quite quickly. 

2. Database design: I use SQLite as it is relatively easy to deploy and integrate. Key tables include:
User: Stores user credentials and their information
Note: Stores notes linked to a specific user
CalendarEvent: Stores events with a date and a time
LocationActivity: keeps track of activities with their name and adress that is linked to a user

I also emply a self-referential relationship model. The User model lets two users be paired (for sharing notes, activities, events) without requiring another table. My model has a foreign key that refers to a primary key of the samel model, so theres a link between records in the same table

3. Authentication and Authorization. I implement user authentication using Flask-Login because of how compatatible it is with Flask App. I ensure to protect key routes like /calendar and /activities with the @login_required decorator. I use the werkzeug.security.generate_password_hash to hass passwords for extra security. 

4. Google Maps API Integration. The /find-place route utilizes Google Maps Places API to provide query abilities for location0based activities. This makes the project have a real-world element. I chose Google Maps API bc it has robust documentation, integrates easily, and has lots of place data.

5. Blueprints for Modularity. My app uses Flask blueprints so functionality is seperated into logical modules. Auth.py handles my authentication (sign-up/register, login, logout). views.py manages what the user actual sees once logged in (notes, calendars,activities). The reason why I did this was because my project is more modular, easier to navigate and by extent debug, and is scalable for future features. 

6. Front End Design. First of all, I used Jinja and a base.html file so I could have a centralized look and reduce the amount of redundancy amognst my html files. Additionally, I use Bootstrap for a uniform and professional look, but also include my own personalization in my style.css file. I include flash messages for user feedback, and I implement scripts from my static index.js JavaScript file for async request like deleting notes or activities that do not require reloading the web page.