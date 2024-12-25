from flask import Flask, render_template, request, send_file
import yt_dlp as youtube_dl
import os
import logging
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Path ffmpeg
FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# Root route
@app.route('/')
def index():
    return render_template('index.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Support route
@app.route('/support')
def support():
    return render_template('support.html')

# Download route
@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form.get('download_type', 'video')  # Cek apakah MP3 atau video

    # Opsi umum untuk yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(os.path.expanduser('~'), 'Downloads', '%(title)s.%(ext)s'),
        'ffmpeg_location': FFMPEG_PATH,
        'restrictfilenames': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
        }
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
    except Exception as e:
        app.logger.error(f"Error extracting info: {e}")
        return str(e)

    # Jika pengguna memilih download audio (MP3)
    if download_type == 'mp3':
        ydl_opts['format'] = 'bestaudio/best'  # Hanya unduh audio terbaik
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Ekstrak audio ke format MP3
            'preferredquality': '192',  # Kualitas 192 kbps
        }]

        try:
            # Unduh dan konversi file audio
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

                # Mencari nama file hasil unduhan yang tepat
                downloaded_file = os.path.join(os.path.expanduser('~'), 'Downloads', f"{info_dict['title']}.mp3")

                # Memastikan file berhasil diubah menjadi MP3 dan ada di direktori yang benar
                if os.path.exists(downloaded_file):
                    # Memperbaiki timestamp file ke tanggal saat ini
                    current_time = time.time()
                    os.utime(downloaded_file, (current_time, current_time))

                    # Kirim file ke browser untuk diunduh
                    return send_file(downloaded_file, as_attachment=True)
                else:
                    return "File MP3 tidak ditemukan setelah konversi."

        except Exception as e:
            app.logger.error(f"Error downloading audio: {e}")
            return str(e)

    # Jika pengguna memilih download video
    else:
        resolutions = []
        for f in info_dict.get('formats', []):
            if f.get('height'):
                resolution = {
                    'format_id': f['format_id'],
                    'format_note': f.get('format_note', 'Unknown'),
                    'ext': f['ext'],
                    'filesize': f.get('filesize', 'Unknown'),
                    'height': f['height']
                }
                resolutions.append(resolution)

        resolutions = sorted(resolutions, key=lambda x: x['height'])
        return render_template('choose_resolution.html', resolutions=resolutions, url=url)

# Route untuk mengunduh video dengan resolusi yang dipilih
@app.route('/download_video', methods=['POST'])
def download_video():
    url = request.form['url']
    format_id = request.form['format_id']

    download_path = os.path.join(os.path.expanduser('~'), 'Downloads', '%(title)s.%(ext)s')

    ydl_opts = {
        'format': format_id,
        'outtmpl': download_path,
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'  # Format yang diinginkan
        }],
        'merge_output_format': 'mp4',  # Gabungkan audio dan video ke dalam format MP4
        'noplaylist': True,  # Untuk menghindari pengunduhan playlist jika URL adalah playlist
        'verbose': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            downloaded_file = ydl.prepare_filename(ydl.extract_info(url, download=False))

            # Memperbaiki timestamp file ke tanggal saat ini
            current_time = time.time()
            os.utime(downloaded_file, (current_time, current_time))

            # Kirim file ke browser untuk diunduh
            return send_file(downloaded_file, as_attachment=True)

    except Exception as e:
        app.logger.error(f"Error downloading video: {e}")
        return str(e)  # Kembali ke string error untuk kemudahan debugging


# Jalankan server
if __name__ == '__main__':
    app.run(debug=True)
