from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__) #create the object for using the Flask function
socketio = SocketIO(app)


@app.route('/')    #address to render the home page
def home():
    return render_template("indexpage.html")


@app.route('/chat') #address to render the chat page
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chatpage.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@app.route('/about') #the page describing the project
def about():
        return render_template("about.html")
    
@app.route('/developers') #the page giving details about the developers
def developers():
        return render_template("developers.html")
        
@app.route('/topics')  #the page giving details of the topics covered in the project
def topics():
        return render_template("topics.html")

@socketio.on('send_message')  #to print the sent message
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],data['room'],data['message']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room') #to announce that a person has joined the room
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room') #to announce that a person has left the room
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True) # this runs the application through the socketio object
