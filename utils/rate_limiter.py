import time
from groq import RateLimitError

def safe_groq_call(func, *args,**kwargs):
    """
   Wrap groq api calls with retry+backoff
    """
    max_retries = 5
    delay = 2

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        
        except RateLimitError as e:
            print("Rate limit hit. Retyring in {delay} seconds...")
            time.sleep(delay)
            delay *=2
    raise Exception("Groq API failed after multiple retries.")