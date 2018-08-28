# coding:utf-8
from flask import Flask, jsonify, render_template, Blueprint, abort

import re
import urllib2
import urllib
import sys
import json
import time

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

@api.route('/')
def homes():
	# abort(403)
	return render_template("index.html")
#玩客币昨日矿场情况
@api.route('/recently')
def recently():
	return jsonify(getapi('https://x.miguan.in/otc/recently'))

#数字货币市值TOP 100
@api.route('/monitorRecordList')
def recordList():
	return jsonify(getapi('https://x.miguan.in/otc/v7/monitorRecordList?orderBy=turnover'))

#矿场情况趋势
@api.route('/marketHistoryList')
def history():
	# return jsonify(gethistory(getapi('https://x.miguan.in/otc/marketHistoryList')))
	return jsonify(getapi('https://x.miguan.in/otc/marketHistoryList'))

#请求数据接口函数
def getapi(url):
	send_headers = {
		'accept':'application/json, text/plain, */*',
		'Origin':'https://t.miguan.in',
		'Referer':'https://t.miguan.in/monitor',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
		'x-requested-with':'XMLHttpRequest'
	}

	req = urllib2.Request(url,headers=send_headers)
	r = urllib2.urlopen(req)

	html = r.read()		#返回网页内容
	receive_header = r.info()	 #返回的报头信息
	# sys.getfilesystemencoding() 
	html = html.decode('utf-8','replace').encode(sys.getfilesystemencoding()) #转码:避免输出出现乱码 
	html = json.loads(html)
	return html
	#print receive_header
	# print '####################################'
# 历史数据处理接口
def gethistory(history):
	historydata = {}
	historydata['historytime'] = makeHistoryData(history['result'],'datetime')
	historydata['historytopwkb'] = makeHistoryData(history['result'],'topWkb')
	historydata['historyaveragewkb'] = makeHistoryData(history['result'],'averageWKb')
	historydata['historykjnumber'] = makeHistoryData(history['result'],'kjNumber')
	return historydata
# 历史详细数据处理函数
def makeHistoryData(data,type):
	if type == 'datetime':
		CreateTime = []
		for i in data:
			timeArray = time.localtime(i['createTime'])
			otherStyleTime = time.strftime("%m-%d", timeArray)
			# print otherStyleTime
			CreateTime.append(otherStyleTime)
		return CreateTime
	if type == 'topWkb':
		TopWKB = []
		for i in range(len(data)):
			TopWKB.append(data[i]['topWkb']);
		return TopWKB

	if type == 'averageWKb':
		AverageWKb = []
		for i in data:
			nmb = i['wkbAdd'] / float(i['blockNum'])
			AverageWKb.append('%.2f' % nmb);
		return AverageWKb

	if type=='kjNumber':
		KjNumber = []
		for i in range(len(data)):
			KjNumber.append(int(data[i]['wkbAdd'] / data[i]['averageBandWidth'] * 10));
		return KjNumber