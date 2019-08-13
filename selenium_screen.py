from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


def read_url():
    df_info = pd.read_excel('C:/Users/Administrator/Desktop/D88品牌库最终_本地.xlsx', skiprows=254, usecols=[1, 2], names=['brand_name', 'url'])
    df_info = df_info.dropna()
    info_list = df_info.values.tolist()
    return info_list


def take_screenshot(browser):
    browser.maximize_window()
    # 以下代码是将浏览器页面拉到最下面。
    # browser.execute_script("""
    #     (function () {
    #         var y = 0;
    #         var step = 100;
    #         window.scroll(0, 0);
    #         function f() {
    #             if (y < document.body.scrollHeight) {
    #                 y += step;
    #                 window.scroll(0, y);
    #                 setTimeout(f, 100);
    #             } else {
    #                 window.scroll(0, 0);
    #                 document.title += "scroll-done";
    #             }
    #         }
    #         setTimeout(f, 1000);
    #     })();
    # """)

    time.sleep(1)


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    info_list = read_url()
    startTime = time.time()
    for info in info_list[:5]:
        screen_time = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        name = info[0].strip() + screen_time
        print(name)
        driver.get(info[1])
        time.sleep(1)
        driver.save_screenshot('D:/yanzhengma/' + name + '.png')
    driver.quit()
    endTime = time.time()
    print('共计耗时：%s' % (endTime - startTime))


if __name__ == "__main__":
    main()

