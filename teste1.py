#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 21:31:10 2023

@author: jonatha
"""
import numpy as np
from datetime import datetime,timedelta
from netCDF4 import Dataset
# In[mudando a rodada para o caminho de outro script]
# Colocar o diretório do wrf_plot.py no os.chdir
import os
os.chdir('/home/jonatha/Downloads/demanda_azul/AZUL')
from teste import Plot,Variaveis

# In[abrindo arquivo por data]

# Teste para dia anterior 
# hoje = datetime.now() #dia atual
hoje = datetime(2022 , 12 , 29)
Ano_hoje = str(hoje.year)
Mes_hoje = str(hoje.strftime("%m"))
Dia_hoje = str(hoje.strftime("%d"))

# Caminho dos arquivos de saída
PATH = '/home/jonatha/Downloads/demanda_azul/AZUL'
grade = 'G01'
arquivo = f'{PATH}/wrfout-{grade}-{Ano_hoje}-{Mes_hoje}-{Dia_hoje}'

ncfile = Dataset(arquivo)

# In[ajustando o eixo do tempo]
tempo = np.array(ncfile['Times'])

def arruma_tempo(tempo):
    
    data_titulo = [str(name) for i,name in enumerate(tempo)]
    
    def messTonumber(lista):
        
        lista_nova = [x.replace("b", "") for x in lista]
        lista_nova = [x.replace("'", "") for x in lista_nova]
        lista_nova = [x.replace(" ", "") for x in lista_nova]
        lista_nova = [x.replace("[", "") for x in lista_nova]
        lista_nova = [x.replace("]", "") for x in lista_nova]
        lista_nova = [x.replace("\n", "") for x in lista_nova]
        lista_nova = [x.replace("_", " ") for x in lista_nova]
        
        return lista_nova
    
    data_nova = messTonumber(data_titulo)
    
    return data_nova
  
tempo = arruma_tempo(tempo)

# str to datetime
tempo = [datetime.strptime(x, '%Y-%m-%d	 %H:%M:%S') for x in tempo]
# tempo1 = pd.to_datetime(tempo, infer_datetime_format=True)

# hora local
tempo_LOCAL = [x + timedelta(hours=-3) for x in tempo]

# In[testando variáveis]
idx_time = list(range(0,len(tempo_LOCAL)))

hgt500   = [Variaveis().interp_hgt(ncfile,500,x) for x in idx_time]
temp500  = [Variaveis().interp_tempC(ncfile, 500, x) for x in idx_time]
pw       = [Variaveis().agua_precip(ncfile,x) for x in idx_time]

omega500 = [Variaveis().interp_omega(ncfile, 500, x) for x in idx_time]
omega550 = [Variaveis().interp_omega(ncfile, 550, x) for x in idx_time]
omega600 = [Variaveis().interp_omega(ncfile, 600, x) for x in idx_time]
omega650 = [Variaveis().interp_omega(ncfile, 650, x) for x in idx_time]
omega700 = [Variaveis().interp_omega(ncfile, 700, x) for x in idx_time]

u700     = [Variaveis().interp_u(ncfile, 700, x) for x in idx_time]
v700     = [Variaveis().interp_v(ncfile, 700, x) for x in idx_time]
omega_media = [(a+b+c+d+e)/5 for a,b,c,d,e in zip(omega500,omega550,omega600,omega650,omega700)]

del omega500,omega700,omega550,omega600,omega650
# In[plotando as figuras]
[Plot().mix700(ncfile,pw,temp500,omega_media,u700,v700,hgt500,tempo_LOCAL[x],x) for x in idx_time]

