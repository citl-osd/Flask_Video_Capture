import os
import time
import os.path
from flask import Flask, render_template, url_for, redirect, send_from_directory
from subprocess import Popen, PIPE


app = Flask(__name__)
roots = ['X:/','Z:/']

class ffmpegClass:
	def __init__(self):
		self.command = 'Y:/management/staff/liam/scripts/bin/ffmpeg -y -f decklink -i "Intensity Pro@12" -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -vb 20m -s 1920X1080 -r 29.97 -acodec libvo_aacenc -ar 48000 -ac 2 -ab 192k "'
		self.outputfile = 'X:/test/ffmpeg/flasktest.mp4'
		self.lastDir = 'X/test/ffmpeg'

	def setOutput(self, output):
		self.outputfile = output

	def setLastDir(self, path):
		self.lastDir = '/'.join(path.split('/')[:-1])

	def startProcess(self):
		self.pipe = Popen(self.command + self.outputfile + '"',stdin=PIPE,shell=True)
		waiting = True
		counter = 0
		while waiting:
			if counter == 40:
				self.pipe.terminate()
				return "FAIL"
			if os.path.exists(self.outputfile):
				waiting = False
			else:
				counter = counter + 1
				time.sleep(0.5)
		return "WE GOT ONE"

	def stopProcess(self):
		code= self.pipe.communicate('q')
		return code

ffmpegProcess = ffmpegClass()

@app.route('/favicon.ico')
def favicon():
	return send_from_directory('static','favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/bootstrap.css')
def bootstrap():
	return send_from_directory('static','bootstrap.css', mimetype='text/css')

@app.route("/")
def root():
	return render_template('fileBrowser.html', dirs=roots, submit=False)


@app.route('/stop')
def stop():
	code = ffmpegProcess.stopProcess()
	return render_template('captureFinished.html', output=ffmpegProcess.outputfile, dirs = ffmpegProcess.lastDir)


@app.route('/start')
def start():
	ready = ffmpegProcess.startProcess()
	if ready == 'FAIL':
		return "SOMETHING WENT VERY WRONG!"
	return render_template('recordingInProgress.html',output=ffmpegProcess.outputfile)

@app.route('/saveto/<path:path>')
def saveto(path):

	if path.startswith('X/') and os.path.isdir('X:/' + path[2:]):
		if path.endswith('/'):
			path = path[:-1]
		alldirs = os.listdir('X:' + path[1:])
		dirs = ['X:' + path[1:] + '/..']
		for dir in alldirs:
			if not dir.startswith('.'):
				if path[2:]:
					dir = '/'.join(['X:', path[2:], dir])
				else:
					dir = 'X:/' + dir
				if os.path.isdir(dir):
					dirs = dirs + [dir]
		return render_template('fileBrowser.html',dirs=dirs, curdir='X:/' + path[2:], submit=True)
	elif path.startswith('Z/') and os.path.isdir('Z:/' + path[1:]):
		if path.endswith('/'):
			path = path[:-1]
		alldirs = os.listdir('Z:' + path[1:])
		dirs = ['Z:' + path[1:] + '/..']
		for dir in alldirs:
			if not dir.startswith('.'):
				if path[2:]:
					dir = '/'.join(['Z:', path[2:], dir])
				else:
					dir = 'Z:/' + dir
				if os.path.isdir(dir):
					dirs = dirs + [dir]
		return render_template('fileBrowser.html',dirs=dirs, curdir='Z:/' + path[2:], submit=True)
	elif path.endswith('.mp4') and (path.startswith('Z/') or path.startswith('X/')):
		if os.path.exists(path[0] + ':' + path[1:]):
			return 'FILE ALREADY EXISTS!'
		elif not os.path.exists(path[0] + ':' + '/'.join(path[2:].split('/')[:-1])):
			return 'PARENT DIRECTORY DOES NOT EXIST!'
		else:
			ffmpegProcess.setOutput(path[0] + ':' + path[1:])
			ffmpegProcess.setLastDir(path)
			return render_template('startRecording.html', filename=path)
	else:
		return('What tomfoolery is this?')

@app.route('/saveto/')
def bareSaveto():
	return render_template('fileBrowser.html', dirs=roots, submit=False)


if __name__ == "__main__":
	app.run()
