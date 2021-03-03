from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from collections import deque

profile = webdriver.FirefoxProfile()

dv = webdriver.Firefox(executable_path="D:\\WebDriver\\geckodriver.exe", firefox_profile=profile)
queue = deque()


def get_items(kw, driver):
    driver.get("https://www.lagou.com/")
    wait = WebDriverWait(driver, 10)
    driver.find_element_by_id("search_input").send_keys(kw)
    driver.find_element_by_id("search_button").click()
    while True:
        items = driver.find_elements_by_css_selector(".position_link")
        next_clickable = ec.element_to_be_clickable(
            ec.presence_of_element_located((By.CSS_SELECTOR, "[action='next']")))
        if next_clickable:
            wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, ".item_con_list li")))
            for i in items:
                link = i.find_element_by_css_selector(".position_link").get_attribute("href")
                if link not in queue:
                    queue.appendleft(link)
                    print(link)

            print(driver.find_element_by_css_selector(".pager_is_current").text)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "[action='next']"))).click()
        break
    driver.close()


def parse_detail(driver):
    # while len(queue) > 0:
        # url = queue.pop()
        # driver.get(url)
    driver.get("https://www.lagou.com/jobs/8063954.html?show=0070a35276cb4131bd4a5ec5a709d1e7")
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, ".job_bt")))
    # print(driver.find_elements_by_css_selector(".job-detail"))
    return {
        'title': driver.find_element_by_css_selector(".position-head-wrap-name").text,
        'sec': [i.text.strip() for i in driver.find_elements_by_css_selector(".job-detail br")],
        'salary': driver.find_element_by_css_selector(".salary").text,
        'city': driver.find_element_by_css_selector(".job_request span:nth-child(2)").text,
        'years': driver.find_element_by_css_selector('.job_request span:nth-child(3)').text,
        'education': driver.find_element_by_css_selector('.job_request span:nth-child(4)').text
    }


if __name__ == '__main__':
    keyword = "GO"
    # get_items(kw=keyword, driver=dv)
    print(parse_detail(dv))
    dv.quit()
