
# VideoEditor
Turns a youtube video into a video you can upload on tiktok or youtube shorts, by adding random clips at the bottom, and scaling the video correctly.

The output video is 608x1080px -- with the video being resized and transformed to fit in a 608x540px frame, and the random clip using up the rest of the 608x540px frame below it.
The text centered in the middle, and the number is put next to the "Part" text. However, **double digit numbers are not supported currently**.

## Examples
![Output Video Screenshot](https://github.com/Iamlel/VideoEditor/blob/main/examples/output.png)

[Download Sample Output Video](https://github.com/Iamlel/VideoEditor/raw/main/examples/sample.mp4)

[Original Video Credit](https://www.youtube.com/watch?v=1KZSGLEgmmU)

## Usage
Below the five functions that you will probably want to use from `main.py` are explained.
 - setup()
 - purge()
 - prepareVideo(vid)
 - downloadVideo(id)
 - main(videos, saferun = True)

### Setup()
    for (dirpath, dirnames, filenames) in os.walk("./assets/"):
        for filename in filenames:
            if not "new_" in filename:
                clip = VideoFileClip(f"{dirpath}/{filename}")
                clip = clip.resize(0.5).crop(x1=176, x2=784)
                clip.write_videofile(f"{dirpath}/new_{filename}")
    print("Completed resizing all fo the assets.")
The setup function is used to create the random clips which will be put at the bottom. After downloading the clips you want into `assets/` run this function.

### Purge()
    for (dirpath, dirnames, filenames) in os.walk("./{WORKING_DIR}/"):
        for filename in filenames:
            if "v.mp4" in filename or "a.mp4" in filename:
                os.remove(os.path.join(dirpath, filename))
    print("Purged all of the temporary files.")
Purge is used to remove the video and audio files that are downloaded separately from youtube and combined in order to get the highest video and audio qualities. You can remove the files manually, but I find that running this function after the main or prepareVideo is much easier.

### prepareVideo(vid)
    vid = downloadVideo(vid)
    saveVideo(vid, resizeVideo(combineAudioVideo(vid)))
This function is used to scale and do everything else to a single youtube video. You can use a loop, and do it for multiple videos that way. `vid` is the video id for the youtube video (a string).

### downloadVideo(id)
This function is used to download a youtube video from its video id (a string) into the `{WORKING_DIR}/{id}/` directory. `WORKING_DIR` is used to store all the videos. Keep in mind that **the display and audio of the video will be saved seperately, and they will be named as according to the following: "Y{id}v" and "Y{id}a"**. The names will be made to work with the windows file system.

### main(videos, saferun = True)
The main function is the one you should probably prefer to use. The inputs are `videos`, a list of the video ids, and `saferun`, which saves the video ids into a log file -- so that you do not run the function twice for the same video id (this is on by default). This also uses threading to speed up the video editing process. Each unique video id will receive its own thread.

## Download
```bash
$ git clone https://github.com/Iamlel/VideoEditor.git
$ cd VideoEditor
```
You will require `main.py` and `text_assets/` for the program to execute.

## Contribute
**Contributions are definitely welcome**, since I do not see myself working on this project anymore. I used to use this myself, which was the reason for the creation of this project, but since I no longer want to do this, I have decided to open source it and put it out there for anyone else looking to do the same thing I was.

Obviously, you can add whatever you would like to, but here is a **list of features that I wanted to add**:
- Support for double digits.
- More softcoded.
- Easier to use.
- Accessibility from command line.
