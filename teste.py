#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 21:18:10 2023

@author: jonatha
"""
# In[bibliotecas]
import os
import numpy as np
import matplotlib.pyplot as plt
# Arrumar esse bloco em uma coisa só
import cartopy.crs as crs
import cartopy.feature as ft
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import wrf 

class Variaveis():
    
    def __init__(self):
        return None
    
    def interp_hgt(self, ncfile,lvl,idx_time):
        hgt = wrf.g_geoht.get_height(ncfile, timeidx=idx_time,meta=False)
        levels = wrf.getvar(ncfile,'pressure')
        
        hgt_interp = wrf.interplevel(hgt,levels,lvl)
        
        return hgt_interp

    def interp_tempC(self,ncfile,lvl,idx_time):
        
        temp = wrf.getvar(ncfile, 'tc', timeidx=idx_time)
        levels = wrf.getvar(ncfile,'pressure')
        
        temp_interp = wrf.interplevel(temp,levels,lvl)
        
        return temp_interp
        
    def interp_omega(self,ncfile,lvl,idx_time):
        
        omega = wrf.getvar(ncfile, 'omega', timeidx=idx_time)
        levels = wrf.getvar(ncfile,'pressure')
        
        omega_interp = wrf.interplevel(omega,levels,lvl)
        
        return omega_interp

    def interp_u(self,ncfile,lvl,idx_time):
        
        uv = wrf.getvar(ncfile, 'uvmet', timeidx=idx_time,units='kt')
        levels = wrf.getvar(ncfile,'pressure')
        
        u_interp = wrf.interplevel(uv[0,:,:,:],levels,lvl)
        
        return u_interp

    def interp_v(self,ncfile,lvl,idx_time):
        
        uv = wrf.getvar(ncfile, 'uvmet', timeidx=idx_time,units='kt')
        levels = wrf.getvar(ncfile,'pressure')
        
        v_interp = wrf.interplevel(uv[1,:,:,:],levels,lvl)
        
        return v_interp


    def agua_precip(self,ncfile,idx_time):
        
        pw = wrf.getvar(ncfile, 'pw', timeidx=idx_time)

        return pw    


# In[plot]
class Plot():
    
    def __init__(self):
        return None

# O base_of_the_fig NÃO ESTÁ FUNCIONANDO    
    def base(self,ax,dset,proj):
        
        # ax.set_extent([-43.4,-42.9,-23.1,22.65],proj)
        
        lat = dset['XLAT'][0,:,:]
        lon = dset['XLONG'][0,:,:]
        
        ax.set_extent([float(np.min(lon)), float(np.max(lon)),float(np.min(lat)), 
                        float(np.max(lat))], proj)
        
        ax.add_feature(ft.COASTLINE)
        
        states_provinces = ft.NaturalEarthFeature(category='cultural',
                                                  name='admin_1_states_provinces_lines',
                                                  scale='50m',
                                                  facecolor='none')
        
        ax.add_feature(states_provinces, edgecolor='black')


# ESTÁ FUNCIONANDO
    def axis_fig(self,ax,ncfile,lons,lats):

        x_lons = np.arange(np.min(wrf.to_np(lons)),np.max(wrf.to_np(lons)),5)
        y_lats = np.arange(np.min(wrf.to_np(lats)),np.max(wrf.to_np(lats)),2)
        
        ax.set_xticks(x_lons, minor=False, crs=crs.PlateCarree())
        ax.set_xticklabels(ax.get_xticks(), fontsize=16)
        ax.set_yticks(y_lats, minor=False, crs=crs.PlateCarree())
        ax.set_yticklabels(ax.get_yticks(), fontsize=16)
        
        lon_formatter = LongitudeFormatter(zero_direction_label=True, 
                                           number_format='.1f')
        lat_formatter = LatitudeFormatter(number_format='.1f')
        
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)


# ALTERAR O DIRETÓRIO DO save_fig QUANDO PASSAR ESSE CÓDIGO PARA A NUMA 14    
    def save_figure(self,fig_name):
        try:
            
            plt.savefig('figures/{}.jpg'.format(fig_name),
                bbox_inches='tight', dpi=100, facecolor='w', edgecolor='w')
        
        except:
            os.mkdir('figures/')
            
            plt.savefig('figures/{}.jpg'.format(fig_name),
                bbox_inches='tight', dpi=100, facecolor='w', edgecolor='w')
            
        plt.close()
        
# In[Variáveis em 700hPa]        
           
    def mix700(self,ncfile,pw,temp700,omega_media,u700,v700,hgt500,tempo,index_time):
        
        fig = plt.figure(figsize=(12,10))
        proj = crs.PlateCarree()
        ax = plt.axes(projection=proj)
            
        lats, lons = np.array(ncfile['XLAT'][0,:,:]), np.array(ncfile['XLONG'][0,:,:])
                    
################ Água precipitável (mm)
        
        colors = colors = ('#61be58','#5fbd56','#4ab547','#33ac35','#1da425','#1da425','#078719','#07761c','#06651f','#055023','#ffdc00','#ffc800','#ffb500','#ffa000','#ff8100','#ff8100','#ff7d00','#ff5a00','#ff3700','#d70000','#f15cb8','#fd84e3','#feaaf8','#ffcfe9','#ffe9ff')
        
        levels = np.arange(20,71,2)
        plt.contourf(np.array(lons),np.array(lats),np.array(pw[index_time]),
                     len(colors)-1,
                     colors=colors,
                     levels=levels,
                     transform=proj,
                     extend='max')

        # Adicionando uma barra de cores 
        barra = plt.colorbar(ax=ax, shrink=.98,ticks=levels)        
        barra.set_label('Água precipitável (mm)', rotation=270, size=15, labelpad=25)
        barra.ax.tick_params(labelsize=15)

################ Temperatura (ºC) - 500 hPa
       
        temp_lev0 = np.arange(np.min(temp700[index_time]),-8,2)        

        lines = plt.contour(wrf.to_np(lons),
                            wrf.to_np(lats),
                            wrf.to_np(temp700[index_time]),
                            levels=temp_lev0,
                            colors='blue',
                            linestyles='dashed')
        
        plt.clabel(lines,fontsize=10)

        temp_lev1 = np.arange(-8,np.max(temp700[index_time]),2)        

        lines = plt.contour(wrf.to_np(lons),
                            wrf.to_np(lats),
                            wrf.to_np(temp700[index_time]),
                            levels=temp_lev1,
                            colors='red',
                            linestyles='dashed')
        
        plt.clabel(lines,fontsize=10)

################ Ômega        
        
        omega_neg = np.arange(np.min(omega_media),0,1)        
        
        suave = wrf.smooth2d(omega_media[index_time],passes=20)

        lines1 = plt.contour(wrf.to_np(lons),
                              wrf.to_np(lats),
                              wrf.to_np(suave),
                              levels=omega_neg,
                              colors='blue',
                              linestyles='solid')
        
        
        
        plt.clabel(lines1,fontsize=10)
                
################ Vento
        
        plt.barbs(wrf.to_np(lons)[::20,::20],
                  wrf.to_np(lats)[::20,::20],
                  u700[index_time][::20,::20],
                  v700[index_time][::20,::20])
        
################ Altura geopot
        
        lines2 = plt.contour(wrf.to_np(lons),
                              wrf.to_np(lats),
                              wrf.to_np(hgt500[index_time]),
                              colors='black',
                              linestyles='solid')
        
        plt.clabel(lines2,fontsize=10)

        fig.canvas.draw()
        fig.tight_layout()

        self.axis_fig(ax, ncfile, lons, lats)
        
        titulo = f'Água precipitável (mm, sombreado)\nTemperatura em 500hPa (ºC, vermelho)\nAltura Geopotencial 500hPa (dam, preto) \nÔmega 700-500hPa (Pa.s⁻¹, azul) e vento em 700hPa (kt, Barbela)      {tempo}'

        plt.title(titulo, fontsize=15, loc='left')
            
        self.base(ax,ncfile,proj)
        self.save_figure(f'atmosfera_mix700_{tempo}')
        plt.close()
