
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import traceback
import sys


def get_courses():
    url = "https://webapp4.asu.edu/catalog/"

    #for local
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="101.0.4951.41").install()))

    #for github actions
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    data = []
    desiredCourses = ["CSE 511", "CSE 546", "CSE 551", "CSE 569", "CSE 571", "CSE 575", "CSE 576"]
    fallCourses = []
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchTypeAllClass"))
        )
        element.click()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "subjectEntry"))
        )
        element.send_keys("CSE")
        element.send_keys(Keys.RETURN)
        
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Any_23_1"))
        )
        #3rd page button id Any_23_1
        element.click()
        #wait to load
        element = WebDriverWait(driver, 10).until(
            EC.staleness_of(element)
        )   

        table = driver.find_element(By.ID,"CatalogList")
        tbody = table.find_element(By.TAG_NAME,"tbody")
        rows = tbody.find_elements(By.TAG_NAME,"tr")
        for row in rows:
            cols= row.find_elements(By.TAG_NAME,"td")
            titleCol = cols[0]
            nameCol = cols[1]
            name = nameCol.find_element(By.CLASS_NAME,"class-results-drawer")
            availableCol = row.find_element(By.CLASS_NAME,"availableSeatsColumnValue")
            values = availableCol.find_elements(By.TAG_NAME, "span")

            fallCourses.append(titleCol.text)
            dic = {}
            if titleCol.text in desiredCourses:
                dic['title'] = titleCol.text
                dic['name'] = name.text
                dic['available'] = int(values[0].text)
                dic['total'] = int(values[2].text)
                if(dic['available'] > 0):
                    data.append(dic)

    except Exception as e:
        print(traceback.format_exc())
        # or
        print(sys.exc_info()[2])
        driver.quit()
    finally:
        driver.quit()
        #print(data)
        # for course in data:
        #     print(course['available'])
        return data






