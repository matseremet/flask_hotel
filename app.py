from flask import Flask, request, url_for, render_template, redirect, flash
import os
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abc'

class PriorityType:
    def __init__(self, code, description, selected):
        self.code = code
        self.description = description
        self.selected = selected
        
        
class NotificationPriorities:
    def __init__(self):
        self.list_of_priorities = []
        
    def load_priorities(self):
        self.list_of_priorities.append(PriorityType('high', 'HIGH PRIORITY', False))
        self.list_of_priorities.append(PriorityType('medium', 'MEDIUM', False))
        self.list_of_priorities.append(PriorityType('normal', 'NOT URGENT', True))
        self.list_of_priorities.append(PriorityType('low', 'REMARK', False))
        
    def get_priority_by_code(self, code):
        for p in self.list_of_priorities:
            if p.code == code:
                return p
        return PriorityType('normal', 'NOT URGENT', True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notification', methods=['GET', 'POST'])
def notification():
    
    priorities = NotificationPriorities()
    priorities.load_priorities()
    
    if request.method == 'GET':
        return render_template('notification.html', priorities=priorities)
    else:
        room_number = request.form['room_number'] if 'room_number' in request.form else ''
        surname = request.form['surname'] if 'surname' in request.form else ''
        room_notification = request.form['room_notification'] if 'room_notification' in request.form else ''
        priority = request.form['priority'] if 'priority' in request.form else 'normal'
        
        flash('Notification has been sent')
        
        the_hour = datetime.now().hour        
        raise_priority = (the_hour >= 20 or the_hour < 6) and priority == 'medium'
        if raise_priority:
            priority = 'high'
            flash('Rising priority from medium to high')
               
        return render_template('notification_content.html', room_number=room_number, surname=surname, room_notification=room_notification, priority_type=priorities.get_priority_by_code(priority) )
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)