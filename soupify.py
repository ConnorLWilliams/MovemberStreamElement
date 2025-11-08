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
target = None

startup_flag = True

def update_value(url, donations_html_div_type, donations_html_class, target_html_div_type, target_html_class, sleep_time):
    global donations
    global target

    while True:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        
        donations_value_element = soup.find(donations_html_div_type, class_=donations_html_class)
        target_value_element = soup.find(target_html_div_type, id=target_html_class)

        new_donation_value = donations_value_element.text.strip() if donations_value_element else None
        if new_donation_value and new_donation_value != donations:
            donations = new_donation_value

        new_target_value = target_value_element.text.strip() if target_value_element else None
        if new_target_value and new_target_value != target:
            target = new_target_value.split("$")[1]

        print(donations)
        print(target)

        time.sleep(sleep_time)

@app.route("/values") # Gets called when /value is accessed
def get_value():
    return jsonify({"donations": donations,
                    "target": target})

def main():
    # Read in config
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except configparser.Error as e:
        print(f"Error reading config file: {e}")

    if 'Website_Values' in config:
        url = config['Website_Values'].get('url')
        donations_html_div_type = config['Website_Values'].get('donations_html_div_type', fallback='h1')
        donations_html_class = config['Website_Values'].get('donations_html_class')
        
        target_html_div_type = config['Website_Values'].get('target_html_div_type', fallback='h1')
        target_html_class = config['Website_Values'].get('target_html_class')
    
    if 'Run_Values' in config:
        sleep_time = config['Run_Values'].getint('sleep_time', fallback = 30)

    if 'Flask_Values' in config:
        host = config['Flask_Values'].get('host', fallback = "0.0.0.0")
        port = config['Flask_Values'].getint('port', fallback = 8080)

    # Scraping Thread
    Thread(target=update_value, daemon=True, args=(url, donations_html_div_type, donations_html_class, target_html_div_type, target_html_class, sleep_time)).start()
    
    #public_url = ngrok.connect(port) --> Removed to change to Render
    #print("Public URL:", public_url)

    #Start Flask app
    if __name__=="__main__":
        app.run(host=host, port=port) 

@app.before_request
def startup():
    global startup_flag
    if startup_flag:
        startup_flag = False
        main()

if __name__=="__main__":
    main()

