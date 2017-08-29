# coding=utf-8
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time
import yaml
from modify_timezone import call_powershell_timezone


def get_config(config_file='config.yaml'):
    application_yaml = open(config_file)
    application = yaml.load(application_yaml)
    application_yaml.close()
    return application['dfp.mongo']['host'], application['dfp.mongo']['port']


@pytest.fixture()
def base_capbility(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # if ua:
    #     pass
    # else:
    #     chrome_options.add_argument('user-agent="asdfwevcsdgeft"')
    # if language != 'zh-cn':
    #     chrome_options.add_argument('lang=en-US')
    # else:
    #     chrome_options.add_argument('lang=zh-cn')
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture()
def base_capbility_ua(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent="asdfwevcsdgeft"')
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture()
def base_capbility_proxy(request):
    chrome_options = webdriver.ChromeOptions()
    proxy = "192.168.12.36:8888"
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


def get_mongo_data(clean=True):
    host, port = get_config()
    client = MongoClient(host, port)
    collection = client.dfp.dfp
    mongo_data = collection.find_one()
    if clean:
        collection.delete_many({})
    else:
        pass
    client.close()
    return mongo_data


@pytest.fixture()
def base_capbility_language(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--lang=zh-cn')

    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture()
def base_capbility_plugins(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.mark.skip()
def test_get_normall(base_capbility):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.get(url)
    # driver.set_window_size(480,800)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']
    driver.delete_all_cookies()


@pytest.fixture()
def base_capbility_incognito(request):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--incognito')

    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.mark.skip()
def test_delete_cookie(base_capbility):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.get(url)
    # driver.set_window_size(480,800)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver.refresh()
    time.sleep(2)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_timezone(base_capbility):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.get(url)
    # driver.set_window_size(480,800)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    call_powershell_timezone()
    driver.refresh()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']
    call_powershell_timezone('-TimeZoneFriendlyName "China Standard Time"')


@pytest.mark.skip()
def test_screnn_size(base_capbility):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver.set_window_size(480, 800)
    driver.refresh()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_ua(base_capbility, base_capbility_ua):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_ua
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_language(base_capbility, base_capbility_language):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_language
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_incognito(base_capbility, base_capbility_incognito):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_incognito
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_proxy(base_capbility, base_capbility_proxy):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_proxy
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


# @pytest.mark.skip()
def test_no_plugins(base_capbility, base_capbility_plugins):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_plugins
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]')))
    print driver.find_element_by_xpath('//*[@id="inner"]').text
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
