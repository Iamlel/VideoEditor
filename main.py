from pytube import YouTube
import json, os, random, threading
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, ImageClip, CompositeVideoClip, clips_array

WORKING_DIR = "videos"

with open("./assets.json", "r") as fp:
    VAR = json.load(fp)

def downloadVideo(id):
    yt = YouTube("https://www.youtube.com/watch?v="+id)
    id = "Y" + id

    yt.streams.filter(mime_type="audio/mp4").order_by("abr").last().download(output_path=f"./{WORKING_DIR}/id}/", filename=id+"a.mp4")
    yt.streams.filter(mime_type="video/mp4").order_by("resolution").last().download(output_path=f"./{WORKING_DIR}/{id}/", filename=id+"v.mp4")

    with open(os.path.join(f"./{WORKING_DIR}/{id}/", "".join(x for x in yt.title if x == ' ' or x.isalnum())), 'w'):
        pass

    print("Finished downloading "+id[1:])
    return id

def combineAudioVideo(key):
    vid = VideoFileClip(f"./{WORKING_DIR}/{key}/{key}v.mp4")
    aud = AudioFileClip(f"./{WORKING_DIR}/{key}/{key}a.mp4")

    vid.audio = CompositeAudioClip([aud])
    return vid

def resizeVideo(vid):
    if (vid.size != (1920, 1080)):
        vid = vid.resize((1920, 1080))
    return vid.resize(0.5).crop(x1 = 176, x2 = 784)

def getBackgroundClip(duration):
    background = VAR.get("assets")

    backgroundclip = random.choice(background)
    backgroundclip = VideoFileClip(f"./assets/{backgroundclip}/{backgroundclip}.mp4")

    background_dur = random.randrange(int(backgroundclip.duration - duration))
    return backgroundclip.subclip(background_dur, background_dur + duration)

def saveVideo(key, final_vid, dur_secs = 210): # 3:30 minutes
    if (final_vid.duration <= dur_secs):
        final_vid = clips_array([[final_vid], [getBackgroundClip(final_vid.duration)]])
        final_vid.write_videofile(f"./{WORKING_DIR}/{key}/{key}.mp4")

    else:
        final_vid = CompositeVideoClip([final_vid, ImageClip("./text_assets/part.png").set_duration(final_vid.duration)])

        for x in range(int(final_vid.duration // dur_secs + (final_vid.duration % 210 != 0))):
            current_vid = final_vid.subclip(dur_secs * x, min(dur_secs * x + dur_secs, int(final_vid.duration)))
            part_text = ImageClip(f"./text_assets/{x + 1}.png").set_pos((350 - 13, 140))

            current_vid = clips_array([[current_vid], [getBackgroundClip(current_vid.duration)]])
            current_vid = CompositeVideoClip([current_vid, part_text.set_duration(current_vid.duration)])

            current_vid.write_videofile(f"./{WORKING_DIR}/{key}/{key}-{x}.mp4")

def prepareVideo(vid):
    vid = downloadVideo(vid)
    saveVideo(vid, resizeVideo(combineAudioVideo(vid)))

def main(videos, saferun = True):
    if saferun:
        with open("used.json", "r") as fp:
            usedVideos = json.load(fp)
            videos = list(filter(lambda i: i not in usedVideos, videos))

    threads = []
    for vid in videos:
        t = threading.Thread(target=prepareVideo, args=(vid,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    print("Completed all the videos.")

    if saferun:
        with open("used.json", "w") as fp:
            json.dump(usedVideos + videos, fp)
        print("Dumped all the ids of the used videos.")

def purge():
    for (dirpath, dirnames, filenames) in os.walk("./{WORKING_DIR}/"):
        for filename in filenames:
            if "v.mp4" in filename or "a.mp4" in filename:
                os.remove(os.path.join(dirpath, filename))
    print("Purged all of the temporary files.")

def setup():
    for (dirpath, dirnames, filenames) in os.walk("./assets/"):
        for filename in filenames:
            if not "new_" in filename:
                clip = VideoFileClip(f"{dirpath}/{filename}")
                clip = clip.resize(0.5).crop(x1=176, x2=784)
                clip.write_videofile(f"{dirpath}/new_{filename}")
    print("Completed resizing all fo the assets.")
