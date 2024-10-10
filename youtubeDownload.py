import os
import subprocess
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save

def download_video(url, format_choice):
    output_path = "downloads"

    # Ensure the downloads directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if format_choice == "mp3" or format_choice == "midi":
        # Download as MP3
        download_command = [
            "yt-dlp",
            "-x", "--audio-format", "mp3", url,
            "-o", os.path.join(output_path, "%(title)s.%(ext)s")
        ]
        subprocess.run(download_command)
        print("Downloaded as MP3.")
        
        # Find the downloaded MP3 file
        for file in os.listdir(output_path):
            if file.endswith(".mp3"):
                mp3_file = os.path.join(output_path, file)

                if format_choice == "midi":
                    wav_file = convert_mp3_to_wav(mp3_file)
                    convert_wav_to_midi(wav_file)
                break
    
    elif format_choice == "mp4":
        # Download as MP4
        download_command = [
            "yt-dlp",
            "-f", "mp4", url,
            "-o", os.path.join(output_path, "%(title)s.%(ext)s")
        ]
        subprocess.run(download_command)
        print("Downloaded as MP4.")
    else:
        print("Invalid choice. Please select mp3, mp4, or midi.")

def convert_mp3_to_wav(mp3_file):
    """Converts an MP3 file to WAV using ffmpeg."""
    wav_file = mp3_file.replace(".mp3", ".wav")
    command = [
        "ffmpeg", "-i", mp3_file, wav_file
    ]
    subprocess.run(command)
    print(f"Converted {mp3_file} to WAV: {wav_file}")
    return wav_file

def convert_wav_to_midi(wav_file):
    """Uses Basic Pitch to convert the WAV file to MIDI."""
    print(f"Converting {wav_file} to MIDI using Basic Pitch...")

    # Specify the output MIDI file name
    midi_output_dir = "midi_outputs"
    if not os.path.exists(midi_output_dir):
        os.makedirs(midi_output_dir)

    # Use the ICASSP_PRETRAINED_MODEL_PATH
    model_or_model_path = ICASSP_2022_MODEL_PATH

    # Call predict_and_save with the required parameters
    predict_and_save(
        [wav_file],                           # List of WAV files to process
        output_directory=midi_output_dir,     # Directory to save output files
        save_midi=True,                       # Save MIDI file
        sonify_midi=False,                    # Do not create a sonification of the MIDI
        save_model_outputs=False,             # Do not save internal model outputs
        save_notes=True,                      # Save the notes as a JSON file
        model_or_model_path=model_or_model_path  # Use the ICASSP model path
    )

    print(f"MIDI file saved to {midi_output_dir}.")

if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    format_choice = input("Enter the format (mp3, mp4, midi): ").lower()
    download_video(url, format_choice)
