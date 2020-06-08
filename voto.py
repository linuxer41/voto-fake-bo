from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from typing import Optional
import time


def get_driver(*, driver_type: str = 'firefox', headless: bool = False) -> Optional[WebDriver]:
    if driver_type == "firefox":
        options = Options()
        if headless:
            options.headless = True
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)  # for private
        driver = webdriver.Firefox(options=options, executable_path="./geckodriver", service_log_path='/dev/null',
                                   firefox_profile=firefox_profile)
        driver.implicitly_wait(10)  # for implisit wait
        return driver
    return None


def run(*, driver: WebDriver, url: str, opt: int):
    driver.get(url)
    el = driver.find_element_by_xpath(f'//*[@id="{opt}"]')
    driver.execute_script("arguments[0].click();", el)
    # delay
    time.sleep(3)
    driver.close()


if __name__ == "__main__":
    from multiprocessing import cpu_count
    import threading
    counter = 0
    votes_for = 2  # 1= JUNTOS, 2 = ADN, 3 = MAS, ........
    print(f"cpu cores: {cpu_count()}")
    while True:
        driver = get_driver()
        threading.Thread(target=run, kwargs={"driver": driver, "url": "https://yoparticipo.voto/", "opt": votes_for}
                         ).start()
        counter += 1
        print(f"{counter} votos para ADN")