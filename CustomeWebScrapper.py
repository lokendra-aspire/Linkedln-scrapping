from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import pandas as pd
import tkinter as tk
from time import sleep

class WebScrapperBot:
    def __init__(self,domain:str,email,password):
        self.domain = domain
        self.root = tk.Tk()
        self.root.withdraw()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.destroy()
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_window_rect(x=0, y=0, width=self.screen_width, height=self.screen_height)
        self.wait = WebDriverWait(self.driver, 2)
        self.email = email
        self.password = password
        self.people_info_list = []
        self.data = {}

    def scraper(self):
        email_lead=str(self.domain)
        domain = email_lead.split('@')
        email = self.email
        password = self.password
        self.data = {}

        logging.warn(msg="Login LinkedIn")
        self.driver.get("https://www.linkedin.com/home")

        email_field = self.driver.find_element(By.XPATH, '//*[@id="session_key"]')
        email_field.clear()
        for i in email:
            email_field.send_keys(i)
            sleep(0.3)

        password_field = self.driver.find_element(By.XPATH, '//*[@id="session_password"]')
        password_field.clear()
        for i in password:
            password_field.send_keys(i)
            sleep(0.4)

        login_button = self.driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
        sleep(2)
        login_button.click()
        
        company_domain = f"https://{domain[1]}/"
        self.driver.get(company_domain)
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

        footer = None

        try:
            footer = self.driver.find_element(By.TAG_NAME, "footer")
        except Exception as e:
            pass

        if footer:
            anchor_tags = footer.find_elements(By.TAG_NAME, "a")
        else:
            anchor_tags = self.driver.find_elements(By.TAG_NAME, "a")
            

        linkedin_href = ""
        for anchor_tag in anchor_tags:
            href = anchor_tag.get_attribute("href")
            if href and "linkedin" in href:
                linkedin_href = href
                break

        self.driver.get(linkedin_href)

        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[2]/div[1]/div[2]/div/h1')))
            company_name = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[2]/div[1]/div[2]/div/h1').text
            self.data["Company Name"] = company_name
            sleep(3)
        except Exception as e:
            pass

        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/section/div/header/h2")))
            home_about = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/section/div/header/h2").text
            sleep(1)
        except Exception as e:
            pass

        self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/section/div/div/div/div")))
        home = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/section/div/div/div/div/span[3]/span/a').click()
        Home_content = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/section/div/div").text
        self.data["About"] = Home_content
        sleep(1)

        self.wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "About")))
        about_c = self.driver.find_element(By.PARTIAL_LINK_TEXT,"About").click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/h2")))

        try:
            about_overview = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/h2").text
        except Exception as e:
            pass
        sleep(1)

        try:
            about_overview_content = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/p").text
            self.data["Overview"] = about_overview_content
        except Exception as e:
            pass
        sleep(1)

        try:
            about_contact = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[1]").text
            self.data["Contact"] = about_contact
        except Exception as e:
            pass
        sleep(1)

        try:
            about_website_link = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[1]/a").get_attribute("href")
           
            self.data["Website"] = about_website_link
        except Exception as e:
            pass
        sleep(1)

        try:
            about_phone = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[2]").text
        except Exception as e:
            pass
        sleep(1)

        try:
            about_phone_no = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[2]/a").get_attribute("href")
            self.data["Phone"] = about_phone_no
        except Exception as e:
            pass
        sleep(1)

        try:
            about_industry = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[3]").text
        except Exception as e:
            pass
        sleep(1)


        try:
            about_industry_content = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[3]").text
            self.data["Industry"] = about_industry_content
        except Exception as e:
            pass
        sleep(1)

        try:
            about_company = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[4]").text
        except Exception as e:
            pass
        sleep(1)

        try:
            about_company1 = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[4]").text
            self.data.setdefault("ComapanyDetails",[]).append(about_company1)
        except Exception as e:
            pass
        sleep(1)

        try:
            about_company2 = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[5]/a").text
            self.data.setdefault("ComapanyDetails",[]).append(about_company2)
        except Exception as e:
            pass
        sleep(1)

        try:
            about_headquaters = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[5]").text
        except Exception as e:
            pass
        sleep(1)

        try:
            about_headquaters_content = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[6]").text
            self.data["Headquarters"] = about_headquaters_content
        except Exception as e:
            pass
        sleep(1)

        try:
            about_founded = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[6]").text
        except Exception as e:
            pass
        sleep(1)

        try:
            about_founded_content = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[7]").text
            self.data["Founded"] = about_founded_content
        except Exception as e:
            pass
        sleep(1)

        try:
            about_specialties = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[7]").text
        except Exception as e:
            pass
        sleep(1)

        try:
            about_specialties_content = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[8]").text
            self.data["Specialties"] = about_specialties_content
        except Exception as e:
            pass
        sleep(2)

        try:
            self.wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "People")))
            post = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'People').click()
            sleep(2)
        except Exception as e:
            pass

        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]/div/input')))
            search = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]/div/input')
            search1 = "ceo"
            for i in search1:
                search.send_keys(i)
                sleep(0.5)
            search.send_keys(Keys.ENTER)
            sleep(2)
            self.driver.execute_script("window.scrollTo(0,window.scrollY*2)")
            sleep(1)
        except Exception as e:
            pass
        self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div')))
        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div')
        self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]')))
        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]')
        list = self.driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul")

        i = 1
        while True:
            try:
                try:
                    element = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[2]/div')
                    show = element.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[2]/div/button')
                    show.click()
                except Exception as e:
                    pass
                
                x_path = f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{i}]"
                self.driver.execute_script("window.scrollTo(0,window.scrollY*1.5)")
                card = self.driver.find_element(By.XPATH,x_path)
                div1 = card.find_element(By.TAG_NAME,"div")
                section = div1.find_element(By.TAG_NAME,"section")
                div2 = section.find_element(By.TAG_NAME,"div")
                name = ""
                try:
                    name = div2.find_element(By.XPATH,f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{i}]/div/section/div/div/div[2]/div[1]").text
                 
                except Exception as e:
                    pass
                position = ""
                try:
                    position = div2.find_element(By.XPATH,f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{i}]/div/section/div/div/div[2]/div[2]").text
                except Exception as e:
                    pass
                experties = "No Data Found"
                try:
                    experties = div2.find_element(By.TAG_NAME,"span").text
                except Exception as e:
                    pass
                d = {
                    "Name": name,
                    "Position": position,
                    "Experties":experties
                }
                if d not in self.people_info_list:
                    self.people_info_list.append({
                    "Name": name,
                    "Position": position,
                    "Experties":experties
                })
                i+=1
            except Exception as e:
                break
      

        try:
            self.driver.execute_script("window.scrollTo({ top: 50, behavior: 'smooth' });")
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]')))
            div = self.driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]")
            sleep(1)
            div2=div.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]")
            sleep(0.5)
            div3 = div2.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]")
            sleep(0.5)
            ul = div3.find_element(By.TAG_NAME,"ul")
            sleep(0.5)
            li = div.find_element(By.TAG_NAME,"li")
            sleep(0.5)
            button = li.find_element(By.TAG_NAME,"button")
            sleep(0.5)
            id = button.get_attribute("id")
            sleep(0.5)
            button1 = li.find_element(By.ID,id)
            sleep(0.5)
            button1.click()
            sleep(2)
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]/div/input')))
            search = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]/div/input')
            search3 = "hr"
            for x in search3:
                search.send_keys(x)
                sleep(0.5)
            search.send_keys(Keys.ENTER)
            sleep(2)
            self.driver.execute_script("window.scrollTo(0,window.scrollY*2)")
            sleep(1)
        except Exception as e:
            pass

        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div')
        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]')
        list = self.driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul")
        j = 1

        while True:
            try:
                try:
                    element = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[2]/div')
                    show = element.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[2]/div/button')
                    show.click()
                except Exception as e:
                    pass
                
                x_path = f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{j}]"
                self.driver.execute_script("window.scrollTo(0,window.scrollY*1.5)")
                card = self.driver.find_element(By.XPATH,x_path)
                div1 = card.find_element(By.TAG_NAME,"div")
                section = div1.find_element(By.TAG_NAME,"section")
                div2 = section.find_element(By.TAG_NAME,"div")
                name = ""
                try:
                    name = div2.find_element(By.XPATH,f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{j}]/div/section/div/div/div[2]/div[1]").text
                 
                except Exception as e:
                    pass
                position = ""
                try:
                    position = div2.find_element(By.XPATH,f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{j}]/div/section/div/div/div[2]/div[2]").text
                 
                except Exception as e:
                    pass
                experties = "No Data Found"
                try:
                    experties = div2.find_element(By.TAG_NAME,"span").text
                   
                    
                except Exception as e:
                    pass
                d = {
                    "Name": name,
                    "Position": position,
                    "Experties":experties
                }
                if d not in self.people_info_list:
                    self.people_info_list.append({
                    "Name": name,
                    "Position": position,
                    "Experties":experties
                })
                j+=1
            except Exception as e:
                break

        try:
            self.driver.execute_script("window.scrollTo({ top: 50, behavior: 'smooth' });")
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]')))
            div = self.driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]")
            sleep(1)
            div2=div.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]")
            sleep(0.5)
            div3 = div2.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]")
            sleep(0.5)
            ul = div3.find_element(By.TAG_NAME,"ul")
            sleep(0.5)
            li = div.find_element(By.TAG_NAME,"li")
            sleep(0.5)
            button = li.find_element(By.TAG_NAME,"button")
            sleep(0.5)
            id = button.get_attribute("id")
            sleep(0.5)
            button1 = li.find_element(By.ID,id)
            sleep(0.5)
            button1.click()
            sleep(2)
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]/div/input')))
            search = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div/div/section/div[1]/div[1]/div[2]/div/input')
            search2 = "sales"
            for x in search2:
                search.send_keys(x)
                sleep(0.5)
            search.send_keys(Keys.ENTER)
            sleep(2)
            self.driver.execute_script("window.scrollTo(0,window.scrollY*2)")
            sleep(1)
        except Exception as e:
            pass

        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div')
        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]')
        list = self.driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul")
        k = 1

        while True:
            try:
                try:
                    element = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[2]/div')
                    show = element.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[2]/div/button')
                    show.click()
                except Exception as e:
                    pass
                
                x_path = f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{k}]"
                self.driver.execute_script("window.scrollTo(0,window.scrollY*1.5)")
                card = self.driver.find_element(By.XPATH,x_path)
                div1 = card.find_element(By.TAG_NAME,"div")
                section = div1.find_element(By.TAG_NAME,"section")
                div2 = section.find_element(By.TAG_NAME,"div")
                name = ""
                try:
                    name = div2.find_element(By.XPATH,f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{k}]/div/section/div/div/div[2]/div[1]").text
                except Exception as e:
                    pass
                position = ""
                try:
                    position = div2.find_element(By.XPATH,f"/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{k}]/div/section/div/div/div[2]/div[2]").text
                except Exception as e:
                    pass
                experties = "No Data Found"
                try:
                    experties = div2.find_element(By.TAG_NAME,"span").text
                   
                except Exception as e:
                    pass
                d = {
                    "Name": name,
                    "Position": position,
                    "Experties":experties
                }
                if d not in self.people_info_list:
                    self.people_info_list.append({
                    "Name": name,
                    "Position": position,
                    "Experties":experties
                })
                k+=1
            except Exception as e:
                break

        sleep(1)
        self.data.setdefault("People",[]).append(self.people_info_list)
        
    def getCSV(self)->pd.DataFrame:
        df = pd.DataFrame([self.data])
        df.to_csv("Company_data.csv", index=False)
       
    def QuitDriver(self):
        self.driver.quit()