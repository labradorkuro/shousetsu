#coding: utf-8
#消雪装置データ管理システム通信端末プログラム (Alpha02)

import time
import os,socket
import struct
from time import sleep
import urllib,urllib2
import fcntl
import datetime
import json
import threading
import serial
import subprocess

VERSION_NO = "1.0a"
INTERVAL = 10	#送信インターバル初期値 単位 sec
SLEEPTIME = 0.1 #永久ループのスリープ時間 単位 sec
TEST_INT = 1   #(テスト用)インターバルを10:1/10[60s] 20:1/20[30s] 30:1/30[20s] 60:1/60[10s]

#グローバル変数
g_macAddr = 0			#MACアドレス保存用
g_sendInterval = 10		#送信インターバル(秒)
g_cmpTime = 0			#時間経過比較用時刻
port = 0
config_file = '/home/pi/sensor_config.txt'

url = ''
#url = 'http://157.7.222.217:8081/nsl1.php'
#url = 'http://kcs2000.info/remos/ajaxlib.php'


#
# センサー設定ファイルの読み込み
# ~/sensor_config.txt
#
def readConfig(fname):
    lines = [];
    for line in open(fname, 'r'):
        config = line[:-1].split('\t')
        print config
        lines.append(config)
    return lines

#
# 設定値の取得
# configs 設定リスト
# name 所得する設定名
def getConfig(configs, name):
    value = "";
    for config in configs:
        if config[0].find(name) > -1:
            v = config[0].split('=')
            if len(v) == 2:
                value = v[1].strip()
    return value

#
# MACアドレスの取得
#  IN: インターフェース名 ex)"eht0" "wlan0"
#
def getMacAddr(ifname):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


def getDatetime():

    datet = datetime.datetime.today()     #現在日付・時刻のdatetime型データの変数を取得
    return datet.strftime("%Y-%m-%d %H:%M:%S")


#
# 装置データ取得
#  OUT: 取得データ
#
def readData():
    global port
    values = []
    port.write('req\r')
    str = port.readline()  # 行終端'\n'までリードする
    print "取得データ: %s " % str + "[len=%d]" % len(str)
    if len(str) > 0:
        values = str.split(',')
    return values

def main():

    global g_macAddr
    global g_sendInterval
    global g_cmpTime
    global port

    print "Version : " + VERSION_NO
    config = readConfig(config_file)
    sensor_no = getConfig(config,"sensor_no")
    serial_port = getConfig(config,"serial_port")
    url = getConfig(config,"post_url")
    g_cmpTime = time.time()

    #g_macAddr = getMacAddr("wwan0")
    #print "<<%s>>" % g_macAddr
    firstboot = 1

    port = serial.Serial(serial_port,
                      baudrate=9600,
                      #bytesize=serial.SEVENBITS,
                      bytesize=serial.EIGHTBITS,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      timeout=5.0)
    #無限ループ
    while True:
        time.sleep(SLEEPTIME)
        #10秒毎に温度湿度を計測して送信する
        if( g_cmpTime+g_sendInterval < time.time()):
            values = readData()  #装置からデータ取得
            print values
            if len(values) > 0:
                if url != "":
                    #HTTP送信
                    value_1 = values[0].split(':')
                    params = urllib.urlencode({'func':"regRecord", 'sensor_no': sensor_no, value_1[0].strip():value_1[1].strip()})
                    try:

                        res = urllib2.urlopen(url, params)
                        print "SEND DATA:%s" % params
                        res_data =res.read()
                        print res_data,     #,で改行されない
                        json_res = json.loads(res_data)
                        print "status=%s" % json_res['status'] + " int=%s" % json_res['int']
                        if json_res['int'] > 0:
                            g_sendInterval = (json_res['int']/1000)/TEST_INT  #msec ⇒ sec
                        print '\r'
                    except urllib2.URLError, e:
                        g_sendInterval = 10          #返り値のintervalが来ないので10秒としておく
                        print e
            g_cmpTime = time.time()
            firstboot = 0


    port.close()

if __name__ == '__main__':
  main()
