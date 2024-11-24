import os
import subprocess
from tkinter import Tk, filedialog
import shutil


def merge_subtitles(video_path, srt_path):
    _, file_extension = os.path.splitext(video_path)
    file_extension = file_extension.lower()
    output_path = f"{os.path.splitext(video_path)[0]}_With_SRT{file_extension}"

    if file_extension == '.mp4':
        command = [
            'ffmpeg',
            '-i', video_path,
            '-i', srt_path,
            '-c', 'copy',
            '-c:s', 'mov_text',
            '-map', '0:v',
            '-map', '0:a',
            '-map', '1:s',
            output_path
        ]
    elif file_extension == '.mkv':
        command = [
            'ffmpeg',
            '-i', video_path,
            '-i', srt_path,
            '-c', 'copy',
            '-c:s', 'srt',
            '-map', '0:v',
            '-map', '0:a',
            '-map', '1:s',
            output_path
        ]
    elif file_extension == '.webm':
        command = [
            'ffmpeg',
            '-i', video_path,
            '-i', srt_path,
            '-c', 'copy',
            '-c:s', 'webvtt',
            '-map', '0:v',
            '-map', '0:a',
            '-map', '1:s',
            output_path
        ]
    elif file_extension == '.mov':
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'subtitles={srt_path}',
            '-c:v', 'libx264',
            '-c:a', 'copy',
            output_path
        ]
    else:
        print(f"❌ Unsupported video format: {file_extension}")
        return

    try:
        subprocess.run(command, check=True)
        print("✨ Subtitles merged successfully.")

        # Create DONE folder if it doesn't exist
        done_folder = "DONE"
        if not os.path.exists(done_folder):
            os.makedirs(done_folder)

        # Move the original video and subtitle files to the DONE folder
        shutil.move(video_path, os.path.join(done_folder, os.path.basename(video_path)))
        shutil.move(srt_path, os.path.join(done_folder, os.path.basename(srt_path)))
        print(f"📁 Moved original files to {done_folder} folder.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error merging subtitles: {e}")

def main():
    Tk().withdraw()  # Hide the main tkinter window

    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.mkv *.webm *.mov")])
    srt_path = filedialog.askopenfilename(title="Select Subtitle File", filetypes=[("Subtitle Files", "*.srt")])

    if video_path and srt_path:
        merge_subtitles(video_path, srt_path)
    else:
        print("❌ Video or subtitle file not selected.")

if __name__ == "__main__":
    main()



