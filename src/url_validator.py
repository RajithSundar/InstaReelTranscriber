"""
URL Validator Module
Validates Instagram Reel URLs and checks accessibility
"""

import re
import validators
import requests
from typing import Dict, Tuple
from config import INSTAGRAM_REEL_PATTERN, USER_AGENT


class URLValidator:
    def __init__(self):
        # Regex to match instagram reel URLs
        self.pattern = re.compile(INSTAGRAM_REEL_PATTERN)
    
    def validate(self, url):
        # Check if URL looks like a URL
        if not validators.url(url):
            return False, "", "That doesn't look like a URL"
        
        # Check if it matches Instagram pattern
        match = self.pattern.match(url)
        if not match:
            return False, "", "Not an Instagram Reel URL!"
        
        reel_id = match.group(1)
        
        # Check if the link actually works
        try:
            headers = {'User-Agent': USER_AGENT}
            # Just get the header info, don't download whole page
            response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.status_code == 404:
                return False, "", "Video not found (404)!"
            elif response.status_code >= 500:
                return False, "", "Instagram is having issues (500)"
            
            return True, reel_id, ""
            
        except requests.exceptions.Timeout:
            return False, "", "Request timed out"
        except requests.exceptions.ConnectionError:
            return False, "", "Connection error"
        except Exception as e:
            return False, "", f"Network error: {str(e)}"
    
    def extract_reel_id(self, url):
        match = self.pattern.match(url)
        if match:
            return match.group(1)
        return ""


# Convenience function
def validate_instagram_url(url: str) -> Tuple[bool, str, str]:
    """
    Validate Instagram Reel URL
    
    Args:
        url: Instagram Reel URL to validate
        
    Returns:
        Tuple of (is_valid, reel_id, error_message)
    """
    validator = URLValidator()
    return validator.validate(url)
