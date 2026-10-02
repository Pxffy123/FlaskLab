from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data class
class Event:

  def __init__(self, id, title):
    self.id = id
    self.title = title

  def to_dict(self):
    return {'id': self.id, 'title': self.title}


# In-memory "database"
events = [Event(1, 'Tech Meetup'), Event(2, 'Python Workshop')]


# Helper function to find an event by ID
def find_event_by_id(event_id):
  for event in events:
    if event.id == event_id:
      return event
  return None


# 1. JSON welcome message at the root route
@app.route('/')
def home():
  return jsonify({'message': 'Welcome to the Flask CRUD API!'}), 200


# 2. GET request to /events returning a JSON array
@app.route('/events', methods=['GET'])
def get_events():
  return jsonify([event.to_dict() for event in events]), 200


# 3. POST request to /events returning 201 Created
@app.route('/events', methods=['POST'])
def create_event():
  data = request.get_json()

  if not data or 'title' not in data:
    return jsonify({'error': 'Invalid or missing data'}), 400

  new_id = events[-1].id + 1 if events else 1
  new_event = Event(new_id, data['title'])
  events.append(new_event)

  return jsonify(new_event.to_dict()), 201


# PATCH: Update an existing event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
  data = request.get_json()

  if not data or 'title' not in data:
    return jsonify({'error': 'No title provided for update'}), 400

  target_event = find_event_by_id(event_id)
  if not target_event:
    return jsonify({'error': 'Event not found'}), 404

  target_event.title = data['title']
  return jsonify(target_event.to_dict()), 200


# DELETE: Remove an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
  target_event = find_event_by_id(event_id)
  if not target_event:
    return jsonify({'error': 'Event not found'}), 404

  events.remove(target_event)
  return '', 204


if __name__ == '__main__':
  app.run(debug=True)