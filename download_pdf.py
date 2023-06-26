import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def __set_config( headless=True):
    """ Helper function that creates a new Selenium browser """
    __tempFolder = os.getcwd() #os.path.join(os.getcwd(), 'TEMP')
    __userPerfil = os.path.join(os.getcwd(), 'perfil')
    options = webdriver.ChromeOptions()
        
    prefs = {}
    prefs["profile.default_content_settings.popups"]=0
    prefs["download.default_directory"] = __tempFolder
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", prefs)

    if headless:             
        options.add_argument('headless')
        options.add_argument(f"user-data-dir={__userPerfil}")
        
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            
    return browser

if __name__ == '__main__':
    url = "https://docs.google.com/spreadsheets/d/1age7c_P-4dKYKq7hNBLp9XMmP5FmjBLNM_IICiiblgE/export?exportFormat=pdf&format=pdf&size=16.215x6.715&scale=2&top_margin=0&bottom_margin=0&left_margin=0&right_margin=0&sheetnames=false&printtitle=false&pagenum=UNDEFINEDhorizontal_alignment=LEFT&gridlines=false&fmcmd=12&fzr=FALSE&gid=280776734&r1=4&r2=34&c1=1&c2=19"
    driver = __set_config(False)
    driver.get(url)
    time.sleep(30)
    driver.quit()


