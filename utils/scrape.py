
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
    url = str(os.getenv('URL'))
    print(url)
    #for local
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="107.0.5304.62").install()))

    #for github actions
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    data = []

    fall22 = ['92030', '70517', '90104', '97669', '98388', '95561',
                     '96730', '76770', '75623', '83713', '96290',
                     '86207', '96593', '76055', '86208', '77802', '83405', '96739', '78302',
                     '98225','84856', '86209', '96727', '87271','97807']
    spring22 = ['20829','25642','30492','22119','23711','29399']
    currentSem = spring22
    term_select_value = "2231"
    try:
        for c_num in currentSem:
            print(c_num)
            dic = {}
            try:
                WebDriverWait(driver, 5,poll_frequency=1).until(
                    EC.text_to_be_present_in_element_value((By.ID,"term"),term_select_value)
                )     
                subject_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME,"subject"))
                )
                subject_element.send_keys(Keys.COMMAND, "a")
                subject_element.send_keys(Keys.BACKSPACE)
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element_value((By.NAME,"subject"),"")
                )   
                subject_element.send_keys("CSE")
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element_value((By.NAME,"subject"),"CSE")
                )   
                # driver.implicitly_wait(2)
                keyword_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME,"keywords"))
                )
                keyword_element.send_keys(Keys.COMMAND, "a")
                keyword_element.send_keys(Keys.BACKSPACE)
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element_value((By.NAME,"keywords"),"")
                )   
                keyword_element.send_keys(c_num)
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element_value((By.NAME,"keywords"),c_num)
                )   
                keyword_element.send_keys(Keys.RETURN)
                # WebDriverWait(driver, 20).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR,".class-results-cell.seats"))
                # ) 
                WebDriverWait(driver, 20).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR,".class-results-cell.number"),c_num)
                ) 
                
                # keyword_element.send_keys(Keys.CONTROL, "a")
                # keyword_element.send_keys(Keys.DELETE)
                # WebDriverWait(driver, 5).until(
                #     EC.text_to_be_present_in_element_value((By.NAME,"keywords"),"")
                # )   
                course = driver.find_element(By.CSS_SELECTOR,".class-results-cell.course")
                # print(course.text)
                number = driver.find_element(By.CSS_SELECTOR,".class-results-cell.number")
                
                id = number.text.replace(' ','')
                # print(id)
                title = driver.find_element(By.CSS_SELECTOR,".class-results-cell.title")
                seats = driver.find_element(By.CSS_SELECTOR,".class-results-cell.seats")
                icon_svg = seats.find_element(By.TAG_NAME,"svg")
                data_icon = icon_svg.get_attribute("data-icon")

                if data_icon == "circle":
                    print('available',id)
                    seats_list = seats.text.split()
                    totalseats = seats_list[2]
                    open = seats_list[0]
                    
                    # dic['available'] = 
                    
                    try:
                        driver.execute_script('arguments[0].click()', title)
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".reserved-seats > tbody > tr:last-child"))
                        )    

                    except TimeoutException:
                        print("cannot find non reserved table - no such element")
                        # available = cols[10]
                        # open = available.find_element(By.TAG_NAME,"span")
                        #print(open.text)
                        dic['available'] = int(open)
                        #continue
                    else:
                        # element = WebDriverWait(driver, 3).until(
                        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".reserved-seats > tbody > tr:last-child"))
                        # ) 
                        nr_text = element.text
                        # print(nr_text)
                        nr = None
                        driver.execute_script('arguments[0].click()', title)
                        if nr_text!=None:
                            nr_text = nr_text.replace('Non Reserved Available Seats: ','')
                            #print(nr + " " + name.text)
                            nr = int(nr_text)
                            dic['available'] = nr
                        else:
                            # dic["available"] = int(open)
                            continue
                else:
                    print('not available',id)
                    dic['available'] = 0

                if(dic['available'] > 0):
                    # availableCol = row.find_element(By.CLASS_NAME,"availableSeatsColumnValue")
                    # values = availableCol.find_elements(By.TAG_NAME, "span")
                    dic['title'] = course.text
                    dic['name'] = title.text
                    dic['id'] = id
                    #dic['available'] = int(values[0].text)
                    dic['total'] = totalseats
                    data.append(dic)
            except NoSuchElementException:
                print("cannot find class results drawer - timed out")
                pass
            except TimeoutException:
                print("cannot find non reserved table - timeout")
                pass
            except:
                print("error while getting non reserved seats")
                pass


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

    # try:
    #     # element = WebDriverWait(driver, 10).until(
    #     #     EC.element_to_be_clickable((By.ID, "searchTypeAllClass"))
    #     # )
    #     # #element.click()
    #     # driver.execute_script('arguments[0].click()', element)
    #     WebDriverWait(driver, 5,poll_frequency=1).until(
    #         EC.text_to_be_present_in_element_value((By.ID,"term"),term_select_value)
    #     )     
    #     element = WebDriverWait(driver, 5).until(
    #         EC.presence_of_element_located((By.NAME,"subject"))
    #     )
    #     element.send_keys("CSE")
    #     # driver.implicitly_wait(2)
    #     WebDriverWait(driver, 5).until(
    #         EC.text_to_be_present_in_element_value((By.NAME,"subject"),"CSE")
    #     )       
    #     element.send_keys(Keys.RETURN)
    #     # driver.implicitly_wait(1)
    #     # element = WebDriverWait(driver, 20).until(
    #     #     EC.element_to_be_clickable((By.ID,"search-button"))
    #     # )
    #     # driver.execute_script('arguments[0].click()', element)
    #     element = WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR,".pagination"))
    #     )

    #     pages = driver.find_elements(By.CSS_SELECTOR,".page-item")
    #     #print(len(pages))

    #     for i in range(len(pages)):
    #         try:
    #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #             #wait time for page to load
    #             element = WebDriverWait(driver, 20).until(
    #                 EC.presence_of_element_located((By.CSS_SELECTOR,".pagination"))
    #             )

    #             # #data processing
    #             # table = driver.find_element(By.ID,"CatalogList")
    #             # tbody = table.find_element(By.TAG_NAME,"tbody")
    #             # rows = tbody.find_elements(By.TAG_NAME,"tr")
    #             table = driver.find_element(By.ID,"class-results")
    #             cresults = table.find_element(By.CLASS_NAME,"class-results-rows")
    #             # rows = cresults.find_elements(By.XPATH,"//div[contains(concat(' ', @class, ' '), ' class-accordion ')]")
    #             rows = cresults.find_elements(By.CLASS_NAME,"class-accordion")
    #             # cols = rows[0].find_elements(By.XPATH,"//div[contains(@class, 'class-results-cell')]")
    #             # print(cols)
    #             for row in rows:
    #                 # cols = row.find_elements(By.CLASS_NAME,"")
    #                 # print(len(cols))
    #                 #cols= row.find_elements(By.TAG_NAME,"td")
    #                 course = row.find_element(By.CLASS_NAME,"course")
    #                 number = row.find_element(By.CLASS_NAME,"number")
    #                 dic = {}
    #                 id = number.text.replace(' ','')
    #                 print(id)
    #                 if id in currentSem:
    #                     title = row.find_element(By.CLASS_NAME,"title")
    #                     seats = row.find_element(By.CLASS_NAME,"seats")
    #                     try:
    #                         # course = WebDriverWait(course, 10).until(
    #                         #     EC.element_to_be_clickable((By.CLASS_NAME,"course"))
    #                         # )

    #                         #nameCol.find_element(By.CLASS_NAME,"class-results-drawer")
                        
    #                         #non reserved
    #                         #driver.execute_script('arguments[0].click()', name)
    #                         #name.click()
    #                         seats = WebDriverWait(row, 10).until(
    #                             EC.presence_of_element_located((By.CLASS_NAME,"seats"))
    #                         )
    #                         icon_svg = seats.find_element(By.TAG_NAME,"svg")
    #                         data_icon = icon_svg.get_attribute("data-icon")

    #                         #check if open or reserved
    #                         if data_icon == "circle":
    #                             print('available',id)
    #                             seats_list = seats.text.split()
    #                             totalseats = seats_list[2]
    #                             open = seats_list[0]
                                
    #                             # dic['available'] = 
                                
    #                             try:
    #                                 driver.execute_script('arguments[0].click()', title)
    #                                 element = WebDriverWait(driver, 10).until(
    #                                     EC.presence_of_element_located((By.CSS_SELECTOR, ".reserved-seats > tbody > tr:last-child"))
    #                                 )    

    #                             except TimeoutException:
    #                                 print("cannot find non reserved table - no such element")
    #                                 # available = cols[10]
    #                                 # open = available.find_element(By.TAG_NAME,"span")
    #                                 #print(open.text)
    #                                 dic['available'] = int(open)
    #                                 #continue
    #                             else:
    #                                 # element = WebDriverWait(driver, 3).until(
    #                                 #     EC.presence_of_element_located((By.CSS_SELECTOR, ".reserved-seats > tbody > tr:last-child"))
    #                                 # ) 
    #                                 nr_text = element.text
    #                                 # print(nr_text)
    #                                 nr = None
    #                                 driver.execute_script('arguments[0].click()', title)
    #                                 if nr_text!=None:
    #                                     nr_text = nr_text.replace('Non Reserved Available Seats: ','')
    #                                     #print(nr + " " + name.text)
    #                                     nr = int(nr_text)
    #                                     dic['available'] = nr
    #                                 else:
    #                                     # dic["available"] = int(open)
    #                                     continue
                                    
    #                         else:
    #                             print('not available',id)
    #                             dic['available'] = 0

    #                     except NoSuchElementException:
    #                         print("cannot find class results drawer - timed out")
    #                         pass
    #                     except TimeoutException:
    #                         print("cannot find non reserved table - timeout")
    #                         pass
    #                     except:
    #                         print("error while getting non reserved seats")
    #                         pass
    #                     #end of non-reserved
    #                     if(dic['available'] > 0):
    #                         # availableCol = row.find_element(By.CLASS_NAME,"availableSeatsColumnValue")
    #                         # values = availableCol.find_elements(By.TAG_NAME, "span")
    #                         dic['title'] = course.text
    #                         dic['name'] = title.text
    #                         dic['id'] = id
    #                         #dic['available'] = int(values[0].text)
    #                         dic['total'] = totalseats

    #                         data.append(dic)
                
    #             #wait for next page button and click it
    #             if(i != (len(pages)-1)):   #if not last page
    #                 # element = WebDriverWait(driver, 10).until(
    #                 #     EC.element_to_be_clickable((By.ID, "Any_24"))
    #                 # )
    #                 # #next page button id Any_24
    #                 # driver.execute_script('arguments[0].click()', element)
    #                 # #element.click()
    #                 # #wait to load
    #                 # element = WebDriverWait(driver, 10).until(
    #                 #     EC.staleness_of(element)
    #                 # )   
    #                 #driver.execute_script('arguments[0].click()', pages[i+1])
    #                 #pages[i+1].click()
    #                 print("page",i+1)
    #                 webdriver.ActionChains(driver).move_to_element(pages[i+1] ).click(pages[i+1] ).perform()
    #                 # element = WebDriverWait(driver, 10).until(
    #                 #     EC.staleness_of(element)
    #                 # )   

    #         except TimeoutException as e:
    #             print('next page element not found with error:',e)
    #             #break

    # except Exception as e:
    #     print(traceback.format_exc())
    #     # or
    #     print(sys.exc_info()[2])
    #     driver.quit()
    # finally:
    #     driver.quit()
    #     #print(data)
    #     # for course in data:
    #     #     print(course['available'])
    #     return data






