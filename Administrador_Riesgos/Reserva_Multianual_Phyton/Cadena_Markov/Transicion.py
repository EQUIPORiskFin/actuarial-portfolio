#Contar la pólizas que nunca se han siniestrado
def Nunca_sin(Vigor, siniestrosF):

    B1 = Vigor.copy()
    B1["POLIZA"] = B1["POLIZA"].astype(str)
    B1["Key"] = B1["POLIZA"].str.replace(r"^\d+-", "", regex=True)

    A = siniestrosF.loc[
        siniestrosF["COBERTURA"] == "DESEMPLEO INVOLUNTARIO"
    ].copy()

    A["POLIZA"] = A["POLIZA"].astype(str)
    A["POLIZA_clean"] = A["POLIZA"]
    #A["POLIZA_clean"] = A["POLIZA"].str.replace(r"^\d+-", "", regex=True)

    A1 = (
        A.groupby(["CERTIFICADO", "POLIZA_clean"], as_index=False)["IMPORTE_PAGADO"]
        .sum()
        .rename(columns={
            "IMPORTE_PAGADO": "SUMA_A",
            "POLIZA_clean": "POLIZA"
        })
    )

    C1_resultado = B1.merge(
        A1,
        how="left",
        left_on=["CERTIFICAD", "Key"],
        right_on=["CERTIFICADO", "POLIZA"],
    )

    # 
    distintos = C1_resultado[C1_resultado['SUMA_A'].isna()]

    return len(distintos)
  #g = Nunca_sin(Vigor, siniestrosF)
######################################################################33
##########################################################################
import pandas as pd
import numpy as np
def Probabilidad(Vigor, siniestrosF, indicador_anio_origen):
    B = siniestrosF
    B = B[B['COBERTURA'] == "DESEMPLEO INVOLUNTARIO"]
    df_result = B.sort_values(["NRO_REPORTE", "FEC_PAGO"]).copy()

    # Agrupación
    g = df_result.groupby("NRO_REPORTE")

    # Fecha anterior
    df_result["fecha_ant"] = g["FEC_PAGO"].shift(1)

    # Índice dentro del grupo
    df_result["row_num"] = g.cumcount() + 1

    # Antecedente
    df_result["antecedente"] = df_result["row_num"] - 1
    #df_result["antecedente"] = df_result["antecedente"].clip(upper=7)

    # Cálculo de meses
    def diff_months(start, end):
        return (end.dt.year - start.dt.year) * 12 + (end.dt.month - start.dt.month)

    # Conversión de fechas
    df_result["FEC_PAGO"] = pd.to_datetime(df_result["FEC_PAGO"])
    df_result["FEC_VIG_DESDE"] = pd.to_datetime(df_result["FEC_VIG_DESDE"])
    df_result["fecha_ant"] = pd.to_datetime(df_result["fecha_ant"])

    # Tiempo
    df_result["tiempo"] = diff_months(df_result["fecha_ant"], df_result["FEC_PAGO"])

    # Ajuste para el primer registro
    mask = df_result["row_num"] == 1
    df_result.loc[mask, "tiempo"] = diff_months(
        df_result.loc[mask, "FEC_VIG_DESDE"],
        df_result.loc[mask, "FEC_PAGO"]
    )

    # Eliminar columna auxiliar
    df_result.drop(columns=["row_num"], inplace=True)

    # =======================
    # TABLA DE FRECUENCIAS
    # =======================
    tabla123 = df_result.pivot_table(
        index='tiempo',
        columns='antecedente',
        aggfunc='size',
        fill_value=0
    )
    indice = tabla123.index.max()/12
    tabla_sin7 = tabla123.drop(columns=7, errors='ignore')
    #tabla_sin7['restante'] = len(Vigor) - tabla123.sum(axis=1)

    # Normalización por fila
    #tabla_sin7 = tabla_sin7.div(tabla_sin7.sum(axis=1), axis=0)
    tabla_sin7 = tabla_sin7.sum(axis=0)/(indice* len(B) )
    media_columnas = tabla_sin7
    # Media por columnas
    #media_columnas = tabla_sin7.mean(axis=0)

    # =======================
    # MATRIZ DE TRANSICIÓN
    # =======================
    a = np.zeros((7, 7))

    p_0 = media_columnas.get(0, 0)
    p_1 = media_columnas.get(1, 0)
    p_2 = media_columnas.get(2, 0)
    p_3 = media_columnas.get(3, 0)
    p_4 = media_columnas.get(4, 0)
    p_5 = media_columnas.get(5, 0)

    #if p_0 > 0:
     #   a[0, 1] = p_1 / p_0
      #  a[0, 0] = 1 - a[0, 1]

    #if p_1 > 0:
     #   a[1, 2] = p_2 / p_1
      #  a[1, 1] = 1 - a[1, 2]

    #if p_2 > 0:
     #   a[2, 3] = p_3 / p_2
      #  a[2, 2] = 1 - a[2, 3]

    #if p_3 > 0:
     #   a[3, 4] = p_4 / p_3
      #  a[3, 3] = 1 - a[3, 4]

    #if p_4 > 0:
     #   a[4, 5] = p_5 / p_4
      #  a[4, 4] = 1 - a[4, 5]

    #if p_5 > 0:
     #   a[5, 6] = p_6 / p_5
      #  a[5, 5] = 1 - a[5, 6]

    # Estado absorbente
    a[0,1] = p_0
    a[0,0] =1-a[0,1]
    a[1,2] = p_1
    a[1,1] =1-a[1,2]
    a[2,3] = p_2
    a[2,2] =1-a[2,3]
    a[3,4] = p_3
    a[3,3] =1-a[3,4]
    a[4,5] = p_4
    a[4,4] =1-a[4,5]
    a[5,6] = p_5
    a[5,5] =1-a[5,6]
    a[6, 6] = 1

    # =======================
    # POTENCIA DE MATRIZ
    # =======================
    n = indicador_anio_origen
    a1 = np.linalg.matrix_power(a, n)

    # Ajuste de matriz (ojo aquí)
    matriz = np.delete(a1, 0, axis=1)
    matriz = np.delete(matriz, 6, axis=0)

    # =======================
    # VECTOR
    # =======================
    #Vec = np.array([p_0, p_1, p_2, p_3, p_4, p_5])
    Vec = np.array([1, 0, 0, 0, 0, 0])
    # Multiplicación por fila
    matriz = matriz * Vec[:, None]

    # Resultado final
    resul = matriz.sum()

    # Output
    K234 = []
    K234.append(resul)
    K234.append(matriz)
    K234.append(a1)
    K234.append(a)
    K234.append(Vec)

    return K234
#####################################################################################################################
def Probabilidades(Vigor, siniestrosF, MAX_DUR_REM):
  
    n4 = MAX_DUR_REM#Resumen['duracion_remanente'].max()

    v_values = np.arange(0, n4 + 1)

    G = [Probabilidad(Vigor, siniestrosF, int(k))[0] for k in v_values]

    return G
