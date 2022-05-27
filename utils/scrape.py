
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
import os
from dotenv import load_dotenv


def get_courses():
    load_dotenv()
    url = os.getenv('URL')

    #for local
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="101.0.4951.41").install()))

    #for github actions
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    data = []

    fall22Courses = ['92030', '70517', '81289', '90104', '97669',
                     '96730', '76770', '98070', '75623', '83713', '96290', '78322',
                     '86207', '96593', '76055', '86208', '77802', '83405', '96739', '78302',
                     '84856', '86209', '96727', '87271']
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "searchTypeAllClass"))
        )
        #element.click()
        driver.execute_script('arguments[0].click()', element)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "subjectEntry"))
        )
        element.send_keys("CSE")
        element.send_keys(Keys.RETURN)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,".pagination"))
        )

        pages = driver.find_elements(By.CSS_SELECTOR,".change-page")
        #print(len(pages))
        
        for i in range(len(pages)):
            try:
                #wait time for page to load
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "Any_23"))
                )

                #data processing
                table = driver.find_element(By.ID,"CatalogList")
                tbody = table.find_element(By.TAG_NAME,"tbody")
                rows = tbody.find_elements(By.TAG_NAME,"tr")
                for row in rows:
                    cols= row.find_elements(By.TAG_NAME,"td")
                    titleCol = cols[0]
                    courseId = cols[2]
                    dic = {}
                    id = courseId.text.replace(' ','')
                    if id in fall22Courses:
                        nameCol = cols[1]
                        
                        try:
                            name = WebDriverWait(nameCol, 10).until(
                                EC.element_to_be_clickable((By.CLASS_NAME,"class-results-drawer"))
                            )
                            #nameCol.find_element(By.CLASS_NAME,"class-results-drawer")
                        
                            #non reserved
                            driver.execute_script('arguments[0].click()', name)
                            #name.click()
                            try:
                                element = WebDriverWait(driver, 3).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "#reserved-tbl > tbody .total"))
                                )    
                            except TimeoutException:
                                print("cannot find non reserved table - no such element")
                                available = cols[10]
                                open = available.find_element(By.TAG_NAME,"span")
                                print(open.text)
                                dic['available'] = int(open.text)
                                #continue
                            else:
                                nr_text = element.text
                                nr = None
                                if nr_text!=None:
                                    nr_text = nr_text.replace('Non Reserved Available Seats: ','')
                                    #print(nr + " " + name.text)
                                    nr = int(nr_text)
                                    dic['available'] = nr
                                else:
                                    #dic["available"] = None
                                    continue

                        except NoSuchElementException:
                            print("cannot find class results drawer - timed out")
                            pass
                        except TimeoutException:
                            print("cannot find non reserved table - timeout")
                            pass
                        except:
                            print("error while getting non reserved seats")
                            pass
                        #end of non-reserved
                        if(dic['available'] > 0):
                            availableCol = row.find_element(By.CLASS_NAME,"availableSeatsColumnValue")
                            values = availableCol.find_elements(By.TAG_NAME, "span")
                            dic['title'] = titleCol.text
                            dic['name'] = nameCol.text
                            dic['id'] = id
                            #dic['available'] = int(values[0].text)
                            dic['total'] = int(values[2].text)

                            data.append(dic)
                
                #wait for next page button and click it
                if(i != (len(pages)-1)):   #if not last page
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "Any_24"))
                    )
                    #next page button id Any_24
                    driver.execute_script('arguments[0].click()', element)
                #element.click()
                #wait to load
                    element = WebDriverWait(driver, 10).until(
                        EC.staleness_of(element)
                    )   
            

            except TimeoutException:
                print('next page element not found')
                #break

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






