import pandas as pd
#####Construir Base para triángulo
def Triangulo(siniestrosF):
 B = siniestrosF.copy()

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
 
# B['Clase'] = np.where(
 #   B['meses'] >= 30, 30,
  #  np.where(
   #     (B['meses'] >= 24) & (B['meses'] < 30), 24,
    #    np.where(
     #       (B['meses'] >= 18) & (B['meses'] < 24), 18,
      #      np.where(
       #         (B['meses'] >= 12) & (B['meses'] < 18), 12,
        #        6
         #   )
        #)
    #)
 #)
 C = B[B['COBERTURA'] == "DESEMPLEO INVOLUNTARIO"]
 
 Triangulo = (
    C
    .groupby(['Periodo_origen', 'Periodo_desarrollo','COBERTURA'], as_index=False)
    .agg(
        Suma=('IMPORTE_PAGADO', 'sum'),
        Numero=('NRO_STRO', 'nunique'),
        NumT = ('NRO_STRO', 'size')
    )
    .drop_duplicates()
 )
 return Triangulo
##################################################
####################################################
########################################################
#########Prima originada Mensual
import pandas as pd
def Primas(Vigor):
 B1 = Vigor.copy()
 B1['INIVIG1'] = pd.to_datetime(B1['fecha_credito'])
 B1['FEMIS'] = pd.to_datetime(B1['FEMIS'])
 B1['FIN_PLAZO1'] = pd.to_datetime(B1['fin_de_vig'])

 B1['Periodo_Origen'] = pd.to_datetime(B1['INIVIG1'].dt.strftime('%m-%Y'),format='%m-%Y')


 B1['Anio_origen'] = B1['Periodo_Origen'].dt.year

 # Variables auxiliares
 ini = B1['INIVIG1']
 fin = B1['FIN_PLAZO1']

 B1['meses'] = (
    (fin.dt.year - ini.dt.year) * 12 +
    (fin.dt.month - ini.dt.month) -
    (fin.dt.day < ini.dt.day)
 )
 B1.columns



# B1['Clase'] = np.where(
 #   B1['meses'] >= 30, 30,
  #  np.where(
   #     (B1['meses'] >= 24) & (B1['meses'] < 30), 24,
    #    np.where(
     #       (B1['meses'] >= 18) & (B1['meses'] < 24), 18,
      #      np.where(
       #         (B1['meses'] >= 12) & (B1['meses'] < 18), 12,
        #        6
         #   )
        #)
    #)
 #)
 C1 = B1[B1['PEOTRAS'] != 0]
 Primas = (
    C1
    .groupby(['Periodo_Origen'], as_index=False)
    .agg(
        Suma=('PEOTRAS', 'sum'),
        Numero=('POLIZA', lambda x: 
                len(set(zip(x, C1.loc[x.index, 'CERTIFICAD'])))),
        NumT=('POLIZA', 'size')
    )
    .drop_duplicates()
 )
 return Primas
  #################################################################################
  ##################################################################################
  ###Método siniestralidad cruzar prima y siniestros
  def Siniestralidad(X, Y):
    Res = X.merge(
        Y,
        left_on='Periodo_origen',
        right_on='Periodo_Origen',
        how='left'
    )
    
    # Evitar división por cero o NaN
    Res['Factor_S'] = np.where(
        (Res['Suma_y'].notnull()) & (Res['Suma_y'] != 0),
        Res['Suma_x'] / Res['Suma_y'],
        np.nan
    )
    
    return Res
    ##################################################################3
