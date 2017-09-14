# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redis
# import aerospike
from pymongo import MongoClient
import yaml

android_data = {"device": "c5pltechn", "networkCountryIso": "cn", "currentWifi": "[\"Bangsun\",e4:8d:8c:6b:9b:42]",
                "user": "dpi", "timeZone": "[GMT+08:00,Asia/Shanghai]",
                "wifiList": "[Bangsun,e4:8d:8c:6b:9b:42,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:6b:9b:42,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:6b:9a:fa,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:72:bd:a1,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:4b:1f:d4,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:6b:9b:43,WPA-PSK-CCMPWPA2-PSK-CCMPESS,HZ-WL2504,c0:25:5c:ed:52:c3,WPA-PSK-CCMP+TKIPWPA2-PSK-CCMP+TKIPESSBLE,360WiFi-yyan,5c:93:a2:fd:2c:17,WPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:72:bd:a2,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:6b:9b:7e,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Bangsun,e4:8d:8c:6b:9a:fb,WPA-PSK-CCMPWPA2-PSK-CCMPESS,VIPGuest,c0:25:5c:ed:52:cd,WPA-PSK-CCMP+TKIPWPA2-PSK-CCMP+TKIPESSBLE,Bangsun,e4:8d:8c:4b:1f:d5,WPA-PSK-CCMPWPA2-PSK-CCMPESS,Sa,36:f3:9a:48:58:14,WPA2-PSK-CCMPWPSESS,Bangsun,e4:8d:8c:4b:20:2b,WPA-PSK-CCMPWPA2-PSK-CCMPESS,HZ-WL2504,c0:25:5c:ed:52:cc,WPA-PSK-CCMP+TKIPWPA2-PSK-CCMP+TKIPESSBLE,HZ-WLCEMP,c0:25:5c:ed:52:cf,WPA2-EAP-CCMPESSBLE,Bangsun,e4:8d:8c:5c:06:9f,WPA-PSK-CCMPWPA2-PSK-CCMPESS]",
                "IMEI": "353288083696025", "sdkVersion": "4.2.1", "id": "MMB29M", "version": "6.0.1",
                "uevent": "MAJOR10MINOR40DEVNAMEcpu_dma_latency", "serial": "aa5ad488", "manufacturer": "samsung",
                "ppp": "isContent", "type": "user", "rooted": "0", "networkType": "0", "host": "SWHD7414",
                "totalSD": "27146612736", "totalSystem": "3039856",
                "fingerprint": "samsung/c5pltezc/c5pltechn:6.0.1/MMB29M/C5000ZCU1AQE2:user/release-keys",
                "misc": "183hw_random28qce29usb_accessory30android_ssusbcon31usb_ncm32android_rndis_qc33usb_mtp_gadget34ccid_bulk35ccid_ctrl36android_mbim37ramdump_smem38network_throughput39network_latency40cpu_dma_latency41ramdump_modem42ramdump_wcnss43ramdump_adsp44xt_qtaguid45msm_rtac46binder47alarm48log_system49log_radio50log_events51log_main52ashmem239uhid236device-mapper53power_on_alarm223uinput54hbtp_vm55hbtp_input56zinitix_touch_misc1psaux57dpl_ctrl58rmnet_ctrl359rmnet_ctrl260rmnet_ctrl161rmnet_ctrl62wcnss_wlan63wcnss_ctrl200tun64p6165tgt66pn54767sec_misc68msm_hweffects69msm_amrwb_in70msm_qcelp71msm_evrc72msm_amrwbplus73msm_amrwb74msm_amrnb75msm_mp376msm_ape77msm_alac78msm_multi_aac79msm_aac80msm_wmapro81msm_wma82msm_amrnb_in83msm_evrc_in84msm_qcelp_in85msm_aac_in237loop-control86ramdump_venus87smem_log88sdp_dlp89dek_log90dek_req91dek_evt92tima_uevent229fuse93smcmod94msm_audio_cal95ion",
                "platform": "AND", "syncookies": "notExist", "availableMemory": "1884811264", "brightness": "153",
                "product": "c5pltezc", "cellularIP": "192.168.90.8", "existPipe": "0", "packageName": "com.lucky",
                "startupTime": "1499133623", "timestamp": "1499217078210", "isProxy": "1", "cpufreq": "isContent",
                "bootloader": "C5000ZCU1AQE2", "appVersion": "1.0", "isVPN": "0", "availableSD": "22221756",
                "availableSystem": "305492", "algID": "ANDAlg", "tags": "release-keys", "cpuABI": "armeabi-v7aarmeabi",
                "battery": "[5,100]", "bluetooth": "FC:42:03:55:1F:61", "stat": "notExist",
                "wifiMacAddress": "fc:42:03:55:1f:62", "time": "0", "switch": "isContent", "parameters": "notExist",
                "hashCode": "G_iy_1sxnk_PbtF1X1yH30-S8cPR3SYs99DIgYEs3B8", "radio": "C5000ZCU1AQE2", "board": "MSM8952",
                "brand": "samsung", "displayRom": "MMB29M.C5000ZCU1AQE2",
                "resolution": "[2.625,1080,1920,2.625,397.565,399.737]", "totalMemory": "3716800", "hardware": "qcom",
                "custID": "123", "adb": "notExist", "model": "SM-C5000", "existQemu": "0"}

