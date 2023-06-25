import os
import time
import shutil
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class SpxDonwloader():
    __headless = True
    __tempFolder = os.path.join(os.getcwd(), 'TEMP')

    def __init__(self, headless=True):
        """ Para primeiro acesso, definir headless=True para conseguir realizar login e salvar as credenciais de execução
            :param headless: Boolean (Opcional) - Define se o navegaor será exibido durante a execução do código
        """
        self.__headless = headless
    
    def __move_recent_file(self, folder, filepath, new_name):
        """ Função que localiza o ultimo arquivo baixado, renomea e move o arquivo para o local informado
            :param folder: String - Pasta de origem do arquivos baixados, pasta a ser verificada a procura de arquivos recentes
            :param filepath: String (Opcional)- Caminho para qual o arquivo será movido após ser baixado, se não informado, então salvo no diretorio de execução
            :param new_name: String (Opcional)- Nome que será utilizado ao renomear o arquivo, se não informado, então mantem
        """
        files_list = glob.glob(os.path.join(folder, '*'))
        if not files_list:
            print("Nenhum arquivo encontrado na folder.")
            return

        latest_file = max(files_list, key=os.path.getctime)
        file_extension = os.path.splitext(latest_file)[1]

        if new_name is None:
            new_path = os.path.join(filepath, os.path.basename(latest_file))
        else:
            new_path = os.path.join(filepath, new_name + file_extension)

        try:
            shutil.move(latest_file, new_path)
            print("Arquivo movido com sucesso.")
        except Exception as e:
            print("Ocorreu um erro ao mover o arquivo:", str(e))
            
    def __set_config(self, headless=True):
        """ Helper function that creates a new Selenium browser """
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument('headless')
    
        self.tempFolder = self.__tempFolder
        if not os.path.exists(self.tempFolder):
            os.makedirs(self.tempFolder)

        self.userPerfil = os.path.join(os.getcwd(), 'perfil')
        if not os.path.exists(self.userPerfil):
            os.makedirs(self.userPerfil)
        
        self.prefs = {}
        self.prefs["profile.default_content_settings.popups"]=0
        self.prefs["download.default_directory"] = self.tempFolder
        self.options.add_argument("--disable-extensions")
        self.options.add_experimental_option("prefs", self.prefs)

        self.options.add_argument(f"user-data-dir={self.userPerfil}")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        #input()
        return self.browser

    def export_outbound(self, path_download=None, filename=None):
        """ Função que exporta os dados de produtividade a partir do Sistema SPX
            :param path_download: String (Opcional) - local de destino do arquivo baixado, se não informado, então realiza o download para o diretorio atual de execução
            :param filename: String (Opcional)- o nome que será utilizado ao salvar o arquivo, se não informado, então mantem o nome atual
        """

        if not os.path.exists(path_download):
            os.makedirs(path_download)

        driver = self.__set_config(self.__headless)
        driver.get('https://spx.shopee.com.br/#/dashboard/toProductivity?page_type=Outbound')
        time.sleep(3)
        driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/span/span/span/button').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/span/div/div/div[1]').click()
        time.sleep(15)
        driver.find_element(By.XPATH,'/html/body/span/div/div[1]/div/span/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/button').click()
        time.sleep(5)
        driver.quit()

        if path_download is None:
            path_download = os.getcwd()

        self.__move_recent_file(self.__tempFolder, path_download, filename)
        shutil.rmtree(self.__tempFolder)