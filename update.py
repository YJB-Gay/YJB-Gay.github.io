import json

# Read data from cache.json
with open('cache.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Extract the URLs from cache.json
txt_url = data["txt_url"]
json_url = data["json_url"]
count = data.get("count")
# Full HTML content including CSS and JavaScript
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Gaza Internet Watch</title>
    <meta name="description" content="Based on 2,437 IPs in the Gaza Strip">
    <meta property="og:title" content="Gaza Internet Watch">
    <meta property="og:description" content="Based on 2,437 IPs in the Gaza Strip">
    <meta property="og:image" content="https://files.catbox.moe/4ledo4.jpg">
<head>
    <title>Gaza Internet Watch</title>
    <style>
        body {{
            background-image: url('https://files.catbox.moe/26caxg');
            background-size: cover;
            backdrop-filter: blur(0px);
            color: #ffffff;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        h1 {{
            font-size: 72px; /* 3x bigger */
        }}
        p {{
            font-size: 48px; /* Same size as Online/Offline text */
        }}
        #status {{
            font-size: 72px; /* 3x bigger */
            color: green;
        }}
        #status.offline {{
            color: red;
        }}
        #additional-info {{
            font-size: 24px; /* Smaller text */
        }}
        #more-info {{
            font-size: 18px; /* Even smaller text */
        }}
        #donate-button {{
            background-color: #0074d9;
            color: #ffffff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            position: fixed;
            bottom: 20px;
            left: 20px;
        }}
        #image-credit {{
            color: #ffffff;
            text-decoration: none;
            position: absolute;
            bottom: 20px;
            right: 20px;
        }}
        #contact-button {{
            background-color: #0074d9;
            color: #ffffff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            position: fixed;
            bottom: 70px;
            left: 20px;
        }}
        
    </style>
    <script>
        function checkStatus() {{
            fetch('{txt_url}')
                .then(response => response.text())
                .then(data => {{
                    if (data.trim() === 'online') {{
                        document.getElementById('status').textContent = 'Online';
                    }} else {{
                        document.getElementById('status').textContent = 'Offline';
                        document.getElementById('status').classList.add('offline');
                    }}
                }})
                .catch(error => {{
                    document.getElementById('status').textContent = 'Error';
                    document.getElementById('status').classList.add('offline');
                }});
        }}
    </script>
</head>
<body style="margin: 0; padding: 0;">
    <h1 style="margin: 0;">Gaza Internet</h1>
    <p style="margin: 0;">Status: <span id="status">Checking...</span></p>
    <p id="count" style="font-size: 24px; margin: 0; padding: 0; line-height: 1.2;">Offline Count: {count}</p>
    <p style="margin: 0;">Based on 2,437 IPs in the Gaza Strip</p>
    <p style="margin: 0;"><a href="{json_url}">Logs</a></p>
    
    <div>
        <a id="donate-button" href="/donate/">Donate To Save Gaza</a>
        <a id="image-credit" href="https://www.instagram.com/alijadallah66">Image credit Ali Jadallah - علي جادالله</a>
        <a id="contact-button" href="mailto:contact@is-gaza.online">Contact</a>
    </div>
    
    </div>
    <script>
        checkStatus();
    </script>
</body>
</html>
"""

# Save the HTML content to index.html with UTF-8 encoding
with open('index.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print("HTML file updated successfully.")
