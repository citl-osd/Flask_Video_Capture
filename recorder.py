import os
import os.path
from flask import Flask, render_template, url_for, redirect, send_from_directory
from subprocess import Popen, PIPE


app = Flask(__name__)
roots = ['X:/','Z:/']

class ffmpegClass:
	def __init__(self):
		self.command = 'Y:/management/staff/liam/scripts/bin/ffmpeg -y -decklink -i X:/A_Watch_Folder/1030Archive_2.mov -vcodec libx264 -preset ultrafast -vb 15m -s 1920X1080 -r 29.97 -acodec libvo_aacenc -ar 48000 -ac 2 -ab 192k '
		self.outputfile = 'X:/test/ffmpeg/flasktest.mp4'

	def setOutput(self, output):
		self.outputfile = output
		print 'output changed to ' + output

	def startProcess(self):
		self.pipe = Popen(self.command + self.outputfile,stdin=PIPE, shell=True)

	def stopProcess(self):
		code= self.pipe.communicate('q')
		print code
		return code

ffmpegProcess = ffmpegClass()

@app.route('/favicon.ico')
def favicon():
	return send_from_directory('static','favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def root():
	return render_template('fileBrowser.html', dirs=roots)


@app.route('/stop')
def stop():
	code = ffmpegProcess.stopProcess()
	print code
	return render_template('captureFinished.html', output=ffmpegProcess.outputfile)


@app.route('/start')
def start():
	ffmpegProcess.startProcess()
	return render_template('recordingInProgress.html',output=ffmpegProcess.outputfile)

@app.route('/saveto/<path:path>')
def saveto(path):
	print path
	print path[2:]
	if path.startswith('X/') and os.path.isdir('X:/' + path[2:]):
		alldirs = os.listdir('X:/' + path[2:])
		dirs = []
		for dir in alldirs:
			dir = '/'.join(['X:', path[2:], dir])
			print dir
			if not dir.startswith('.') and (os.path.isdir(dir)):
				dirs = dirs + [dir]
		return render_template('fileBrowser.html',dirs=dirs, curdir='X:/' + path[2:])
	elif path.startswith('Z/') and os.path.isdir('Z:/' + path[2:]):
		alldirs = os.listdir('Z:/' + path[2:])
		dirs = []
		for dir in alldirs:
			dir = '/'.join(['Z:', path[2:], dir])
			if not dir.startswith('.') and (os.path.isdir(dir)):
				dirs = dirs + [dir]
		return render_template('fileBrowser.html',dirs=dirs, curdir='Z:/' + path[2:])
	elif path.endswith('.mp4') and (path.startswith('Z/') or path.startswith('X/')):
		if os.path.exists(path[0] + ':' + path[1:]):
			return 'FILE ALREADY EXISTS'
		else:
			ffmpegProcess.setOutput(path[0] + ':' + path[1:])
			return render_template('startRecording.html', filename=path)
	else:
		return('What tomfoolery is this?')

@app.route('/saveto/')
def bareSaveto():
	return render_template('fileBrowser.html', dirs=roots)


if __name__ == "__main__":
	app.run(debug=True)
