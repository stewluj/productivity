from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, User, CalendarEvent, LocationActivity
from . import db
import json
from datetime import datetime
import requests

# Your Google Maps API key
API_KEY = 'AIzaSyAaaPR9FAED7jjbSgA4-F2CKxa3JM8kyNA'

views = Blueprint('views', __name__)

# Home route
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

# Delete a note
@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note.get('noteId')
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})

# Pair with another user
@views.route('/pair', methods=['POST'])
@login_required
def pair_user():
    email = request.form.get('email')
    paired_user = User.query.filter_by(email=email).first()

    if not paired_user:
        flash('User with this email does not exist.', category='error')
    elif paired_user.id == current_user.id:
        flash('You cannot pair with yourself.', category='error')
    else:
        current_user.paired_user_id = paired_user.id
        db.session.commit()
        flash(f'Paired with {paired_user.first_name} successfully!', category='success')

    return redirect(url_for('views.home'))

# View shared notes with paired user
@views.route('/shared-notes', methods=['GET'])
@login_required
def shared_notes():
    paired_user_notes = Note.query.filter_by(user_id=current_user.paired_user.id).all() if current_user.paired_user else []
    return render_template("shared_notes.html", user=current_user, notes=paired_user_notes)

# My Activities: Add, view, and delete user-specific activities
@views.route('/activities', methods=['GET', 'POST'])
@login_required
def my_activities():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        if name and address:
            activity = LocationActivity(name=name, address=address, user_id=current_user.id)
            db.session.add(activity)
            db.session.commit()
            flash('Activity added!', category='success')
        else:
            flash('Name and address are required.', category='error')

    activities = LocationActivity.query.filter_by(user_id=current_user.id).all()
    return render_template("activities.html", user=current_user, activities=activities)

# Delete an activity
@views.route('/delete-activity', methods=['POST'])
@login_required
def delete_activity():
    data = json.loads(request.data)
    activity_id = data.get('activityId')
    activity = LocationActivity.query.get(activity_id)
    if activity and activity.user_id == current_user.id:
        db.session.delete(activity)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 403

# Find a place using Google Maps API
@views.route('/find-place', methods=['POST'])
def find_place():
    data = request.get_json()  # Parse JSON request body
    query = data.get('query')  # Get the 'query' field from JSON
    if not query:
        return jsonify({"error": "Query is required"}), 400

    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        'input': query,
        'inputtype': 'textquery',
        'fields': 'name,formatted_address,place_id,geometry',
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    results = response.json()

    if results.get('status') != 'OK':
        return jsonify({"error": f"No results found. Status: {results.get('status')}"}), 404

    return jsonify(results)


# View paired user's activities
@views.route('/paired-activities', methods=['GET'])
@login_required
def paired_activities():
    if not current_user.paired_user:
        flash('You are not paired with anyone.', category='error')
        return redirect(url_for('views.my_activities'))

    paired_user = current_user.paired_user
    activities = LocationActivity.query.filter_by(user_id=paired_user.id).all()
    return render_template("paired_activities.html", user=current_user, paired_user=paired_user, activities=activities)

# Calendar functionality: Add, view, and delete events
@views.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        event_time = request.form.get('event_time')

        try:
            event_time = datetime.strptime(event_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid time format. Use the date picker.', category='error')
            return redirect(url_for('views.calendar'))

        if not event_name:
            flash('Event name is required.', category='error')
        else:
            new_event = CalendarEvent(name=event_name, time=event_time, user_id=current_user.id)
            db.session.add(new_event)
            db.session.commit()
            flash('Event added to your calendar!', category='success')

    events = CalendarEvent.query.filter_by(user_id=current_user.id).order_by(CalendarEvent.time).all()
    return render_template("calendar.html", user=current_user, events=events)

# View paired user's calendar
@views.route('/paired-calendar', methods=['GET'])
@login_required
def paired_calendar():
    if not current_user.paired_user:
        flash('You are not paired with anyone.', category='error')
        return redirect(url_for('views.calendar'))

    paired_user = current_user.paired_user
    events = CalendarEvent.query.filter_by(user_id=paired_user.id).order_by(CalendarEvent.time).all()
    return render_template("paired_calendar.html", user=current_user, paired_user=paired_user, events=events)

# Delete a calendar event
@views.route('/delete-event', methods=['POST'])
@login_required
def delete_event():
    event_data = json.loads(request.data)
    event_id = event_data.get('eventId')
    event = CalendarEvent.query.get(event_id)

    if event and event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted!', category='success')
        return jsonify({"success": True})
    else:
        flash('Event not found or unauthorized.', category='error')
        return jsonify({"success": False}), 403
