import yt_dlp as youtube_dl
import os

def download_youtube_video(url, output_path='.'):
    try:
        # Create yt_dlp options
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'merge_output_format': 'mp4',  # Ensures merging video and audio into an MP4 file
        }

        # Download the video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print(f"Title: {info_dict.get('title')}")
            print(f"Views: {info_dict.get('view_count')}")
            print(f"Duration: {info_dict.get('duration')} seconds")
            print("Download completed!")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Get URL and output path from user
    url = input("Enter the YouTube video URL: ").strip()
    output_path = input("Enter the output path (leave empty for current directory): ").strip()

    if not output_path:
        output_path = '.'

    # Create the directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Download the video
    download_youtube_video(url, output_path)

if __name__ == "__main__":
    main()
