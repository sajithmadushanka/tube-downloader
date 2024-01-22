from flask import Flask, request, jsonify
from pytube.exceptions import RegexMatchError
from downloader import downloade_runner
from flask_cors import CORS 
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

        return jsonify({"status": "success", "message": "Download completed successfully."})

    except RegexMatchError:
        return jsonify({"status": "error", "message": "Invalid YouTube URL."})

    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)