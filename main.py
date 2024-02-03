from data_manager import Data_manager
from manag_flights import Find_flight
import os
import smtplib



manga_data = Data_manager()
flights = Find_flight()
flights.search_flight()

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("EMAIL_PASSWORD")
        



if len(flights.destination_dict) > 0:
    for x in flights.destination_dict:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            # Encode the message using UTF-8
            subject = "There is a cheap flight"
            body = f"Hello, there is a flight from {x['cityFrom']} to {x['cityTo']}.\nPrice: {x['price']}€\nSee details at: {x['link']}"
            msg = f"Subject: {subject}\n\n{body}"

            connection.sendmail(
                from_addr=my_email,
                to_addrs="merabtoduapy@gmail.com",
                msg=msg.encode('utf-8')
            )

    print("Email sent to merabtoduapy@gmail.com")
      





