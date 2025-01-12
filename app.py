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
        subjects = parameters.get('study_subjects', ['your subjects'])
        time_duration = parameters.get('time_duration', '1 hour')
        break_type = parameters.get('break_preference', 'short')

        # Extract numeric hours from the time_duration string
        try:
            hours = float(''.join(filter(str.isdigit, time_duration.split()[0])))  # Extract numbers
        except (ValueError, IndexError):
            hours = 1  # Default to 1 hour if parsing fails

        # Generate the study plan response
        response_text = generate_subject_study_plan(subjects, hours, break_type)
    else:
        # Let Dialogflow handle other intents
        return jsonify({})

    # Return the response as JSON
    return jsonify({'fulfillmentText': response_text})


def generate_subject_study_plan(subjects, hours, break_type):
    """
    Generates a study plan for multiple subjects with time management and recommendations.
    """
    # Define study and break durations based on the break type
    if break_type == "short":
        study_period = 25  # Pomodoro-style sessions
        break_duration = 5
    elif break_type == "long":
        study_period = 50  # Longer focused sessions
        break_duration = 15
    else:
        study_period = 40  # Default balance
        break_duration = 10

    # Calculate total study time in minutes
    total_time = int(hours * 60)
    subject_count = len(subjects)

    # Divide time proportionally among subjects
    time_per_subject = total_time // subject_count

    # Generate the study plan
    plan_text = f"Here’s your study plan for {hours:.1f} hour(s):\n"
    for subject_index, subject in enumerate(subjects):
        plan_text += f"\n**Subject {subject_index + 1}: {subject}**\n"
        session_count = time_per_subject // (study_period + break_duration)

        for session in range(1, session_count + 1):
            plan_text += f"  Session {session}: Study for {study_period} minutes focused on {subject}.\n"
            plan_text += f"  Break: Take a {break_duration}-minute break. Suggested activities: stretch, hydrate, or walk around.\n"

        # Handle remaining time for the subject
        remaining_time = time_per_subject % (study_period + break_duration)
        if remaining_time >= study_period:
            plan_text += f"  Final session: Study for {study_period} minutes.\n"
        elif remaining_time > 0:
            plan_text += f"  Final session: Study for {remaining_time} minutes.\n"

        # Add subject-specific closing suggestion
        plan_text += f"  Tip: Review your notes or practice key problems for {subject} before moving to the next subject.\n"

    # Add final suggestions
    plan_text += "\n🌟 End your study session by summarizing key takeaways and preparing for the next day."

    return plan_text


if __name__ == '__main__':
    app.run(port=5000, debug=True)
