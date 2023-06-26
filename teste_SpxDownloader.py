import os
from SpxSystem import SpxDonwloader
import sendMessage

def send_log_seatalk():
    with open((os.path.join(os.getcwd(), 'exec.log')), "r") as file_log:
        log = file_log.read()
    sendMessage.send_message_custom(f"Teste de log em Seatalk: \n {log}")

csv_folder = os.path.join(os.getcwd(), 'CSV_FILES')

spx = SpxDonwloader(headless=True)

# Chama a função que realiza o download do arquivo
# path_download é a pasta de destino do arquivo baixado
# filename é o nome que o arquivo deverá ser nomeado no final
# Ambos parâmetros são opcionais, caso não informados, o arquivo será saldo no diretorio de execução
# com o nome original
#spx.export_outbound() # Sem parametros
#send_log_seatalk()

#spx.export_outbound(path_download=csv_folder) # apenas com o diretorio de destino
#send_log_seatalk()

#spx.export_outbound(path_download="D:\\Shopee\\Seatalk Bot\\Seatalk Bot", filename="cerberus.csv") # apenas com o diretorio de destino
#send_log_seatalk()

#spx.export_outbound(path_download=csv_folder, filename="OUTBOUND_RESOURCE_DATA") # com local de destino e nome de salvamento
#send_log_seatalk()

spx.download_produty(path_download="D:\\Shopee\\Seatalk Bot\\Seatalk Bot", filename="meu_pdf")