ios_data = {
    "totalSystem": "15989485568",
    "language": "[zh-Hans_US-中文（简体、美国）]",
    "fork": "0",
    "totalMemory": "2107113472",
    "IDFA": "DB8AE8D6-E0C0-42D3-A6A8-64C76BDDCABC",
    "packageName": "com.bangsheng.dfp-ios-demo-poc-bhv",
    "appVersion": "1.0",
    "algID": "IOSAlg",
    "resolution": "[320-568]",
    "version": "10.3.1",
    "isProxy": "1",
    "isVPN": "0",
    "rooted": "0",
    "cellularIP": "192.168.91.158",
    "platform": "IOS",
    "startupTime": "1496158385",
    "sdkVersion": "4.2.1",
    "custID": "130",
    "battery": "[unplugged-0.830000]",
    "networkType": "WiFi",
    "model": "iPhoneSE(A1662/A1723/A1724)",
    "carrier": "中国电信",
    "timestamp": "1499159397000",
    "availableSystem": "446672896",
    "brightness": "0.377097",
    "wifiList": "[Bangsun-e4:8d:8c:6b:9a:fa]",
    "IDFV": "REMALLW_gABsT12fIXavPlVYOX1gH4bt",
    "hashCode": "F_70XhkzFxOxOcU-RWII8g"
}

def get_config(config_file='config.yaml'):
    application_yaml = open(config_file)
    application = yaml.load(application_yaml)
    application_yaml.close()
    return application['dfp.mongo']['host'], application['dfp.mongo']['port']


def mongo_client(type):
    host, port = get_config()
    client = MongoClient(host, port)
    collection = client.dfp.dfp
    if type == "ios":
        return collection.find({"IDFA": "DB8AE8D6-E0C0-42D3-A6A8-64C76BDDCABC"})[0]
    elif type == "android":
        return collection.find({"IMEI": "353288083696025"})[0]


def get_as_data():
    config = {
        'hosts': [('10.100.1.116', 3000)],
        'policies': {'timeout': 1000}
    }
    try:
        client = aerospike.client(config).connect()
    except:
        print("failed to connect to the cluster with", config['hosts'])
        sys.exit(1)

    scan = client.scan('dfp', 'dfp')
    as_data = []
    def get_result(key):
        as_data.append(key[0][2])
    scan.foreach(get_result)
    client.close()
    return str(as_data)




def get_redis_data():
    r = redis.StrictRedis(host='10.100.1.116', port=6380)
    redis_data = r.keys()
    for i in range(len(redis_data)):
        redis_data[i] = redis_data[i][4:]
    return redis_data


def data_validate(db_type, platform, db_data):
    if db_type == 'mongo':
        if platform == 'and':
            map(db_data.pop,
                ["updateTime", "createTime", "crc64Code", "passiveCode", "passiveIP", "possbility", "_id", "dfp", "UDID",
                 "isvm"])
            if cmp(android_data,db_data) == 0:
                print "mongo android ios_data validation success"
            else:
                print "mongo android ios_data validation failed"
        elif platform == 'ios':
            map(db_data.pop,
                ["updateTime", "createTime", "crc64Code", "passiveCode", "passiveIP", "possbility", "_id", "dfp"])
            if cmp(ios_data, db_data) == 0:
                print "mongo ios ios_data validation success"
            else:
                print "mongo ios ios_data validation failed"

    elif db_type == 'as' or db_type == 'redis':
        if platform == 'and':
            if android_data["wifiMacAddress"] in str(db_data) and android_data["IMEI"] in str(db_data) and \
                            android_data["startupTime"] in str(db_data) and android_data["bluetooth"] in str(db_data):
                print db_type + " android ios_data validation success"
            else:
                print db_type + " android ios_data validation failed"
        if platform == 'ios':
            if ios_data["startupTime"] in str(db_data) and ios_data["IDFA"] in str(db_data) and \
                            ios_data["IDFV"] in str(db_data):
                print db_type + " iOS ios_data validation success"
            else:
                print db_type + " iOS ios_data validation failed"

if __name__ == '__main__':
    redis_db_data = get_redis_data()
    data_validate('redis', 'ios', redis_db_data)
    data_validate('redis', 'and', redis_db_data)
    # as_db_data = get_as_data()
    # data_validate('as', 'ios', as_db_data)
    # data_validate('as', 'and', as_db_data)
    android_mongo_data = mongo_client('android')
    data_validate('mongo', 'and', android_mongo_data)
    ios_mongo_data = mongo_client('ios')
    data_validate('mongo', 'ios', ios_mongo_data)
