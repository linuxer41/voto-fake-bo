from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from typing import Optional
import time
from log import logger


def get_driver(*, driver_type: str = 'firefox', headless: bool = False) -> Optional[WebDriver]:
    """ retorna un driver boot, firefox por defecto.
    use [headless = true] para iniciar el driver sin intefaz grafica"""
    if driver_type == "firefox":
        options = Options()
        if headless:
            options.headless = True
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)  # for private
        driver = webdriver.Firefox(options=options, executable_path="./geckodriver", service_log_path='/dev/null',
                                   firefox_profile=firefox_profile)
        driver.implicitly_wait(10)  # for implicit wait
        return driver
    return None


def run(*, driver: WebDriver, url: str, opt: int):
    driver.get(url)
    try:
        main_node = driver.find_element_by_xpath("/html/body/form/div[1]")
        els: list = main_node.find_elements_by_tag_name("input")
        el = els[int(opt)-1]
        driver.execute_script("arguments[0].click();", el)
        # delay
        time.sleep(3)
        logger.info("ok")
    except:  # noqa
        logger.info("ko")
    finally:
        driver.close()


options = {
    "1": "Creemos",
    "2": "ADN",
    "3": "MAS",
    "4": "PDC",
    "5": "PAN-BOL",
    "6": "Libre",
    "7": "CC",
    "8": "Juntos",
}

if __name__ == "__main__":
    from multiprocessing import cpu_count
    import threading
    
    votes = 0
    url = "https://yoparticipo.voto/"
    votes_for = 2  # 1 = Creemos, 2 = ADN, 3 = MAS, ........

    cores = cpu_count()
    logger.info(f"cpu cores: {cores}")
    while True:
        driver = get_driver(headless=False)
        ## mayor numero de cores, mayor rapidez de ejecucion. threads solo pueden ejecutarse
        ## cuando hay 2 o mas nucleos en la cpu
        if cores > 1 :
            threading.Thread(target=run, kwargs={"driver": driver, "url": url, "opt": votes_for}
                            ).start()
            
        else:
            run(driver=driver, url=url, opt=votes_for)
        votes += 1
        logger.info(f"{votes} votos para: {options[str(votes_for)]}")
