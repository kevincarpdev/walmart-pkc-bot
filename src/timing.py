import asyncio
from datetime import datetime
import pytz

def get_target_time(time_str, timezone="US/Eastern"):
    """
    Parses HH:MM:SS and returns a datetime object for today in the given timezone.
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    target_dt = datetime.strptime(time_str, "%H:%M:%S").time()
    return tz.localize(datetime.combine(now.date(), target_dt))

async def wait_until(target_time):
    """
    Sleeps until the target datetime is reached.
    """
    tz = target_time.tzinfo
    while True:
        now = datetime.now(tz)
        diff = (target_time - now).total_seconds()
        
        if diff <= 0:
            break
            
        # Precise sleep for the last 5 seconds to reduce CPU but maintain accuracy
        if diff > 5:
            await asyncio.sleep(diff - 5)
        else:
            await asyncio.sleep(0.01)
    
    print(f"Target time {target_time} reached at {datetime.now(tz)}")
