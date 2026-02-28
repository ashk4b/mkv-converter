import os
import subprocess
import argparse
from pathlib import Path


def convert_mkv_to_hls(input_file, output_dir):
    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    master_playlist = os.path.join(output_dir, 'master.m3u8')
    segment_pattern = os.path.join(output_dir, 'chunk_%03d.ts')

    # The FFmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,  # Input file
        '-c:v', 'libx264',  # Video codec: H.264 (Universally supported in browsers)
        '-crf', '23',  # Video Quality: 23 is a great balance of quality/size
        '-preset', 'fast',  # Encoding speed: 'fast' is good for local testing
        '-c:a', 'aac',  # Audio codec: AAC (Universally supported)
        '-b:a', '128k',  # Audio bitrate
        '-ac', '2',  # Audio channels: Mixdown to stereo (safe for web)
        '-hls_time', '10',  # HLS: Target length of each chunk in seconds
        '-hls_playlist_type', 'vod',  # HLS: Video On Demand (adds an end tag to the playlist)
        '-hls_segment_filename', segment_pattern,
        master_playlist
    ]

    print(f"Starting conversion for: {input_file}")
    print(f"Outputting to: {output_dir}")
    print("Running FFmpeg... Grab a coffee, this might take a while depending on your CPU!\n")

    try:
        # Run the command. Output will stream directly to your terminal.
        subprocess.run(command, check=True)
        print("\n✅ Conversion completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during conversion. FFmpeg exited with code {e.returncode}.")
    except FileNotFoundError:
        print("\n❌ FFmpeg is not installed or not in your system's PATH.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert MKV to HLS format for web streaming.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input MKV file')
    parser.add_argument('-o', '--output', required=True, help='Name of the output folder (e.g., movies/inception)')

    args = parser.parse_args()
    convert_mkv_to_hls(args.input, args.output)