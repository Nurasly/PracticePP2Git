from datetime import datetime, timedelta

# Current date
today = datetime.now()          # or datetime.today()
five_days_ago = today - timedelta(days=5)

print("Today:         ", today.strftime("%Y-%m-%d"))
print("Five days ago: ", five_days_ago.strftime("%Y-%m-%d"))


from datetime import datetime, timedelta

today = datetime.now().date()    # .date() to keep only date part

yesterday = today - timedelta(days=1)
tomorrow  = today + timedelta(days=1)

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:    ", today.strftime("%Y-%m-%d"))
print("Tomorrow: ", tomorrow.strftime("%Y-%m-%d"))


from datetime import datetime

now = datetime.now()

# Method 1 – most readable
now_no_micro = now.replace(microsecond=0)

# Method 2 – using floor (Python 3.7+)
# now_no_micro = now - timedelta(microseconds=now.microsecond)

# Method 3 – string formatting (very common for display)
now_no_micro_str = now.strftime("%Y-%m-%d %H:%M:%S")

print("With microseconds:   ", now)
print("Without microseconds:", now_no_micro)
print("Formatted:           ", now_no_micro_str)

from datetime import datetime

# Option A: two specific dates
date1 = datetime(2025, 2, 17, 8, 0, 0)
date2 = datetime(2025, 2, 20, 14, 30, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print(f"Difference: {difference}")
print(f"In seconds: {seconds:.0f}")

