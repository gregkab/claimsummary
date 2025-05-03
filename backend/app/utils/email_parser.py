import re
import email
from email.parser import Parser
from email.policy import default
from bs4 import BeautifulSoup
import html2text
from datetime import datetime


def parse_email_content(raw_email):
    """
    Parse raw email content to extract subject, clean body, and timestamp.
    """
    try:
        # Parse the email using Python's email module
        parsed_email = email.message_from_string(raw_email, policy=default)
        
        # Extract subject
        subject = parsed_email.get('Subject', '')
        
        # Extract body
        body = ""
        if parsed_email.is_multipart():
            for part in parsed_email.iter_parts():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_content()
                    break
                elif content_type == 'text/html':
                    html_body = part.get_content()
                    # Convert HTML to plain text
                    h = html2text.HTML2Text()
                    h.ignore_links = False
                    body = h.handle(html_body)
                    break
        else:
            content_type = parsed_email.get_content_type()
            if content_type == 'text/plain':
                body = parsed_email.get_content()
            elif content_type == 'text/html':
                html_body = parsed_email.get_content()
                # Convert HTML to plain text
                h = html2text.HTML2Text()
                h.ignore_links = False
                body = h.handle(html_body)
        
        # Extract timestamp
        date_str = parsed_email.get('Date')
        timestamp = None
        if date_str:
            try:
                timestamp = email.utils.parsedate_to_datetime(date_str)
            except:
                # Fallback to current time if date parsing fails
                timestamp = datetime.utcnow()
        else:
            timestamp = datetime.utcnow()
            
        # Clean the body
        clean_body = clean_email_body(body)
        
        return {
            'subject': subject,
            'clean_body': clean_body,
            'raw_body': raw_email,
            'timestamp': timestamp
        }
    
    except Exception as e:
        # If parsing fails, return a basic structure
        return {
            'subject': 'Unable to parse subject',
            'clean_body': raw_email,
            'raw_body': raw_email,
            'timestamp': datetime.utcnow()
        }


def clean_email_body(body):
    """
    Clean email body by removing signatures, forwarded content markers, etc.
    """
    # Remove email signatures
    signature_patterns = [
        r'--\s*\n.*', # Standard signature separator
        r'Sent from my .*', # Mobile signatures
        r'Get Outlook for .*', # Outlook signatures
    ]
    
    cleaned_body = body
    
    for pattern in signature_patterns:
        cleaned_body = re.sub(pattern, '', cleaned_body, flags=re.DOTALL)
    
    # Remove quoted text/forwarded content
    forwarded_patterns = [
        r'From:.*Sent:.*To:.*Subject:.*', # Outlook style
        r'-{5}Original Message-{5}', # Standard forwarded message
        r'On.*wrote:', # Gmail style reply
    ]
    
    for pattern in forwarded_patterns:
        # Instead of removing completely, we could mark these sections
        cleaned_body = re.sub(pattern, '[FORWARDED CONTENT] ', cleaned_body, flags=re.DOTALL)
    
    # Remove excessive whitespace
    cleaned_body = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_body)
    
    return cleaned_body.strip() 