from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, User, CalendarEvent
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

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

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    return jsonify({})

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

@views.route('/shared-notes', methods=['GET'])
@login_required
def shared_notes():
    if current_user.paired_user:
        paired_user_notes = Note.query.filter_by(user_id=current_user.paired_user.id).all()
    else:
        paired_user_notes = []

    return render_template("shared_notes.html", user=current_user, notes=paired_user_notes)

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

@views.route('/paired-calendar', methods=['GET'])
@login_required
def paired_calendar():
    if not current_user.paired_user:
        flash('You are not paired with anyone.', category='error')
        return redirect(url_for('views.calendar'))

    paired_user = current_user.paired_user
    events = CalendarEvent.query.filter_by(user_id=paired_user.id).order_by(CalendarEvent.time).all()
    return render_template("paired_calendar.html", user=current_user, paired_user=paired_user, events=events)
