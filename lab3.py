import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

successful_login = False

while not successful_login:
    user_input = input("Enter your username: ")
    password_input = input("Enter your password: ")

    try:
        driver = webdriver.Chrome()

        driver.get('https://sso.aztu.edu.az/')

        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "UserId")))
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password")))

        username.send_keys(user_input)
        password.send_keys(password_input)

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div[1]/div/div/form/div[3]/button')))
        login_button.click()

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a')))

        student_section_button = driver.find_element(By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a')
        student_section_button.click()

        departments_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/a/span[2]/span')))
        departments_button.click()

        python_course_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/ul/li[3]/a')))
        python_course_button.click()

        attendance_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/div[1]/div/div[2]/a[7]')))
        attendance_button.click()

        time.sleep(10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        dates = soup.find_all('font', {'style': 'font-size:11px;'})
        attendance = soup.find_all('span', {'class': 'attend-label'})

        if dates and attendance:
            for date, attend in zip(dates, attendance):
                date_text = date.get_text().strip()
                attendance_text = attend.get_text().strip()

                if attendance_text == "i/e":
                    status = "Student attended the class."
                elif attendance_text == "q/b":
                    status = "Student did not attend the class."
                else:
                    status = f"Unknown status: {attendance_text}"

                print(f"Date: {date_text}, Status: {status}")
        else:
            print("No attendance data found.")

        successful_login = True

    except TimeoutException:
        print("Invalid username or password. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()