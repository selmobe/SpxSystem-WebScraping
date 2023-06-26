import os
import time
import shutil
import glob
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class SpxDonwloader():
    logging.basicConfig(level=logging.INFO, filename="exec.log", format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")
    __headless = True
    __tempFolder = os.path.join(os.getcwd(), 'TEMP')
    __userPerfil = os.path.join(os.getcwd(), 'perfil')

    def __init__(self, headless=True):
        """ Para primeiro acesso, definir headless=True para conseguir realizar login e salvar as credenciais de execução
            :param headless: Boolean (Opcional) - Define se o navegaor será exibido durante a execução do código
        """
        with open((os.path.join(os.getcwd(), 'exec.log')), "r+") as file_log:
            file_log.truncate()
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
            return new_path
        except Exception as e:
            print("Ocorreu um erro ao mover o arquivo:", str(e))
            
    def __set_config(self, headless=True):
        """ Helper function that creates a new Selenium browser """
        self.options = webdriver.ChromeOptions()
    
        self.tempFolder = self.__tempFolder
        if not os.path.exists(self.tempFolder):
            os.makedirs(self.tempFolder)
        
        self.prefs = {}
        self.prefs["profile.default_content_settings.popups"]=0
        self.prefs["download.default_directory"] = self.tempFolder
        self.options.add_argument("--disable-extensions")
        self.options.add_experimental_option("prefs", self.prefs)       

        if not os.path.exists(self.__userPerfil):
            logging.warning(f"Diretorio com cache de credenciais não existente, criando.")
            os.makedirs(self.__userPerfil)
            self.options.add_argument(f"user-data-dir={self.__userPerfil}")
            self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
            self.__headless = False
            self.browser.get("https://spx.shopee.com.br/#/dashboard/toProductivity?page_type=Outbound")
            WebDriverWait(self.browser, 50).until(EC.url_to_be("https://spx.shopee.com.br/#/index"))
            time.sleep(5)
            self.browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/p").click()
            return self.browser
            
        if headless:             
            self.options.add_argument('headless')
            self.options.add_argument(f"user-data-dir={self.__userPerfil}")
        
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
            
        return self.browser

    def export_outbound(self, path_download=None, filename=None):
        """ Função que exporta os dados de produtividade a partir do Sistema SPX
            :param path_download: String (Opcional) - local de destino do arquivo baixado, se não informado, então realiza o download para o diretorio atual de execução
            :param filename: String (Opcional)- o nome que será utilizado ao salvar o arquivo, se não informado, então mantem o nome atual
        """
        logging.info("Iniciando acesso ao sistema e extraindo dados")
        if not os.path.exists(path_download):
            logging.warning(f"Diretorio de destino não existe: {path_download}, sistema criando diretório")
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

        result = self.__move_recent_file(self.__tempFolder, path_download, filename)
        shutil.rmtree(self.__tempFolder)
        logging.info(f"Relatorio exportado com successo para a pasta {result}")
    
    def download_produty(self, path_download=None, filename=None):
        """ Função que exporta os dados de produtividade a partir do Sistema SPX
            :param path_download: String (Opcional) - local de destino do arquivo baixado, se não informado, então realiza o download para o diretorio atual de execução
            :param filename: String (Opcional)- o nome que será utilizado ao salvar o arquivo, se não informado, então mantem o nome atual
        """
        logging.info("Iniciando acesso ao sistema e extraindo dados")
        if not os.path.exists(path_download):
            logging.warning(f"Diretorio de destino não existe: {path_download}, sistema criando diretório")
            os.makedirs(path_download)

        driver = self.__set_config(self.__headless)
        driver.get("https://docs.google.com/spreadsheets/d/1age7c_P-4dKYKq7hNBLp9XMmP5FmjBLNM_IICiiblgE/export?exportFormat=pdf&format=pdf&size=16.215x6.715&scale=2&top_margin=0&bottom_margin=0&left_margin=0&right_margin=0&sheetnames=false&printtitle=false&pagenum=UNDEFINEDhorizontal_alignment=LEFT&gridlines=false&fmcmd=12&fzr=FALSE&gid=280776734&r1=4&r2=34&c1=1&c2=19")
        time.sleep(3)
        driver.quit()

        if path_download is None:
            path_download = os.getcwd()

        result = self.__move_recent_file(self.__tempFolder, path_download, filename)
        shutil.rmtree(self.__tempFolder)
        logging.info(f"Relatorio exportado com successo para a pasta {result}")

if __name__ == '__main__':

    csv_folder = os.path.join(os.getcwd(), 'CSV_FILES')
    spx = SpxDonwloader()
    new_name = "123456"

    # Chama a função que realiza o download do arquivo
    # path_download é a pasta de destino do arquivo baixado
    # filename é o nome que o arquivo deverá ser nomeado no final
    # Ambos parâmetros são opcionais, caso não informados, o arquivo será saldo no diretorio de execução
    # com o nome original
    spx.export_outbound(path_download=csv_folder, filename=new_name)