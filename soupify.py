import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, jsonify
from threading import Thread
import configparser
from pyngrok import ngrok
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
donations = None

def update_value(url, html_div_type, html_class, sleep_time):
    global donations
    while True:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        value_element = soup.find(html_div_type, class_=html_class)
    
        new_donation_value = value_element.text.strip() if value_element else None
        if new_donation_value and new_donation_value != donations:
            donations = new_donation_value

        print(donations)

        time.sleep(sleep_time)

@app.route("/values") # Gets called when /value is accessed
def get_value():
    return jsonify({"donations": donations})

def main():
    # Read in config
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except configparser.Error as e:
        print(f"Error reading config file: {e}")

    if 'Website_Values' in config:
        url = config['Website_Values'].get('url')
        html_div_type = config['Website_Values'].get('html_div_type', fallback='h1')
        html_class = config['Website_Values'].get('html_class')
    
    if 'Run_Values' in config:
        sleep_time = config['Run_Values'].getint('sleep_time', fallback = 30)

    if 'Flask_Values' in config:
        host = config['Flask_Values'].get('host', fallback = "0.0.0.0")
        port = config['Flask_Values'].getint('port', fallback = 8080)

    # Scraping Thread
    Thread(target=update_value, daemon=True, args=(url, html_div_type, html_class, sleep_time)).start()
    
    #public_url = ngrok.connect(port) --> Removed to change to Render
    #print("Public URL:", public_url)

    #Start Flask app
    app.run(host=host, port=port) 
    
if __name__ == "__main__":
    main()
