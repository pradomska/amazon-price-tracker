from bs4 import BeautifulSoup
import requests
import smtplib

TARGET_PRICE = 100
AMAZON_URL = "https://www.amazon.com/dp/B08PQ2KWHS?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

MY_EMAIL = "example@outlook.com"
MY_PASSWORD = "******"

headers = { 'Accept-Language': "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

response = requests.get(AMAZON_URL, headers=headers)
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
# print(soup.prettify())
price = float(soup.find(name="span", class_="a-offscreen").getText().split("$")[1])
# print(price)

title = soup.find(id="productTitle").getText().strip()
# print(title)

if price < TARGET_PRICE:
    with smtplib.SMTP("smtp-mail.outlook.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{title} is now ${price}\n{AMAZON_URL}".encode("UTF-8"))
