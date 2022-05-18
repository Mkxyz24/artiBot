
from ast import Try
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
    desiredCourses = ["CSE 511", "CSE 512", "CSE 535", "CSE 546", "CSE 551", "CSE 552", "CSE 564",
                         "CSE 571", "CSE 573", "CSE 575", "CSE 576", "CSE 578", "CSE 579"]
    a_c = ["CSE 463", "CSE 511", "CSE 512", "CSE 535", "CSE 543", "CSE 546", "CSE 551", "CSE 573", "CSE 575",
                 "CSE 576", "CSE 578", "CSE 579"]
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
        
        while(True):
            try:
                #wait time for page to load
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "Any_23"))
                )

                #data processing
                table = driver.find_element(By.ID,"CatalogList")
                tbody = table.find_element(By.TAG_NAME,"tbody")
                rows = tbody.find_elements(By.TAG_NAME,"tr")
                for row in rows:
                    cols= row.find_elements(By.TAG_NAME,"td")
                    titleCol = cols[0]


                    fallCourses.append(titleCol.text)
                    dic = {}
                    if titleCol.text in desiredCourses:
                        nameCol = cols[1]
                        name = nameCol.find_element(By.CLASS_NAME,"class-results-drawer")
                        
                        #non reserved
                        name.click()
                        try:
                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "#reserved-tbl > tbody .total"))
                            )     
                            nr_text = element.text
                            nr = None
                            if nr_text!=None:
                                nr_text = nr_text.replace('Non Reserved Available Seats: ','')
                                #print(nr + " " + name.text)
                                nr = int(nr_text)
                            dic['available'] = nr

                        except NoSuchElementException:
                            print("cannot find non reserved table - no such element")
                            pass
                        except TimeoutException:
                            print("cannot find non reserved table - timeout")
                            pass
                        #end of non-reserved
                        if(dic['available'] > 0):
                            availableCol = row.find_element(By.CLASS_NAME,"availableSeatsColumnValue")
                            values = availableCol.find_elements(By.TAG_NAME, "span")
                            dic['title'] = titleCol.text
                            dic['name'] = name.text
                            #dic['available'] = int(values[0].text)
                            dic['total'] = int(values[2].text)

                            data.append(dic)
                
                #wait for next page button and click it
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "Any_24"))
                )
                #next page button id Any_24
                element.click()
                #wait to load
                element = WebDriverWait(driver, 10).until(
                    EC.staleness_of(element)
                )   
            

            except TimeoutException:
                print('next page element not found')
                break

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






