YOUTUBE LINK: https://youtu.be/pj-cSl4MjG0?si=TgbxSK2bqhST6nT2 
Hi and welcome to my roommates app! As an overview, this is a Flask-based wep app designed to let users namange notes, activitites, events in a calendar, and see/collaborate with paired users. It combines authentication features with Google Maps API to scrape the web.

My app uses Flask-SQLAlchemy for database interactions, Flask-Migrate for database migrations, and Flask-login for managing sessions. Consequently, make sure you have those all downloaded. But here are the following steps to get this to run:

For pre-reqs, have the following installed: Python 3.9 or later, pip, SQLite, google cloud platform (GCP) API key with "Places API" enabled, and flask-migrate and requests installed. 

Steps include: 
1. Clone my code
2. Install dependencies: pip install -r requirements.txt
pip install flask-migrate
pip install flask-login
pip install flask
pip install flask-sqlalchemy

3. Set up database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
4. Configure environment variables: FLASK_APP=main.py
FLASK_ENV=development
API_KEY=YOUR_GOOGLE_MAPS_API_KEY
5. run the application:  flask --app main run

For the google maps part, login to Google cloud consolle, enable the places API, generate an API key and remove restrctions, and replace the placeholder API key with the generated key.

For any issues contact me on github @stewluj

Here is how you actually use the app:

1. Register. The app has a very similar authentication system to Finance. The exception to this is you have to have an email ('@") when you register. It checks for a complex engouh password that is the same as the confirm password, and a unique email, and then you are registered. From there, you are automatically redirected to your home page. Here, you can add notes and delete them. On the calendar page, you can add a list of things to do with a time feature. Lastly, on the activities page, you can search for a term in the find activities section using a key word (i.e. "mexican") and the top result will pop out (i.e. Felipes) with its address. You can then add those to your activities section and later delete them. 

The next big feature is pairing users. You can search for a user by typing their email in on the paired users page, and if it is a valid register user, you are "paired." Then, you can see their notes, calendar, and activities under the respective paired blank page. 