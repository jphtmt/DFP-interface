# coding=utf-8
import yaml
import json
import requests
import ast
import sys
from pymongo import MongoClient
import aerospike
import redis

reload(sys)
sys.setdefaultencoding('utf8')
header = {"Content-Type": "application/json; charset=utf-8",
          "Accept": "application/json",
          "User-Agent": "dfp-ios-demo-poc/1 CFNetwork/811.4.18 Darwin/16.5.0",
          "Accept-Language": "zh-cn",
          "Accept-Encoding": "gzip, deflate"
          }

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
ios_3_data = {
    "packageStr": "IDFA=A634D3A0-6682-48D9-808F-C909B99A54F2&IDFV=RBCLLZCGAQSIHN1ON_P9SALZ1PKN-FEG&activeTime=173661&battery=%5BUNPLUGGED%2C0.830000%5D&brightness=0.411891&bundleId=COM.BANGSHENG.BSFINGERSDK-TESTIN&carrier=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8&freeDiskSpace=9378299904&iOSVersion=9.3.2&isProxy=1&isRooted=1&isVPN=0&language=%5BZH_CN%2C%E4%B8%AD%E6%96%87%EF%BC%88%E4%B8%AD%E5%9B%BD%EF%BC%89%5D&model=IPHONE%206S(A1634%2FA1687%2FA1700)&network=%5BWIFI%2C192.168.91.202%2C0.0.0.0%5D&networkType=WIFI&partnerCode=123&resolution=%5B375%2C667%5D&sdkVersion=3.4.1&startupTime=1488960059097&systemTime=1488960232772&totalDiskSpace=12609748992&totalMemory=2102394880&wifiList=%5BBANGSUN%2CE4%3A8D%3A8C%3A72%3ABD%3AA1%5D&sign=9139a9d3d50916a216489e09ea920e098c55eb0be6e2e6a0832ce8ba2c564b75",
    "platform": "0",
    "signature": "f60c8cd67d69a07fdf3e367f61fc65c7514f97b8",
    "nonceStr": "",
    "partnerCode": "123"
}

and_3_data = {"platform": "1", "signature": "75043d437f65cd112a43b4ae44a1c5a33c953304", "nonceStr": "",
              "partnerCode": "123",
              "packageStr": "IMEI=864664034674265&IMSI=&activeTime=78103&applicationVersion=1.0&basestation=&battery=%5B2%2C2%5D&bluetoothAddress=&board=M5%20NOTE&brand=MEIZU&brightness=80&bsId=2BCC7419521EB725&cellular=192.168.91.73&cpuABI=ARM64-V8A&cpuNumber=7D7EEBE31DE52226&displayRom=FLYME%206.1.0.0A&freeMemory=1598500864&freeSDCard=7204948&freeSystem=593872&hardware=MT6755&isRooted=0&isSimulator=0&macAddress=54%253A14%253A73%253AB4%253A08%253AD0&machineNumber1=000000&machineNumber2=00&manufacturer=MEIZU&nbasestaion=&networkType=WIFI&packageName=COM.EXAMPLE.BANGSUN.SS&partnerCode=123&product=MEIZU_M5%20NOTE&resolution=%5B3.0%2C1080%2C1920%2C3.0%2C403.411%2C403.041%5D&sdkVersion=3.3.3&startupTime=1499326304289&timeZone=%5BGMT%2B08%3A00%2CASIA%2FSHANGHAI%5D&totalMemory=2849104&totalSDCard=11424468992&totalSystem=2519280&version=6.0&wifi=%5B%22BANGSUN%22%2CE4%3A8D%3A8C%3A6B%3A9B%3A42%5D&wifiList=&sign=364ba18b2bad389245d92a877ccdcf2aa1455a185b1588c9101d65665c03f090"}

param = {}
param['WEB'] = {"touchSupport": "wNLf", "scrHeight": "5Jwy", "scrAvailSize": "TeRS", "hasLiedLanguages": "j5po",
                "adblock": "FMQw", "flashVersion": "dzuS", "browserVersion": "d435", "indexedDb": "3sw-",
                "userAgent": "0aew", "browserName": "-UVA", "plugins": "ks0Q", "jsFonts": "EOQP", "custID": "pnPb",
                "scrColorDepth": "qmyu", "userLanguage": "hLzX", "UUID": "KomL", "hasLiedOs": "ci5c",
                "timeZone": "q5aJ", "mimeTypes": "jp76", "localCode": "lEnu", "online": "9vyE", "javaEnabled": "yD16",
                "historyList": "kU5z", "storeDb": "Fvje", "webSmartID": "E3gR", "doNotTrack": "VEek",
                "appMinorVersion": "qBVW", "localStorage": "XM7l", "hasLiedResolution": "3neK",
                "sessionStorage": "HVia", "cookieEnabled": "VPIf", "platform": "0pT8", "os": "hAqN",
                "srcScreenSize": "tOHY", "hasLiedBrowser": "2xC5", "openDatabase": "V8vl", "scrWidth": "ssI5",
                "appcodeName": "qT7b", "scrAvailHeight": "88tV", "browserLanguage": "q4f3", "cpuClass": "Md7A",
                "scrAvailWidth": "E-lJ", "systemLanguage": "e6OK", "cookieCode": "VySQ", "scrDeviceXDPI": "3jCe"}

