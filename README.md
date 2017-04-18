# Flask Video Recorder

---

This is a simple python script that exposes a Flask webserver to show simple pages that you can use to control an FFMPeg process to capture live video.

It's currently set up to listen on Flask's default port 5000 (so hit 127.0.0.1:5000), FFMPeg's path is hard-codeded in, and we're capturing from a Blackmagic Intensity Pro capture card.

The throwawaypipe stuff was to grab a frame, to ensure that your capture device is working as expected and not grabbing color bars or something otherwise that would spoil your day.