# coding=utf-8
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pymongo import MongoClient
import time
import yaml
from modify_timezone import call_powershell_timezone


def get_config(config_file='config.yaml'):
    application_yaml = open(config_file)
    application = yaml.load(application_yaml)
    application_yaml.close()
    return application['dfp.mongo']['host'], application['dfp.mongo']['port']


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


class base_line:
    def __init__(self):
        self.url = None
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--lang=en-us')
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def set_url(self, url):
        self.url = url

    def setup(self):
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 7).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
        except TimeoutException:
            self.driver.refresh()
            time.sleep(3)
        dfp = self.driver.get_cookie(name='BSFIT_OkLJUJ')['value']
        # assert self.driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']
        # assert self.driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data(clean=False)['dfp']
        self.driver.delete_all_cookies()
        self.driver.quit()
        return dfp

    def setup_timezone(self):
        call_powershell_timezone()
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 13).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
        except TimeoutException:
            self.driver.refresh()
            time.sleep(3)
        dfp = self.driver.get_cookie(name='BSFIT_OkLJUJ')['value']
        # assert self.driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']
        # assert self.driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data()['dfp']
        self.driver.delete_all_cookies()
        self.driver.quit()
        return dfp

    def mongo_teardown(self):
        call_powershell_timezone('-TimeZoneFriendlyName "China Standard Time"')
        get_mongo_data()


@pytest.fixture()
def base_capbility(request):
    # firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--lang=en-us')
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


@pytest.fixture()
def base_capbility_language(request):
    chrome_options = webdriver.ChromeOptions()

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


@pytest.fixture()
def base_capbility_incognito(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--incognito')

    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture()
def ff_base_capbility(request):
    binary = FirefoxBinary()
    binary.add_command_line_options('-headless')
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"D:\geckodriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture()
def ff_base_capbility_ua(request):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "whatever you want")
    driver = webdriver.Firefox(profile, executable_path=r"D:\geckodriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture()
def ff_base_capbility_incognito(request):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    binary = FirefoxBinary()
    binary.add_command_line_options('-headless')
    driver = webdriver.Firefox(profile, firefox_binary=binary, executable_path=r"D:\geckodriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture()
def ff_base_capbility_language(request):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("intl.accept_languages", "zh-cn")
    driver = webdriver.Firefox(profile, executable_path=r"D:\geckodriver.exe")

    def fin():
        print "browser close"
        driver.quit()

    request.addfinalizer(fin)
    return driver


# @pytest.mark.skip()
def test_get_normall(base_capbility):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data()['dfp']


# @pytest.mark.skip()
def test_delete_cookie(base_capbility):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver.refresh()
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_timezone():
    driver = base_line()
    url = "http://10.100.1.53:9080/public/index.html"
    driver.set_url(url)
    dfp_before = driver.setup()
    driver2 = base_line()
    driver2.set_url(url)
    dfp_after = driver2.setup_timezone()
    driver2.mongo_teardown()
    assert dfp_after != dfp_before


# @pytest.mark.skip()
def test_screnn_size(base_capbility):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver.set_window_size(480, 800)
    driver.refresh()
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data()['dfp']


# @pytest.mark.skip()
def test_ua(base_capbility, base_capbility_ua):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_ua
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text != get_mongo_data()['dfp']


# @pytest.mark.skip()
def test_language(base_capbility, base_capbility_language):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_language
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']


# @pytest.mark.skip()
def test_incognito(base_capbility, base_capbility_incognito):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_incognito
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_proxy(base_capbility, base_capbility_proxy):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_proxy
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


# @pytest.mark.skip()
def test_no_plugins(base_capbility, base_capbility_plugins):
    driver = base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = base_capbility_plugins
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_ff_get_normall(ff_base_capbility):
    driver = ff_base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_ff_delete_cookie(ff_base_capbility):
    driver = ff_base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver.refresh()
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_ff_screnn_size(ff_base_capbility):
    driver = ff_base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver.set_window_size(480, 800)
    driver.refresh()
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.get_cookie(name='BSFIT_OkLJUJ')['value'] == get_mongo_data()['dfp']


@pytest.mark.skip()
def test_ff_ua(ff_base_capbility, ff_base_capbility_ua):
    driver = ff_base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = ff_base_capbility_ua
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text != get_mongo_data()['dfp']


# @pytest.mark.skip()
def test_ff_incognito(ff_base_capbility, ff_base_capbility_incognito):
    driver = ff_base_capbility
    url = "http://10.100.1.53:9080/public/index.html"
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data(clean=False)['dfp']
    driver.delete_all_cookies()
    driver = ff_base_capbility_incognito
    url = 'http://10.100.1.53:9080/public/index.html'
    driver.maximize_window()
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]')))
    except TimeoutException:
        driver.refresh()
        time.sleep(3)
    assert driver.find_element_by_xpath('//*[@id="inner"]').text == get_mongo_data()['dfp']
