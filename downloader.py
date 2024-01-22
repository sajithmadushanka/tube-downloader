# -*- coding: utf-8 -*-  # Explicitly declare UTF-8 encoding

import os
import locale  # Import for locale information

os.environ['PYTHONIOENCODING'] = 'utf-8'  # Set environment variable for I/O encoding

from pytube import YouTube

def downloade_runner(url, format="mp3"):
    """Downloads the highest quality audio or video stream from a YouTube video
    in the specified format (mp3 or mp4).

    Args:
        url (str): The URL of the YouTube video.
        format (str, optional): The desired format to download, either "mp3" or "mp4".
            Defaults to "mp3".

    Raises:
        Exception: If errors occur during the download process.
    """

    try:
        locale.setlocale(locale.LC_ALL, '')  # Set locale for correct encoding

        yt = YouTube(url)

        if format == "mp3":
            # Prioritize MP3 streams, but consider other audio formats if not available
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            if not stream:
                print(f"MP3 stream not found, selecting the highest quality audio stream available.")
                stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        else:
            # Select the highest quality video stream
            stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()

        # Download the selected stream
        stream.download()

        # Convert to MP3 if necessary and format is "mp3"
        if format == "mp3" and not stream.default_filename.lower().endswith(".mp3"):
            import moviepy.editor as mp

            audio_file = stream.default_filename
            mp3_file = os.path.splitext(audio_file)[0] + '.mp3'

            clip = mp.AudioFileClip(audio_file)
            clip.write_audiofile(mp3_file)

            os.remove(audio_file)  # Remove the original audio file

            print(f"Audio converted to MP3 and saved as: {mp3_file}")
        else:
            print(f"Download complete! File format: {stream.default_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


