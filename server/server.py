from flask import Flask, render_template, request
import shutil
import os
import time
import tailer
from werkzeug.serving import WSGIRequestHandler
from multiprocessing import Process, Queue

app=Flask(__name__)
dir=''

@app.route('/')
def content():
	file = open('man.txt')
	text = file.read()
	return text+'\r\n'

@app.route('/getcmd')
def getCmdHandler():
	# wait for cmd to be written completely()
	id = request.args.get('id')
	filename = str(dir) + 'to' + str(id) + '.txt'
	cmd = str(tailer.tail(open(filename), 1))
	cmd_json = cmd[2:-2]
	return cmd_json

@app.route('/getdata')
def getDataHandler():
	# wait for data to be written completely()
	id = request.args.get('id')
	filename = str(dir) + 'from' + str(id) + '.txt'
	fd = open(filename)
	data = fd.read()	
	return data


@app.route('/postcmd', methods = ['POST'])
def postCmdHandler():
	if(request.is_json):
		jsondata = request.get_json(silent=True)
	else:
		return 'Invalid json data\r\n'
	id = jsondata['id']
	cmd_type = jsondata['cmd-type']
	cmd = jsondata['cmd']
	filename = str(dir) + 'to' + str(id) + '.txt'
	file = open(filename, 'a')
	file.write(str(jsondata+'\r\n'))
	return "Post complete!\r\n"

@app.route('/postdata', methods = ['POST'])
def postDataHandler():
	if(request.is_json):
		jsondata = request.get_json(silent=True)
	else:
		return 'Invalid json data\r\n'
	id = jsondata['id']
	data_type = jsondata['data-type']
	data = jsondata['data']
	filename = str(dir) + 'from' + str(id) + '.txt'
	file = open(filename, 'a')
	file.write(str(jsondata)+'\r\n')
	return "Post complete!\r\n"
	#return render_template('content.html', text=data)

@app.route('/monitor')
def showMonitorPage():
	return render_template('monitor_page.html')

@app.route('/init')
def init():
	timeStamp = time.strftime('%y%m%d%H%M%S')
	global dir
	dir = './data/'+timeStamp+'/'
	os.mkdir(dir)
	for i in range(11):
		filename = str(dir) + 'from' + str(i) + '.txt'
		file = open(filename, 'w')
		file.write("")
		file.close()
		filename = str(dir) + 'to' + str(i) + '.txt'
		file = open(filename, 'w')
		file.write("")
		file.close()
	return 'System initialized. Data files will be written in '+str(dir)+'\r\n'

if __name__ == '__main__':
    #WSGIRequestHandler.protocol_version = "HTTP/1.1"
	print(init())
	app.run(host='0.0.0.0', port=5555, debug=False)
