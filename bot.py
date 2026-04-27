import json, os, requests
#from datetime import date

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone

#today = datetime.date.today()
#today = date.today()
# Custom format: Day/Month/Year
#todaysDate = today.strftime("%d-%m-%Y")

def utc_to_ist():
    # Current UTC time
    utc_now = datetime.now(timezone.utc)
    # Convert to IST (UTC + 5:30)
    ist_now = utc_now + timedelta(hours=5, minutes=30)

    return ist_now

# Example usage
ist_time = utc_to_ist()
todaysDate = ist_time.date()

BOT_TOKEN = "8669021019:AAFg8lSIG0hmPOzC_O133VwAZ92JB7LyLCE"
CHAT_ID = "-1003971790115"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, data=payload)
    return r.json()

def send_job(company, role, location, link,postingdate):
    message = f"*{company}* \nHiring for *{role}* at *{location}* \n[Apply Link]: {link} \nPosted at : {postingdate}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"  # enables bold and links
    }
    r = requests.post(url, data=payload)
    print(r.json())

def load_sent():
    if os.path.exists("sent.json"):
        with open("sent.json") as f:
            #print(set(json.load(f)))
            return set(json.load(f))
        
    return set()

def save_sent(sent_ids):
    with open("sent.json", "w") as f:
        json.dump(list(sent_ids), f)

def process_jobs():
    
    url = "https://raw.githubusercontent.com/JaideepVerma/openings/main/output/data.json"
    jobs = requests.get(url).json()
    #path=jobs
    #with open(path) as f:   # replace with path or fetch from GitHub
    #    jobs = json.load(f)
    new_jobs=0
    sent_ids = load_sent()
    print((sent_ids))
    print('TodaysDate: ' ,todaysDate)
    print('Total jobs in data: ', len(jobs))
    for job in jobs:
        job_id = job["job_id"]  # must be unique per job
        job_company =job["company"]
        print(job_company+ ' ' + job_id not in sent_ids , job["posting_date"] == str(todaysDate) )
        if job_company+ ' ' + job_id not in sent_ids and job["posting_date"] == str(todaysDate): #"23-04-2026": 
            print('Loading...')
            send_job(job["company"], job["role"], job["location"], job["apply_link"],job["posting_date"])
            sent_ids.add(job_company+ ' ' + job_id)
            new_jobs +=1
            with open("jobs.log", "a") as log:
                log.write(f"Sent {job_company+ ' ' + job_id} at {datetime.datetime.now()}\n")
    print('<--------------  ',len(sent_ids), 'Posted to Telegram','---------------->')
    save_sent(sent_ids)

    # If no new jobs, post a heartbeat/status message
    if new_jobs == 0:
        #ist_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Get current UTC time
        #utc_now = datetime.datetime.now(timezone.utc)
        ist_time = utc_to_ist()
        utc_now = datetime.now(timezone.utc)
        # Add 5 hours 30 minutes
        ist_time = utc_now + timedelta(hours=5, minutes=30)
        ist_time=ist_time.strftime("%Y-%m-%d %H:%M:%S")
        send_message(f"🤖 Still waiting for companies to post vacancies.\nCarry on with your work — I’ll keep you posted! 😉 \n(last checked at {ist_time} IST)")

if __name__ == "__main__":
    process_jobs()
     
'''
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, data=payload)
    print(r.json())

send_message("Test message from my bot!")
'''
