"""
Email utility for sending emails
"""
import logging

logger = logging.getLogger(__name__)


async def send_otp_email(email: str, otp: str) -> bool:
    """
    Send OTP to user's email
    
    TODO: Implement actual email sending with SMTP or email service
    For now, this just logs the OTP to console for development
    
    Args:
        email: Recipient email address
        otp: The OTP code to send
        
    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        # For development: Print OTP to console
        logger.info(f"========================================")
        logger.info(f"OTP Email for: {email}")
        logger.info(f"OTP Code: {otp}")
        logger.info(f"========================================")
        print(f"\n{'='*50}")
        print(f"📧 OTP Email")
        print(f"{'='*50}")
        print(f"To: {email}")
        print(f"OTP Code: {otp}")
        print(f"{'='*50}\n")
        
        # TODO: Replace with actual email sending
        # Example with aiosmtplib:
        # message = MIMEText(f"Your OTP code is: {otp}")
        # message["From"] = settings.SMTP_FROM_EMAIL
        # message["To"] = email
        # message["Subject"] = "Your OTP Code"
        # await aiosmtplib.send(message, hostname=settings.SMTP_HOST, ...)
        
        return True
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {str(e)}")
        return False
