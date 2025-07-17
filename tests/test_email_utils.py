import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.email_utils import send_email

def test_send_email_real():
    """
    Test sending a real email using environment SMTP settings.
    This test will actually send an email to the recipient.
    """
    to_email = os.getenv("SMTP_USER")  # send to yourself for test
    subject = "Test Email from Event CRM"
    body = "This is a test email sent from the Event Management CRM project."
    result = send_email(to_email, subject, body)
    assert result is True
