from pytube import YouTube

def download_youtube_video(video_url, output_path='.'):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream available
        video_stream = yt.streams.get_highest_resolution()

        # Download the video
        video_stream.download(output_path)

        print(f"Video downloaded successfully to {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage:
video_url = "https://www.youtube.com/watch?v=GCmiIaTCiNA"
output_path = "Audio"
download_youtube_video(video_url, output_path)
