#Importando bibliotecas
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

#URL da página da receita com status da emissão NF
url = 'http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx?versao=0.00&tipoConteudo=P2c98tUpxrI='

#Pegando o HTML da página
pag = requests.get(url = url)
soup = bs(pag.content,'html.parser')

#Encontrando todos as tags TR da classe que contem as tabelas
list_par = soup.find_all('tr', {'class': 'linhaParCentralizada'})
list_impar = soup.find_all('tr', {'class': 'linhaImparCentralizada'})
receita_nf = {}
for impar in list_impar + list_par:
  dados_uf = impar.find_all('td')
  col_1 = dados_uf[0].get_text()
  col_2 = dados_uf[1].find('img')['src']
  col_3 = dados_uf[2].find('img')['src']
  if col_1 == 'SVC-RS':
    col_4 = dados_uf[3].get_text()
  else:
    col_4 = dados_uf[3].find('img')['src']
  col_5 = dados_uf[4].find('img')['src']
  col_6 = dados_uf[5].find('img')['src']
  col_7 = dados_uf[6].get_text()
  col_8 = dados_uf[7].get_text()
  col_9 = dados_uf[8].find('img')['src']
  receita_nf['UF'] = col_1
  receita_nf[col_1] = {'Autorização4': col_2,
                       'Retorno Autorização4': col_3,
                       'Inutilização4': col_4,
                       'Consulta Protocolo4': col_5,
                       'Status Serviço4': col_6,
                       'Tempo Médio': col_7,
                       'Consulta Cadastro4': col_8,
                       'Recepção Evento4': col_9}

df = pd.DataFrame(receita_nf).drop('UF', axis=1).T.reset_index()
df['Ultima verificacao'] = soup.find('span', {'class': 'fonte10'}).get_text()
df