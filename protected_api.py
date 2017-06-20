# coding=utf-8
import yaml
import json
import requests
import ast
import sys
reload(sys)
sys.setdefaultencoding('utf8')
param = {}
param['WEB'] = {"touchSupport":"wNLf","scrHeight":"5Jwy","scrAvailSize":"TeRS","hasLiedLanguages":"j5po","adblock":"FMQw","flashVersion":"dzuS","browserVersion":"d435","indexedDb":"3sw-","userAgent":"0aew","browserName":"-UVA","plugins":"ks0Q","jsFonts":"EOQP","custID":"pnPb","scrColorDepth":"qmyu","userLanguage":"hLzX","UUID":"KomL","hasLiedOs":"ci5c","timeZone":"q5aJ","mimeTypes":"jp76","localCode":"lEnu","online":"9vyE","javaEnabled":"yD16","historyList":"kU5z","storeDb":"Fvje","webSmartID":"E3gR","doNotTrack":"VEek","appMinorVersion":"qBVW","localStorage":"XM7l","hasLiedResolution":"3neK","sessionStorage":"HVia","cookieEnabled":"VPIf","platform":"0pT8","os":"hAqN","srcScreenSize":"tOHY","hasLiedBrowser":"2xC5","openDatabase":"V8vl","scrWidth":"ssI5","appcodeName":"qT7b","scrAvailHeight":"88tV","browserLanguage":"q4f3","cpuClass":"Md7A","scrAvailWidth":"E-lJ","systemLanguage":"e6OK","cookieCode":"VySQ","scrDeviceXDPI":"3jCe"}

param['IOS'] = {"platform":"0pT8","model":"k3LE","networkType":"Swlw","packageName":"VQFA","totalMemory":"oUvy","totalSystem":"bxIT","custID":"pnPb","cellularIP":"PneH","resolution":"9_vV","availableSystem":"H6Rg","IDFA":"bA0Q","sdkVersion":"Vkrm","version":"XKTz","brightness":"qm7W","IDFV":"sxWp","startupTime":"oA3w","wifiList":"wXg4","appVersion":"wfQn","battery":"89Fw","rooted":"UqMW","activeTime":"R7of","carrier":"WANY","language":"pO8w"} 

param['AND'] = {"model":"k3LE","networkType":"Swlw","hardware":"Jnh9","packageName":"VQFA","availableMemory":"qiHP","existPipe":"7eMA","totalSystem":"bxIT","custID":"pnPb","displayRom":"2vam","wifiMacAddress":"_Y6j","timeZone":"q5aJ","resolution":"9_vV","baseStation":"yXoP","musicHash":"FNei","sdkVersion":"Vkrm","version":"XKTz","photosHash":"GLBj","brightness":"qm7W","startupTime":"oA3w","currentWifi":"bOhy","battery":"89Fw","existQemu":"JC9t","UDID":"NfP-","platform":"0pT8","availableSD":"Uaj4","totalMemory":"oUvy","simulator":"YIxZ","cellularIP":"PneH","IMSI":"7UTv","bootloader":"O0oS","board":"hZFp","totalSD":"LtgM","availableSystem":"H6Rg","product":"qHkh","sensors":"4i37","wifiList":"wXg4","bluetooth":"qCjR","IMEI":"9POg","nearbyBaseStation":"EyOF","appVersion":"wfQn","manufacturer":"EAAo","device":"JjpN","brand":"BKn7","activeTime":"R7of","rooted":"UqMW","contactsHash":"kClR","cpuType":"aKfq","cpuABI":"U3oU"}


def get_base_url(config_path='H:\\DFP-interface\\config.yaml'):
    application_yaml = open(config_path)
    application = yaml.load(application_yaml)
    application_yaml.close()
    return application['dfp.url']


def get_preFetch():
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'public/downloads/preFetch.js')
    if r.status_code != 200:
        print "get_preFetch fail"
    else:
        print "get preFetch success"


def get_rd():
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'public/downloads/extra.js?includes=rd')
    if r.status_code != 200:
        print "get_rd fail"
    else:
        print "get_rd success"


