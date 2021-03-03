from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

profile = webdriver.FirefoxProfile()

dv = webdriver.Firefox(executable_path="D:\\WebDriver\\geckodriver.exe", firefox_profile=profile)


def get_items(kw, driver):
    driver.get("https://www.zhipin.com/guangzhou/?ka=header-home")

    driver.find_element_by_class_name("ipt-search").send_keys(kw)
    driver.find_element_by_class_name("btn-search").click()

    for _ in range(100):
        items = driver.find_elements_by_css_selector(".job-title")
        wait = WebDriverWait(driver, 10)
        next_clickable = ec.element_to_be_clickable(ec.presence_of_element_located((By.CSS_SELECTOR, ".page .next")))
        if next_clickable:
            wait.until(ec.presence_of_all_elements_located((By.XPATH, "//div[@class='job-list']/ul/li")))
            for i in items:
                print(i.find_element_by_xpath("./span/a").get_attribute("href"))
            print("第", driver.find_element_by_css_selector(".page .cur").text, "页爬取完成")
            wait.until(ec.presence_of_element_located((By.XPATH, "//a[@ka='page-next']"))).click()
        break
    driver.quit()


if __name__ == '__main__':
    keyword = "Go"
    get_items(kw=keyword, driver=dv)

