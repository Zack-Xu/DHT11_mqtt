import oled
import wifi
import network
import time
import machine
from umqtt.simple import MQTTClient
import ubinascii
import utime
import micropython


ssid="WUSI"
##这里填写wifi名称
password="wusi01601"
##这里填写wifi密码


oled.text("connecting WIFI",0,0)
oled.show()

if(wifi.do_connect(ssid,password)):  
    wlan = network.WLAN(network.STA_IF)
    status=wlan.ifconfig()
    oled.fill(0)
    oled.text("conneted",0,0)
    oled.text(status[0],0,8)
    oled.show()
else:
    oled.fill(0)
    oled.text("error",0,0)
    oled.text("not connected",0,8)
    oled.text("check ssid or pa",0,16)
    oled.text("ssword",0,24)         
    oled.show()

##wifi的连接状态都会在oled上面显示出来
time.sleep_ms(1000)

import dht
DHT= dht.DHT11(machine.Pin(12))


PROGRAM_NAME = 'DHT_sensor'
DEVICE_NAME = ubinascii.hexlify(machine.unique_id()).decode()

#DEVICENAME MQTT设备ID

# JSON格式转换？
CONFIG_DATA_SCHEMA = """
{"name": "%s",
"state_topic": "%s",
"unit_of_measurement": "%s",
"availability_topic": "%s"
}
"""
CONFIG = {
    "broker": "10.0.1.3",
    "mqtt_user": "homeassistant",
    "mqtt_password": "",
}


BASE_TOPIC = 'HA/sensor/piliboard/'


TEMP_STATE = BASE_TOPIC+"temperature" + "/state"
HUMI_STATE = BASE_TOPIC+"humidity" + "/state"


CONFIG_TOPIC1 = 'homeassistant/sensor/piliboard/' + DEVICE_NAME +"temperature"  + '/config'
CONFIG_TOPIC2 = 'homeassistant/sensor/piliboard/' + DEVICE_NAME +"humidity"  + '/config'

UNIT_of_TEMP = '℃'
UNIT_of_HUMI = '%'

AVAILABILITY_TOPIC = BASE_TOPIC + "/availability"

CONFIG_DATA1 = CONFIG_DATA_SCHEMA % ("temperature"+DEVICE_NAME,
                                    TEMP_STATE,
                                    UNIT_of_TEMP,
                                    AVAILABILITY_TOPIC,
                                    )
CONFIG_DATA2 = CONFIG_DATA_SCHEMA % ("humidity"+DEVICE_NAME ,
                                    HUMI_STATE,
                                    UNIT_of_HUMI,
                                    AVAILABILITY_TOPIC,
                                    )

def mqtt_start():
    DHT.measure()
    oled.fill(0)
    oled.ShowChar40x64(0,0,DHT.temperature()/10)
    oled.ShowChar40x64(20,0,DHT.temperature()%10)
    oled.ShowChar24x24(40,30,0)
    oled.ShowChar40x64(64,0,DHT.humidity()/10)
    oled.ShowChar40x64(84,0,DHT.humidity()%10)
    oled.ShowChar24x24(104,30,1)
    c.connect()
    print("mqtt connected: subto {b}".format(b=TEMP_STATE))
    print("mqtt connected: subto {b}".format(b=HUMI_STATE))
        
    c.publish( CONFIG_TOPIC1, CONFIG_DATA1.encode(), retain=True)
    c.publish( CONFIG_TOPIC2, CONFIG_DATA2.encode(), retain=True)
        
    c.publish( AVAILABILITY_TOPIC, b"online", retain=True)
        
    c.publish( TEMP_STATE, str(DHT.temperature()).encode(), retain=True )
    c.publish( HUMI_STATE, str(DHT.humidity()).encode(), retain=True )
    oled.ShowIcon(107,0)  
    oled.show()



def start():
    
    global c
    # 创建MQTT的客户端对象
    c = MQTTClient(DEVICE_NAME, CONFIG["broker"], user=CONFIG["mqtt_user"], password=CONFIG["mqtt_password"])
    try:
        while True:
            c.set_last_will( AVAILABILITY_TOPIC, b"offline", retain=True)
            mqtt_start()
    # 设置当订阅的信息到达时的处理函数
    #c.set_callback(sub_cb)
 
    # 连接MQTT代理服务器
    #c.connect()
 
    # 订阅命令信息
    #c.subscribe(CONFIG["mqtt_topic_command"])
    
    finally:
        c.disconnect()