def params_map(platform=None):
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'protected/paramsMap?platform=' + platform)
    return json.loads(r.text)


def compare_paramsmap(platform):
    params_from_server = params_map(platform=platform)
    if cmp(params_from_server, param[platform]) != 0:
        print "%s platform param map wrong!" % platform
    else:
        print "%s platfrom param map correct" % platform


def global_stat():
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'protected/globalStat')
    if r.status_code != 200:
        print "global_stat connection error"
    elif r.status_code == 200:
        if json.loads(r.text)['stat']['invokerCount'] != 0:
            print json.loads(r.text)['stat']['invokerCount']


def daily_stat():
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'protected/dailyStat')
    if r.status_code != 200:
        print "daily_stat connection error"
    elif r.status_code == 200:
        print json.loads(r.text)['default']
        print " daily_stat success"


def dfp_about():
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'protected/about')
    if r.status_code != 200:
        print "dfp_about connection error"
    elif r.status_code == 200:
        print json.loads(r.text)['version']
        print "dfp_about success"


def js_download():
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'public/downloads/frms-fingerprint.js')
    if r.status_code != 200:
        print "download js error"
    elif r.status_code == 200:
        print "js_download success"


def view_key():
    config_public = 'MIGWMA0GCSqGSIb3DQEBAQUAA4GEADCBgAJ5AL2KNNzht9zQVQPiXcpQGC0kd0aMUJscviBkaaGRL36U26r9UvG7yTVSYxLWRN7FU7eYy2J4otWLASk6atN8LEYkd5KQKuCn12Asp4T8JbJHi805sUvjrN5BfjHW+uN104CRwb/bK/2hHCcLmvRl5wu5MCRmbvZ8uwIDAQAB'
    config_private = 'MIICUgIBADANBgkqhkiG9w0BAQEFAASCAjwwggI4AgEAAnkAvYo03OG33NBVA+JdylAYLSR3RoxQmxy+IGRpoZEvfpTbqv1S8bvJNVJjEtZE3sVTt5jLYnii1YsBKTpq03wsRiR3kpAq4KfXYCynhPwlskeLzTmxS+Os3kF+Mdb643XTgJHBv9sr/aEcJwua9GXnC7kwJGZu9ny7AgMBAAECeQCHzHzBgOtFxvISXV5LdIVN2qGmpyOdbsN929Oe0bHQpICaivOhhKTNkmCvf1tKrOClW1DlFX+9NeG4E0R3nLTQ95TwPvJ7XYTRVDBnhxe8knWvp7+omhN1Z2e0gGFokHMX/7SCtQY+BntpFnfg8b6rWHPxYyqnkKECPQDxNly9JwDKUf7IHWridXqB/j3IS5LDY7mSSBsfcUk9LzURYOu4wY6bjLkAH9sGFLxhoIK30iagxzJpATECPQDJKOKlcSrefN3aIwUF95ZpbscfM1Cf5+4unBN2fi404p9XLAHrqVW+XIr+yaIXCW8LXG/f6PA3tRaJgasCPQDNnxThXe1LiyhQ+NrTn2fGhq+uHdZHX6yiqXsNi6nuUV7AqMlo3v8tVIGkPIOeJHEOHCEyiB/LsOMlJhECPFrRTqIK2aPhE/gr31S2Vv36uYNok3neKDZ62H6isRHHTtD4WVWf+cob1dT6C2gDJlMmxIt+ixVbeHVUSQI9AJbjeZfL44/NiytYzNSQ8kz+mXGZOhB7VdwFoIu+SNwrlfsbwlRaom65/kK6SUoxwN1icoFLinx5vRj4aA=='
    r = requests.get(url=get_base_url(
        config_path='H:\DFP-interface\config.yaml') + 'protected/viewKey')
    if r.status_code != 200:
        print "view_key error"
    elif r.status_code == 200:
        if json.loads(r.text)['public'] == config_public and json.loads(r.text)['private'] == config_private:
            print "view_key success"


def main():
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
    


if __name__ == '__main__':
    main()
