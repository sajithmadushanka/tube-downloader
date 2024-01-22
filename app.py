from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube.exceptions import RegexMatchError
from downloader import downloade_runner

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download():
    try:
        # Get parameters from the request's query string
        url = request.args.get('url')
        format = request.args.get('format', 'mp3')

        # Call the downloade_runner function
        downloade_runner(url, format)

        # Assume the downloaded file is named 'output.mp3' or 'output.mp4'
        output_file = f'output.{format}'

        return send_file(
            output_file,
            as_attachment=True,
            download_name=f'download.{format}'  # Change the download_name to your desired filename
        )

    except RegexMatchError:
        return jsonify({"status": "error", "message": "Invalid YouTube URL."})

    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