param['IOS'] = {"platform": "0pT8", "fork": "jQx6", "model": "k3LE", "networkType": "Swlw", "packageName": "VQFA",
                "totalMemory": "oUvy", "totalSystem": "bxIT", "custID": "pnPb", "cellularIP": "PneH",
                "resolution": "9_vV", "availableSystem": "H6Rg", "IDFA": "bA0Q", "sdkVersion": "Vkrm",
                "version": "XKTz", "brightness": "qm7W", "IDFV": "sxWp", "startupTime": "oA3w", "wifiList": "wXg4",
                "appVersion": "wfQn", "battery": "89Fw", "rooted": "UqMW", "activeTime": "R7of", "carrier": "WANY",
                "language": "pO8w"}

param['AND'] = {"uevent": "0Qzb", "networkType": "Swlw", "packageName": "VQFA", "availableMemory": "qiHP",
                "custID": "pnPb", "totalSystem": "bxIT", "existPipe": "7eMA", "type": "EwPA", "baseStation": "yXoP",
                "phoneNumber": "nrYU", "existQemu": "JC9t", "parameters": "9Sgh", "platform": "0pT8",
                "availableSD": "Uaj4", "host": "R0Cu", "networkOperator": "csj7", "cellularIP": "PneH", "ppp": "xCiW",
                "voiceMailNumber": "d8FW", "board": "hZFp", "availableSystem": "H6Rg", "wifiList": "wXg4",
                "appVersion": "wfQn", "manufacturer": "EAAo", "activeTime": "R7of", "contactsHash": "kClR",
                "cpuABI": "U3oU", "model": "k3LE", "hardware": "Jnh9", "phoneType": "LrgZ", "displayRom": "2vam",
                "wifiMacAddress": "_Y6j", "switch": "eLSf", "timeZone": "q5aJ", "resolution": "9_vV",
                "musicHash": "FNei", "version": "XKTz", "sdkVersion": "Vkrm", "id": "pWFF", "brightness": "qm7W",
                "photosHash": "GLBj", "fingerprint": "RIY7", "startupTime": "oA3w", "currentWifi": "bOhy",
                "battery": "89Fw", "UDID": "NfP-", "simCountryIso": "Hx1a", "tags": "l4wv", "cpufreq": "DR1H",
                "simSerialNumber": "WCxt", "totalMemory": "oUvy", "simulator": "YIxZ", "IMSI": "7UTv",
                "IOPorts": "4-es", "bootloader": "O0oS", "totalSD": "LtgM", "stat": "QEYN", "misc": "nDJC",
                "sensors": "4i37", "product": "qHkh", "adb": "fhag", "bluetooth": "qCjR", "networkCountryIso": "lRtB",
                "syncookies": "4MYi", "nearbyBaseStation": "EyOF", "IMEI": "9POg", "device": "JjpN", "radio": "qjoF",
                "rooted": "UqMW", "brand": "BKn7", "user": "BPiZ", "serial": "AUSx", "cpuType": "aKfq"}


def get_base_url(config_path='config.yaml'):
    application_yaml = open(config_path)
    application = yaml.load(application_yaml)
    application_yaml.close()
    return application['dfp.url']


def get_preFetch():
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'public/downloads/preFetch.js')
    if r.status_code != 200:
        print "get_preFetch fail"
    else:
        print "get preFetch success"


def get_rd():
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'public/downloads/extra.js?includes=rd')
    if r.status_code != 200:
        print "get_rd fail"
    else:
        print "get_rd success"


def params_map(platform=None):
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'protected/paramsMap?platform=' + platform)
    return r.json()


def compare_paramsmap(platform):
    params_from_server = params_map(platform=platform)
    if cmp(params_from_server, param[platform]) != 0:
        print "%s platform param map wrong!" % platform
    else:
        print "%s platfrom param map correct" % platform


def global_stat():
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'protected/globalStat')
    if r.status_code != 200:
        print "global_stat connection error"
    elif r.status_code == 200:
        if r.json()['stat']['invokerCount'] != 0:
            print json.loads(r.text)['stat']['invokerCount']


def daily_stat():
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'protected/dailyStat')
    if r.status_code != 200:
        print "daily_stat connection error"
    elif r.status_code == 200:
        print " daily_stat success"


def dfp_about():
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'protected/about')
    if r.status_code != 200:
        print "dfp_about connection error"
    elif r.status_code == 200:
        print r.json()['version']
        print "dfp_about success"


def js_download():
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'public/downloads/frms-fingerprint.js')
    if r.status_code != 200:
        print "download js error"
    elif r.status_code == 200:
        print "js_download success"


