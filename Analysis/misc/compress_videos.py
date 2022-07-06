import os
from glob import glob
import cv2
from PIL import Image
import ffmpeg
from tqdm import tqdm


#vid_paths = sorted(glob(os.path.join('./billiards_app/static/videos/revised', '*.mp4')))
vid_paths = sorted(glob(os.path.join('../../Studies/Experiment_4/tower_app4/static/stim_vids/', '*.mp4')))
outpath = '../../Studies/Experiment_4/tower_app4/static/stim_vids/gifs'

def convertVid_toimg(path):
    filename = path.split('/')[-1]
    cap = cv2.VideoCapture(path)
    still_reading, image = cap.read()
    frame_count = 0
    while still_reading:
        cv2.imwrite(f'{outpath}/{filename}_frame_{frame_count:03d}.jpg', image)
        still_reading, image = cap.read()
        frame_count += 1


def img_toGif(filename):
    filename = filename.split('.')[0]
    images = glob(os.path.join(f"{outpath}", f"{filename}*.jpg"))
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(outpath+filename+".gif", format="GIF", append_images=frames,
                   save_all=True, duration=32, loop=0, optimized=True)
    [os.remove(framefile) for framefile in
     glob(os.path.join(outpath, filename + "*.jpg"))]


def compress_video(video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = 0 #float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()


# reduce the file sizes
for vid in tqdm(vid_paths):
    filename = vid.split('/')[-1].split('.')[0]
    print(f'compressing video: {filename}')
    compress_video(vid, f'{outpath}/{filename}.mp4', 50 * 1000)

# make gifs
for p in tqdm(vid_paths):
    convertVid_toimg(p)
    filename = p.split('/')[-1]
    img_toGif(filename)