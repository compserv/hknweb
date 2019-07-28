# Sending reminder emails after a certain time has passed

# NOTE: The first two are dummy experiment tasks
def print_something():
    print("RUNNING CRON JOB")
    f = open("cron.txt", "w+")
    f.write("Cron job has run once")


def send_email():
    subject = 'Confirm Officer Challenge'
    officer_email = "alexanderwu68@yahoo.com"
    text_content = 'Confirm officer challenge'

    link = "www.google.com"
    html_content = render_to_string(
        'candidate/request_email.html',
        {
            'candidate_name' : "Harry Potter",
            'candidate_username' : "hp",
            'link' : link,
        }
    )
    msg = EmailMultiAlternatives(subject, text_content,
            'no-reply@hkn.eecs.berkeley.edu', [officer_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
