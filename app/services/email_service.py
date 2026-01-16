"""
Email service for sending notifications.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications."""
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send email notification."""
        if not settings.SMTP_HOST or not settings.SMTP_USER:
            logger.warning("Email settings not configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = settings.EMAILS_FROM_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text
            msg.attach(MIMEText(body, 'plain'))
            
            # Add HTML if provided
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    @staticmethod
    def send_welcome_email(user_email: str, user_name: str):
        """Send welcome email to new user."""
        subject = f"Welcome to {settings.PROJECT_NAME}"
        body = f"""
        Hi {user_name},
        
        Welcome to GlobalShip! Your account has been created successfully.
        
        You can now:
        - Create shipments
        - Track packages
        - Request quotes
        
        Best regards,
        The GlobalShip Team
        """
        return EmailService.send_email(user_email, subject, body)
    
    @staticmethod
    def send_shipment_update(user_email: str, tracking_number: str, status: str):
        """Send shipment status update email."""
        subject = f"Shipment Update - {tracking_number}"
        body = f"""
        Your shipment {tracking_number} has been updated.
        
        New Status: {status}
        
        Track your shipment at: {settings.BACKEND_CORS_ORIGINS[0]}/track/{tracking_number}
        
        Best regards,
        The GlobalShip Team
        """
        return EmailService.send_email(user_email, subject, body)
    
    @staticmethod
    def send_quote_notification(user_email: str, quote_id: str):
        """Send quote response notification."""
        subject = "Your Quote Request Has Been Processed"
        body = f"""
        Your quote request has been processed.
        
        Quote ID: {quote_id}
        
        View your quote in the dashboard.
        
        Best regards,
        The GlobalShip Team
        """
        return EmailService.send_email(user_email, subject, body)


email_service = EmailService()
