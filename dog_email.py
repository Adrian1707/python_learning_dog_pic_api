import os
import requests
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def get_dog_image_url():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    if response.status_code == 200:
        data = response.json()
        return data["message"]
    else:
        raise Exception("Error fetching dog image URL")

def send_email_with_dog_image(api_key, api_secret, from_email, to_email):
    dog_image_url = get_dog_image_url()
    dog_image_response = requests.get(dog_image_url)

    if dog_image_response.status_code != 200:
        raise Exception("Error fetching dog image")

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Dog CEO Image"

    text = MIMEText("Here's a random dog image from Dog CEO API.")
    msg.attach(text)

    img_data = dog_image_response.content
    image = MIMEImage(img_data, name="dog_image.jpg")
    msg.attach(image)

    email_data = {
        "Messages": [
            {
                "From": {
                    "Email": from_email
                },
                "To": [
                    {
                        "Email": to_email
                    }
                ],
                "Subject": msg["Subject"],
                "TextPart": text.get_payload(),
                "Attachments": [
                    {
                        "ContentType": "image/jpeg",
                        "Filename": "dog_image.jpg",
                        "Base64Content": base64.b64encode(img_data).decode("utf-8")
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64.b64encode(f'{api_key}:{api_secret}'.encode('utf-8')).decode('utf-8')}"
    }

    response = requests.post("https://api.mailjet.com/v3.1/send", json=email_data, headers=headers)
    print(response)
    if response.status_code != 200:
        print(f"Error sending email via Mailjet API. Status code: {response.status_code}")
        print(f"Response content: {response.content}")
        raise Exception("Error sending email via Mailjet API")

if __name__ == "__main__":
    MAILJET_API_KEY = os.environ["MAILJET_API_KEY"]
    MAILJET_API_SECRET = os.environ["MAILJET_API_SECRET"]
    FROM_EMAIL = os.environ["FROM_EMAIL"]
    TO_EMAIL = os.environ["TO_EMAIL"]

    send_email_with_dog_image(MAILJET_API_KEY, MAILJET_API_SECRET, FROM_EMAIL, TO_EMAIL)
    print("Email with dog image sent successfully!")
