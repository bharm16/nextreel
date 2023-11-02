# Import required libraries
from flask import Flask
from flask_mailman import Mail, EmailMessage
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure a mock email server
app.config['MAIL_BACKEND'] = 'console'  # Use the console backend
app.config['MAIL_SUPPRESS_SEND'] = True  # Suppress sending emails for testing

# Initialize Flask-Mailman
mail = Mail(app)


# Set up a route to send a test email
@app.route('/send_test_email')
def send_test_email():
    msg = EmailMessage(
        'Test Subject',
        'This is a test email sent from the Flask application.',
        'from@example.com',
        ['to@example.com']
    )
    msg.send()
    return 'Sent a test email to the console!'


if __name__ == "__main__":
    # Set up logging to output emails to the console
    logging.basicConfig(level=logging.DEBUG)

    # Run the Flask app
    app.run(debug=True)
