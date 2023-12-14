import string


SHORT_LINK_DEFAULT_CHARS = string.ascii_letters + string.digits
SHORT_LINK_DEFAULT_LENGTH = 6
SHORT_LINK_MAX_LENGTH = 16
SHORT_LINK_REGEXP = r'\s*[_0-9a-zA-Z]{1,16}\s*$'
