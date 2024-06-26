import re
import pandas as pd
import os
import time

estados = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapa', 'AM': 'Amazonas', 'BA': 'Bahia',
    'CE': 'Ceara', 'DF': 'Distrito Federal', 'ES': 'Espirito Santo', 'GO': 'Goias',
    'MA': 'Maranhao', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
    'PA': 'Para', 'PB': 'Paraiba', 'PR': 'Parana', 'PE': 'Pernambuco', 'PI': 'Piaui',
    'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul',
    'RO': 'Rondonia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'Sao Paulo',
    'SE': 'Sergipe', 'TO': 'Tocantins'
}


def pegar_valor(texto):
    with open(texto, 'r', encoding='utf-8') as arquivo:
        file = arquivo.readlines()

    for linha in file:
        for i in range(len(file)):
            file[i] = file[i].lower()
        if "valor" in linha:
            match = re.search(r'\d{1,3}(\.\d{3})*,\d{2}', linha)
            return match.group()

def pegar_data(texto):
    with open(texto, 'r', encoding='utf-8') as arquivo:
        file = arquivo.readlines()

        for linha in file:
            for i in range(len(file)):
                file[i] = file[i].lower()
                if "data" in linha:
                    pattern = r'\b\d{2}/\d{2}/\d{4}\b'
                    match = re.search(pattern, linha)

                    if match:
                        return match.group()
                    return None

def pegar_estado(texto, estados):
    with open(texto, 'r', encoding='utf-8') as arquivo:
        file = [linha.lower() for linha in arquivo.readlines()]

    for linha in file:
        if "estado" in linha or "convenio" in linha:
            # Verifica padrões específicos um de cada vez
            if "gov-" in linha or "gov " in linha:
                match = re.search(r'gov-?\s*([a-z]{2})', linha, re.IGNORECASE)
                if match:
                    estado_capturado = match.group(1).strip().upper()
                    if estado_capturado in estados:
                        return estado_capturado
            
            elif "estado do" in linha or "estado de" in linha or "estado" in linha:
                match = re.search(r'estado (do|de)?\s*([a-z\s]+)', linha, re.IGNORECASE)
                if match:
                    estado_capturado = match.group(2).strip().upper()
                    for abbr, nome in estados.items():
                        if estado_capturado == nome.upper():
                            return abbr

    return None


# Execução do script
arquivos_txt = [f for f in os.listdir('.') if f.endswith('.txt')]

resultados = []
try:
    for arquivo in arquivos_txt:
        estado = pegar_estado(arquivo, estados)
        valor = pegar_valor(arquivo)
        data = pegar_data(arquivo)
        resultados.append(f"Arquivo: {arquivo}, Estado: {estado},  Data: {data},  Valor: {valor}")
    for resultado in resultados:
        print(resultado)
        
except:
    print(f"Deu ruim no: {arquivo}  ")
    pass
