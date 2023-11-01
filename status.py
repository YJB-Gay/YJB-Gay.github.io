import os
import json
import requests
from collections import Counter
from datetime import datetime, timedelta

logs_dir = "logs"
log_folder = "logs"
def get_most_recent_json_file():
    json_files = [f for f in os.listdir(logs_dir) if f.endswith(".json")]
    if json_files:
        return max(json_files, key=lambda x: os.path.getctime(os.path.join(logs_dir, x)))
    else:
        return None
def count_offline_entries(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        offline_count = sum(1 for entry in data['ip_status'] if entry['status'] == "offline")
        total_count = len(data['ip_status'])
        return offline_count, total_count
def main():
    global offline_count, total_count, json_url
    most_recent_json_file = get_most_recent_json_file()

    if most_recent_json_file:
        offline_count, total_count = count_offline_entries(os.path.join(logs_dir, most_recent_json_file))

        json_url = f"https://is-gaza.online/logs/{most_recent_json_file}"
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(script_directory)
    config_file_path = os.path.join(parent_directory, 'config.json')
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    
    discord_webhook_url = config["discord"]["webhook_url"]
    openweather_api_key = config["openweather"]["api_key"]
    # List all JSON files in the folder
    json_files = [f for f in os.listdir(log_folder) if f.endswith(".json")]
    
    # Sort the files by modification time and get the most recent one
    most_recent_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(log_folder, f)))
    
    # Read the most recent JSON file
    with open(os.path.join(log_folder, most_recent_file), 'r') as file:
        data = json.load(file)
    
    # Extract the 'status' field from each entry in 'ip_status'
    ip_statuses = [entry['status'] for entry in data['ip_status']]
    
    # Calculate the percentage of 'online' and 'offline' entries
    total_count = len(ip_statuses)
    status_counts = Counter(ip_statuses)
    online_percentage = (status_counts.get("online", 0) / total_count) * 100
    offline_percentage = (status_counts.get("offline", 0) / total_count) * 100
    
    # Determine the status and create the status message
    if online_percentage >= 20:
        status = "online"
        color = 0x57F287  # Green color for online
        emoji = "📱"
    else:
        status = "offline"
        color = 0xED4245  # Red color for offline
        emoji = "📵"
    
    offline_count = status_counts.get("offline", 0)
    with open("status.txt", "w") as file:
        file.write(status)
    
        # Make an API call to OpenWeather to get local weather in Gaza
    weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Gaza&appid={openweather_api_key}")
    weather_data = weather_response.json()
    temperature_kelvin = weather_data["main"]["temp"]
    temperature_celsius = temperature_kelvin - 273.15  # Convert to Celsius
    # Get the local time for Gaza (assuming UTC+2)
    current_time = datetime.utcnow() + timedelta(hours=2)
    time_str = current_time.strftime("%H:%M:%S %Z\n%A, %d %B %Y")
    temperature_str = f"{temperature_celsius:.1f} °C"
    
    # Create the Discord message payload
    discord_payload = {
        "content": None,
        "embeds": [
            {
                "title": f"{online_percentage:.2f}% Online {emoji}",
                "description": f"Offline: {offline_count} / {total_count}",
                "color": color,
                "fields": [
                    {
                        "name": "Local Time and Weather",
                        "value": f"```\n{time_str}\n\n{temperature_str}\n```"
                    }
                ],
                "author": {
                    "name": "Gaza IP Address Status",
                    "url": "https://is-gaza.online/",
                    "icon_url": "https://i.imgur.com/cIbuRkt.png"
                }
            }
        ],
        "attachments": []
    }
    
    # Your Discord webhook URL
    webhook_url = discord_webhook_url
    tweet_file_path = os.path.join("E:\\Nicholas\\Downloads\\gaza_ip_test", 'tweet.txt')
    # Your tweet text
    tweet_text = f"Gaza is currently {status}.\n" \
                 f"{online_percentage:.2f}% Online\n" \
                 f"Offline: {offline_count} / {total_count}\n" \
                 f"Logs: {json_url}"
    
    
    # Write the tweet text to the correct file path
    with open(tweet_file_path, 'w', encoding='utf-8') as file:
        file.write(tweet_text)
    
    # Send the payload to the Discord webhook
    response = requests.post(webhook_url, json=discord_payload)# Check if the message was sent successfully
    if response.status_code == 204:
        print("Message sent to Discord successfully")
    else:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")