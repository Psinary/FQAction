from playwright.sync_api import Playwright, sync_playwright
import time
import os,sys
import requests
from bs4 import BeautifulSoup

save_path = "v2rayse_new.yaml"
os.chdir(sys.path[0])

def get_password():
    x = requests.get('https://t.me/s/changfengchannel',verify=True)
    print("打开订阅频道成功")
    bs_1 = BeautifulSoup(x.text, 'lxml')
    password = bs_1.find("tg-spoiler").text
    print("验证密码：" + password)
    return password

def run(playwright: Playwright,password,save_path) -> None:
    browser = playwright.webkit.launch(headless=True)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://v2rayse.com/free-node/
    page.goto("https://v2rayse.com/free-node/")

    # Click input[type="password"]
    page.locator("input[type=\"password\"]").click()

    # Fill input[type="password"]
    page.locator("input[type=\"password\"]").fill(password)

    # Click button:has-text("确定")
    page.locator("button:has-text(\"确定\")").click()

    # Click div[role="button"]:has-text("10")
    page.locator("div[role=\"button\"]:has-text(\"10\")").click()

    # Click text=全部
    page.locator("text=全部").click()

    # Click [aria-label="速度\: ：未排序。 点击以升序排列。"] i
    page.locator("[aria-label=\"速度\\: ：未排序。 点击以升序排列。\"] i").click()

    # Click [aria-label="速度\: ：升序排列。 点击以降序排列。"] i
    page.locator("[aria-label=\"速度\\: ：升序排列。 点击以降序排列。\"] i").click()

    # Click .v-input--selection-controls__input > .v-icon >> nth=0
    page.locator(".v-input--selection-controls__input > .v-icon").first.click()

    # Click button:has-text("转换")
    page.locator("button:has-text(\"转换\")").click()

    # Click div[role="menu"] >> text=Clash
    page.locator("div[role=\"menu\"] >> text=Clash").click()

    # Click button:has-text("下载")
    with page.expect_download() as download_info:
        page.locator("button:has-text(\"下载\")").click()
    download = download_info.value


    download_res = [download.path(), download.url, download.suggested_filename, save_path]

    print("playwright 缓存路径：" + str(download.path()))
    print("URL：" + download.url)
    print("原始名字：" + download.suggested_filename)
    print("下载路径：" + save_path)

    download.save_as(save_path)

    time_node = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    download.save_as(time_node + "_" +save_path)

    # ---------------------
    context.close()
    browser.close()

def get_changfeng_note(password,save_path):
    with sync_playwright() as playwright:
        DL = run(playwright,password=password,save_path=save_path)
    return DL

def v2rayse_update_main():
    pw = get_password()
    DL = get_changfeng_note(pw,save_path)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

if __name__ == '__main__':
    v2rayse_update_main()
