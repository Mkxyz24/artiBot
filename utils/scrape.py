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
import subprocess


def set_action_output(output_name, value) :
    """Sets the GitHub Action output.

    Keyword arguments:
    output_name - The name of the output
    value - The value of the output
    """
    print(value)
    if "GITHUB_OUTPUT" in os.environ :
        with open(os.environ["GITHUB_OUTPUT"], "a") as f :
            print("{0}={1}".format(output_name, value), file=f)
        e = "echo '${{steps.main.outputs.output1}}'"
        subprocess.call(e, shell=True)


def get_courses():
    load_dotenv()
    url = str(os.getenv('URL'))
    #for local
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("--window-size=1440,900")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="107.0.5304.62").install()),options=options)

    #for github actions
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1440,900")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    data = []
    output = ""
    fall22 = ['92030', '70517', '90104', '97669', '98388', '95561',
                     '96730', '76770', '75623', '83713', '96290',
                     '86207', '96593', '76055', '86208', '77802', '83405', '96739', '78302',
                     '98225','84856', '86209', '96727', '87271','97807']
    spring22 = ['20829','25642','30492','22119','23711','29446']
    # spring22 = ['29399']
    currentSem = spring22
    term_select_value = "2231"
    try:
        for c_num in currentSem:
            dic = {}
            try:
                WebDriverWait(driver, 5,poll_frequency=1).until(
                    EC.text_to_be_present_in_element_value((By.ID,"term"),term_select_value)
                )     
                subject_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME,"subject"))
                )
                subject_element.send_keys(Keys.CONTROL, "a")
                subject_element.send_keys(Keys.DELETE)
                # subject_element.send_keys(Keys.COMMAND, "a")
                # subject_element.send_keys(Keys.BACK_SPACE)
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
                
                keyword_element.send_keys(Keys.CONTROL, "a")
                keyword_element.send_keys(Keys.DELETE)
                # keyword_element.send_keys(Keys.COMMAND, "a")
                # keyword_element.send_keys(Keys.BACK_SPACE)
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
                s_title = "Results for CSE "+c_num
                # output = output+s_title+"\n"
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element((By.CLASS_NAME,"search-title"),s_title)
                )  

                search_titles = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME,"search-title"))
                ) 
                open = 1
                for s_title in search_titles:
                    if(s_title.text == "No classes found"):
                        open = 0
                if open == 0:
                    # print("No classes found, going for the next course in list")
                    # output = output + "No classes found, going for the next course in list" + "\n"
                    continue
                c_num_retrieved = ""
                while c_num_retrieved == "":
                    course_num = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,".class-results-cell.number"))
                    )
                    if course_num.text == c_num:
                        c_num_retrieved = c_num
                # keyword_element.send_keys(Keys.CONTROL, "a")
                # keyword_element.send_keys(Keys.DELETE)
                # WebDriverWait(driver, 5).until(
                #     EC.text_to_be_present_in_element_value((By.NAME,"keywords"),"")
                # )   
                course = driver.find_element(By.CSS_SELECTOR,".class-results-cell.course")
                number = driver.find_element(By.CSS_SELECTOR,".class-results-cell.number")
                
                id = number.text.replace(' ','')
                title = driver.find_element(By.CSS_SELECTOR,".class-results-cell.title")
                seats = driver.find_element(By.CSS_SELECTOR,".class-results-cell.seats")
                icon_svg = seats.find_element(By.TAG_NAME,"svg")
                data_icon = icon_svg.get_attribute("data-icon")

                if data_icon == "circle":
                    output = output + ' ' + id + " available" + "\n"
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
                        # print("cannot find non reserved table - no such element")
                        output = output + "cannot find non reserved table - no such element" + "\n"
                        # available = cols[10]
                        # open = available.find_element(By.TAG_NAME,"span")
                        dic['available'] = int(open)
                        #continue
                    else:
                        # element = WebDriverWait(driver, 3).until(
                        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".reserved-seats > tbody > tr:last-child"))
                        # ) 
                        nr_text = element.text
                        nr = None
                        driver.execute_script('arguments[0].click()', title)
                        if nr_text!=None:
                            nr_text = nr_text.replace('Non Reserved Available Seats: ','')
                            nr = int(nr_text)
                            dic['available'] = nr
                        else:
                            # dic["available"] = int(open)
                            continue
                else:
                    # print('seats not available for this course')
                    # output = output + "seats not available for this course" + "\n"
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
                # print("cannot find class results drawer - timed out")
                output = output + "cannot find class results drawer no such element- timed out" + "\n"
                # print(traceback.format_exc())
                output = output + traceback.format_exc() + "\n"
                # or
                # print(sys.exc_info()[2])
                pass
            except TimeoutException:
                # print("cannot find class results drawer - timed out")
                output = output + "cannot find non reserved table - timeout" + "\n"
                # print(traceback.format_exc())
                output = output + traceback.format_exc() + "\n"
                # or
                # print(sys.exc_info()[2])
                pass
            except Exception as e:
                # print("error while getting non reserved seats: ", e)
                output = output + "error while getting non reserved seats:" + "\n"
                # print(traceback.format_exc())
                output = output + traceback.format_exc() + "\n"
                # or
                # print(sys.exc_info()[2])
                
                pass


    except Exception as e:
        # print(traceback.format_exc())
        output = output + traceback.format_exc() + "\n"
        # or
        # print(sys.exc_info()[2])
        driver.quit()
    finally:
        print(output)
        # set_action_output("output1",output)
        driver.quit()
        return data