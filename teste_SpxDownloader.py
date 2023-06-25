import os
from SpxSystem import SpxDonwloader

csv_folder = os.path.join(os.getcwd(), 'CSV_FILES')

spx = SpxDonwloader()

# Chama a função que realiza o download do arquivo
# path_download é a pasta de destino do arquivo baixado
# filename é o nome que o arquivo deverá ser nomeado no final
# Ambos parâmetros são opcionais, caso não informados, o arquivo será saldo no diretorio de execução
# com o nome original
spx.export_outbound() # Sem parametros
spx.export_outbound(path_download=csv_folder) # apenas com o diretorio de destino
spx.export_outbound(path_download=csv_folder, filename="outbound_yyyyMMddhh") # com local de destino e nome de salvamento