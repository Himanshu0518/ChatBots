from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/', methods=['POST'])
def webhook():
    # Parse the incoming JSON request
    req = request.get_json()

    # Extract intent and parameters
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName', {})
    parameters = req.get('queryResult', {}).get('parameters', {})

    # Handle only the "Study Plan" intent
    if intent == 'Study Plan':
        subject = parameters.get('study_subject', 'your subjects')
        time_duration = parameters.get('time_duration', '1 hour')
        break_type = parameters.get('break_preference', 'short')

        # Extract numeric hours from the time_duration string
        try:
            hours = float(''.join(filter(str.isdigit, time_duration.split()[0])))  # Extract numbers
        except (ValueError, IndexError):
            hours = 1  # Default to 1 hour if parsing fails

        # Generate the study plan response
        response_text = generate_study_plan_text(subject, hours, break_type)
    else:
        # Let Dialogflow handle other intents
        return jsonify({})

    # Return the response as JSON
    return jsonify({'fulfillmentText': response_text})


def generate_study_plan_text(subject, hours, break_type):
    """
    Generates a textual study plan based on inputs.
    """
    # Define study and break durations based on the break type
    study_period = 25 if break_type == "short" else 50
    break_duration = 5 if break_type == "short" else 15

    # Calculate total study time in minutes and the number of sessions
    total_time = int(hours * 60)
    session_count = total_time // (study_period + break_duration)

    # Generate the study plan text
    plan_text = f"Here’s your study plan for {hours} hour(s) of {subject}:\n"
    for session in range(1, session_count + 1):
        plan_text += f"Session {session}: Study for {study_period} minutes, then take a {break_duration}-minute break.\n"

    # Handle remaining time, if any
    remaining_time = total_time % (study_period + break_duration)
    if remaining_time >= study_period:
        plan_text += f"Final session: Study for {study_period} minutes.\n"
    elif remaining_time > 0:
        plan_text += f"Final session: Study for {remaining_time} minutes.\n"

    return plan_text


if __name__ == '__main__':
    app.run(port=5000, debug=True)
