import time

def format_time(seconds):
    """
    Format detik menjadi MM:SS
    """
    return time.strftime("%M:%S", time.gmtime(seconds))