def view_key():
    config_public = 'MIGWMA0GCSqGSIb3DQEBAQUAA4GEADCBgAJ5AL2KNNzht9zQVQPiXcpQGC0kd0aMUJscviBkaaGRL36U26r9UvG7yTVSYxLWRN7FU7eYy2J4otWLASk6atN8LEYkd5KQKuCn12Asp4T8JbJHi805sUvjrN5BfjHW+uN104CRwb/bK/2hHCcLmvRl5wu5MCRmbvZ8uwIDAQAB'
    config_private = 'MIICUgIBADANBgkqhkiG9w0BAQEFAASCAjwwggI4AgEAAnkAvYo03OG33NBVA+JdylAYLSR3RoxQmxy+IGRpoZEvfpTbqv1S8bvJNVJjEtZE3sVTt5jLYnii1YsBKTpq03wsRiR3kpAq4KfXYCynhPwlskeLzTmxS+Os3kF+Mdb643XTgJHBv9sr/aEcJwua9GXnC7kwJGZu9ny7AgMBAAECeQCHzHzBgOtFxvISXV5LdIVN2qGmpyOdbsN929Oe0bHQpICaivOhhKTNkmCvf1tKrOClW1DlFX+9NeG4E0R3nLTQ95TwPvJ7XYTRVDBnhxe8knWvp7+omhN1Z2e0gGFokHMX/7SCtQY+BntpFnfg8b6rWHPxYyqnkKECPQDxNly9JwDKUf7IHWridXqB/j3IS5LDY7mSSBsfcUk9LzURYOu4wY6bjLkAH9sGFLxhoIK30iagxzJpATECPQDJKOKlcSrefN3aIwUF95ZpbscfM1Cf5+4unBN2fi404p9XLAHrqVW+XIr+yaIXCW8LXG/f6PA3tRaJgasCPQDNnxThXe1LiyhQ+NrTn2fGhq+uHdZHX6yiqXsNi6nuUV7AqMlo3v8tVIGkPIOeJHEOHCEyiB/LsOMlJhECPFrRTqIK2aPhE/gr31S2Vv36uYNok3neKDZ62H6isRHHTtD4WVWf+cob1dT6C2gDJlMmxIt+ixVbeHVUSQI9AJbjeZfL44/NiytYzNSQ8kz+mXGZOhB7VdwFoIu+SNwrlfsbwlRaom65/kK6SUoxwN1icoFLinx5vRj4aA=='
    r = requests.get(url=get_base_url(
        config_path='config.yaml') + 'protected/viewKey')
    if r.status_code != 200:
        print "view_key error"
    elif r.status_code == 200:
        if r.json()['public'] == config_public and r.json()['private'] == config_private:
            print "view_key success"


def health_check():
    r = requests.get(url=get_base_url('config.yaml') + 'protected/healthCheck')
    if r.status_code != 200:
        print "health check network error"
    elif r.status_code == 200:
        if r.json()["state"] is True:
            print "health_check success"
        if r.json()["state"] is False:
            print "health check failed, can not connect to database"


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
                ["updateTime", "createTime", "crc64Code", "passiveCode", "passiveIP", "possbility", "_id", "dfp",
                 "UDID",
                 "isvm"])
            if cmp(android_data, db_data) == 0:
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


def generate_post(uri, platform, data, generation=4):
    r = requests.post(url=uri, headers=header, json=data)
    if r.status_code == 200:
        if generation == 3:
            if len(r.json()['deviceId']) == 160:
                print platform + " post success"
            elif len(r.json()['deviceId']) == 64:
                print platform + " post success"
        elif len(r.json()['dfp']) == 160:
            print platform + " post success"
    else:
        print platform + " post failed"


def main():
    generate_post(get_base_url(config_path='config.yaml') + 'public/generate/post', 'android', android_data)
    generate_post(get_base_url(config_path='config.yaml') + 'public/generate/post', 'iOS', ios_data)
    generate_post(get_base_url(config_path='config.yaml') + 'api/device-fingerprint', 'iOS', ios_3_data, generation=3)
    generate_post(get_base_url(config_path='config.yaml') + 'api/device-fingerprint', 'Android', and_3_data,
                  generation=3)
    get_preFetch()
    get_rd()
    compare_paramsmap('WEB')
    compare_paramsmap('IOS')
    compare_paramsmap('AND')
    global_stat()
    daily_stat()
    dfp_about()
    js_download()
    view_key()
    health_check()
    redis_db_data = get_redis_data()
    data_validate('redis', 'ios', redis_db_data)
    data_validate('redis', 'and', redis_db_data)
    as_db_data = get_as_data()
    data_validate('as', 'ios', as_db_data)
    data_validate('as', 'and', as_db_data)
    android_mongo_data = mongo_client('android')
    data_validate('mongo', 'and', android_mongo_data)
    ios_mongo_data = mongo_client('ios')
    data_validate('mongo', 'ios', ios_mongo_data)


if __name__ == '__main__':
    main()
