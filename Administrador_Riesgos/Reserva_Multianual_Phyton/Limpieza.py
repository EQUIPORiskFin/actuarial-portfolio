import os
ruta  =os.path.join("C:/Users/agarciadeleon/R_Studio/Scripts/Carp1/P1")
os.chdir(ruta)
from openpyxl import load_workbook
import csv

wb = load_workbook("Siniestros FONACOT 07052026.xlsx", read_only=True)
k = wb.sheetnames

for k1 in k:
 ws = wb[k1]#wb.active  # o especificar nombre de hoja
 nombre = "siniestros" + k1 + ".csv"
 with open(nombre, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in ws.iter_rows(values_only=True):
        writer.writerow(row)
###################################################################3
###################################################################
import pandas as pd
siniestrosParte_1 = pd.read_csv("C:/Users/agarciadeleon/Phyton/siniestrosParte 1.csv")
siniestrosParte_2 = pd.read_csv("C:/Users/agarciadeleon/Phyton/siniestrosParte 2.csv")
siniestrosF = pd.concat([siniestrosParte_1, siniestrosParte_2], axis=0)
siniestrosF.columns
#####################################################################################
####################################################################################
#Importación actualizada del vigor
import pandas as pd
#Vigor = pd.read_feather('Vigor_definitivo_DEF.feather')
Vigor = pd.read_feather('VigorDEFI_Fin.feather')
Vigor['POLIZA'] = Vigor['poliza']
Vigor['FEMIS'] = Vigor['femis']
Vigor['CERTIFICAD'] = Vigor['certificad']
Vigor['SAOTRAS'] = Vigor['saotras']
Vigor['SABAS'] = Vigor['sabas']
Vigor['SAITP'] = Vigor['saitp']
Vigor['PETOTAL'] = Vigor['petotal']
Vigor['PEBAS'] = Vigor['petotal']
Vigor['PEIPT'] = Vigor['peipt']
Vigor['PEOTRAS'] = Vigor['peotras']
import pandas as pd

# Fecha FEMIS
Vigor["FEMIS"] = pd.to_datetime(Vigor["femis"])
Vigor["Anio"] = Vigor["FEMIS"].dt.year

# Fecha inicio vigencia
Vigor["INIVIG"] = pd.to_datetime(Vigor["inivig"])
Vigor["Anio_INI"] = Vigor["INIVIG"].dt.year

# Fecha fin plazo
Vigor["FIN_PLAZO"] = pd.to_datetime(Vigor["fin_plazo"])
Vigor["Anio_FIN"] = Vigor["FIN_PLAZO"].dt.year

# Variables auxiliares
ini = Vigor["INIVIG"]
fin = Vigor["FIN_PLAZO"]

# Fecha crédito
Vigor["INIVIG1"] = pd.to_datetime(Vigor["fecha_credito"])
Vigor["Anio_INI1"] = Vigor["INIVIG1"].dt.year

# Fin de vigencia
Vigor["FIN_PLAZO1"] = pd.to_datetime(Vigor["fin_de_vig"])
Vigor["Anio_FIN1"] = Vigor["FIN_PLAZO1"].dt.year
Vigor["INIVIG2"] = pd.to_datetime(Vigor["fecha_ini_r"])
Vigor["Anio_INI2"] = Vigor["INIVIG2"].dt.year
Vigor["FIN_PLAZO2"] = pd.to_datetime(Vigor["Fecha_FIN_R"])
Vigor["Anio_FIN2"] = Vigor["FIN_PLAZO1"].dt.year

############################################################################3
import pandas as pd
#resultado = texto.split("-", 1)[1]
# Crear el equivalente a cbind(...)
def Filtrado_Siniestros(siniestrosF1,j):
 B = siniestrosF1.copy()

 B['FEC_VIG_DESDE'] = pd.to_datetime(B['FEC_VIG_DESDE'])
 B['FEC_REGISTRO'] = pd.to_datetime(B['FEC_REGISTRO'])
 B['FEC_VIG_HASTA'] = pd.to_datetime(B['FEC_VIG_HASTA'])

 B['Periodo_origen'] = pd.to_datetime(B['FEC_VIG_DESDE'].dt.strftime('%m-%Y'),format='%m-%Y')
 B['Periodo_desarrollo'] = pd.to_datetime(B['FEC_REGISTRO'].dt.strftime('%m-%Y'),format='%m-%Y')

 B['Anio_INI'] = B['FEC_VIG_DESDE'].dt.year
 B['Anio_REGIS'] = B['FEC_REGISTRO'].dt.year
 B['Anio_FIN'] = B['FEC_VIG_HASTA'].dt.year
 # Variables auxiliares
 ini = B['FEC_VIG_DESDE']
 fin = B['FEC_VIG_HASTA']
 
 B['meses'] = (
    (fin.dt.year - ini.dt.year) * 12 +
    (fin.dt.month - ini.dt.month) -
    (fin.dt.day < ini.dt.day)
 )
 
 B['Clase'] = np.where(
    B['meses'] >= 30, 30,
    np.where(
        (B['meses'] >= 24) & (B['meses'] < 30), 24,
        np.where(
            (B['meses'] >= 18) & (B['meses'] < 24), 18,
            np.where(
                (B['meses'] >= 12) & (B['meses'] < 18), 12,
                6
            )
        )
    )
 )
 C = B[B['COBERTURA'] == "DESEMPLEO INVOLUNTARIO"]
 C = B[B['Clase']==j]
 return C

siniestrosF = Filtrado_Siniestros(siniestrosF1,30)
siniestrosF1
siniestrosF
