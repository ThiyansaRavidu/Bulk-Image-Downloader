from flask import Flask, render_template, request, send_from_directory, url_for
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'output_media'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

MEDIA_TYPES = {
    'jpg': ['image/jpeg'],
    'png': ['image/png'],
    'mp3': ['audio/mpeg'],
}

def download_media_from_url(url, media_type):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        media_files = []

        if media_type in ['jpg', 'png']:
            tags = soup.find_all('img')
            media_files = [tag.get('src') for tag in tags if tag.get('src') and any(m in tag.get('src') for m in MEDIA_TYPES[media_type])]
        elif media_type == 'mp3':
            tags = soup.find_all('audio')
            media_files = [tag.get('src') for tag in tags if tag.get('src') and any(m in tag.get('src') for m in MEDIA_TYPES[media_type])]
        else:
            tags = soup.find_all(['img', 'audio'])
            media_files = [tag.get('src') for tag in tags if tag.get('src')]

        downloaded_files = []
        for media_url in media_files:
            full_url = urljoin(url, media_url)
            media_name = secure_filename(full_url.split('/')[-1])
            media_path = os.path.join(app.config['UPLOAD_FOLDER'], media_name)

            try:
                media_data = requests.get(full_url).content
                with open(media_path, 'wb') as f:
                    f.write(media_data)
                downloaded_files.append(media_name)
            except Exception as e:
                print(f"Error downloading {full_url}: {e}")

        return downloaded_files

    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    media_files = []
    if request.method == 'POST':
        url = request.form['url']
        media_type = request.form.get('media_type', 'all')
        media_files = download_media_from_url(url, media_type)
        if isinstance(media_files, str):
            message = media_files
            media_files = []
        else:
            message = f'{len(media_files)} media files downloaded successfully!'
    
    return render_template('index.html', message=message, media_files=media_files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if os.name == 'nt':
        os.system('mode con: cols=120 lines=30')

    GREEN = "\033[92m"
    RESET = "\033[0m"

    # Main banner
    banner = r"""
 ██ ▄█▀ █    ██ ▓█████▄ ▓█████▄  ▄▄▄          ▄▄▄▄    █    ██  ██▓     ██ ▄█▀   ▓█████▄  ▒█████   █     █░███▄    █  ██▓     ▒█████  ▓█████▄ ▓█████  ██▀███  
 ██▄█▒  ██  ▓██▒▒██▀ ██▌▒██▀ ██▌▒████▄       ▓█████▄  ██  ▓██▒▓██▒     ██▄█▒    ▒██▀ ██▌▒██▒  ██▒▓█░ █ ░█░██ ▀█   █ ▓██▒    ▒██▒  ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▓███▄░ ▓██  ▒██░░██   █▌░██   █▌▒██  ▀█▄     ▒██▒ ▄██▓██  ▒██░▒██░    ▓███▄░    ░██   █▌▒██░  ██▒▒█░ █ ░█▓██  ▀█ ██▒▒██░    ▒██░  ██▒░██   █▌▒███   ▓██ ░▄█ ▒
▓██ █▄ ▓▓█  ░██░░▓█▄   ▌░▓█▄   ▌░██▄▄▄▄██    ▒██░█▀  ▓▓█  ░██░▒██░    ▓██ █▄    ░▓█▄   ▌▒██   ██░░█░ █ ░█▓██▒  ▐▌██▒▒██░    ▒██   ██░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
▒██▒ █▄▒▒█████▓ ░▒████▓ ░▒████▓  ▓█   ▓██▒   ░▓█  ▀█▓▒▒█████▓ ░██████▒▒██▒ █▄   ░▒████▓ ░ ████▓▒░░░██▒██▓▒██░   ▓██░░██████▒░ ████▓▒░░▒████▓ ░▒████▒░██▓ ▒██▒
▒ ▒▒ ▓▒░▒▓▒ ▒ ▒  ▒▒▓  ▒  ▒▒▓  ▒  ▒▒   ▓▒█░   ░▒▓███▀▒░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ▒▒ ▓▒    ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒ ░ ▒░   ▒ ▒ ░ ▒░▓  ░░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒ ▒░░░▒░ ░ ░  ░ ▒  ▒  ░ ▒  ▒   ▒   ▒▒ ░   ▒░▒   ░ ░░▒░ ░ ░ ░ ░ ▒  ░░ ░▒ ▒░    ░ ▒  ▒   ░ ▒ ▒░   ▒ ░ ░ ░ ░░   ░ ▒░░ ░ ▒  ░  ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
░ ░░ ░  ░░░ ░ ░  ░ ░  ░  ░ ░  ░   ░   ▒       ░    ░  ░░░ ░ ░   ░ ░   ░ ░░ ░     ░ ░  ░ ░ ░ ░ ▒    ░   ░    ░   ░ ░   ░ ░   ░ ░ ░ ▒   ░ ░  ░    ░     ░░   ░ 
░  ░      ░        ░       ░          ░  ░    ░         ░         ░  ░░  ░         ░        ░ ░      ░            ░     ░  ░    ░ ░     ░       ░  ░   ░     
                 ░       ░                         ░                             ░                                                    ░                      
    """
    
    # New text art banner
    creator_banner = r"""
               Made by Thiyansa Ravidu
    """

    print(f"{GREEN}{banner}{RESET}")
    print(f"{GREEN}{creator_banner}{RESET}")
    app.run(debug=True)
