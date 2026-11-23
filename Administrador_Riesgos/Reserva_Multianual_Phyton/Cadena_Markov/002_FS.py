#Metodo para calcular el factor de siniestralidad del año
def Factor_S_Demo(anio_origen, Res,tama):

    KJ = Res[Res['Periodo_origen'] == anio_origen]
    fecha_corte = KJ['Periodo_desarrollo'].max()

    Res1 = Res[
        (Res['Periodo_desarrollo'] <= fecha_corte) &
        (Res['Periodo_desarrollo'] >= anio_origen) &
        (Res['Periodo_origen'] >= anio_origen) &
        (Res['Periodo_origen'] <= fecha_corte)
    ].copy()

    Res1['Periodo_origen'] = pd.to_datetime(Res1['Periodo_origen'])
    Res1['Periodo_desarrollo'] = pd.to_datetime(Res1['Periodo_desarrollo'])

    Res1['Factor_S'] = Res1['Suma_x'] / Res1['Suma_y']

    Res1['dev'] = (
        (Res1['Periodo_desarrollo'].dt.year - Res1['Periodo_origen'].dt.year) * 12 +
        (Res1['Periodo_desarrollo'].dt.month - Res1['Periodo_origen'].dt.month)
    )

    triangulo = Res1.pivot_table(
        index='Periodo_origen',
        columns='dev',
        values='Factor_S',
        aggfunc='sum'
    ).fillna(0)

    triangulo = triangulo.reindex(
        columns=range(0, int(triangulo.columns.max()) + 1),
        fill_value=0
    )

    meses = triangulo.shape[1]

    
    def simula(k, tam):
        df = triangulo.to_numpy()

        den = df.sum(axis=0)
        den = np.where(den == 0, 1, den)

        p = (df / den)[:, k]
        mask = p != 0
        p_filtrado = p[mask]

        if p_filtrado.size == 0:
            p_filtrado = np.array([1])

        x = df[:, k]
        x_filtrado = x[x != 0]

        if x_filtrado.size == 0:
            x_filtrado = np.array([0])

        return np.random.choice(x_filtrado, size=tam, p=p_filtrado)

    
    def replace_zeros_with_D(df, D, u):
        df = df.copy().astype(float)

        for i in range(len(df)):
            zeros_idx = np.where(df.iloc[i] == 0)[0]

            for j, col_idx in enumerate(zeros_idx):
                if j < len(D) and u < len(D[j]):
                    df.iat[i, col_idx] = D[col_idx][u]

        return df

    
    ty = []
    K1 = []
    
    l = [simula(k, tama) for k in range(meses)]

    for u in range(tama):

        X = replace_zeros_with_D(triangulo, l, u)

        Z = X.mean(axis=1)

        ty.append(Z.mean())
    
        K1.append((Z.mean(), X.mean(axis=1), X, triangulo))
        
    
    Z_final = np.mean(ty)

    K1.append(("Z_final", Z_final))

    return K1
    ################################################################################
def Factores_siniestralidad(Resumen,tama,Res,cota,anio_origen):
   n4 = Resumen['duracion_remanente'].max()
   n4 = n4.astype(int)
   #t1 = n4//12
   #t2 = n4%12
   #if t2==0:
    # m4=t1 
   #else: 
    # m4 = t1+1
   v_values = np.arange(0, n4 + 1)
   #v_values[[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11]] = 21
   G  = [anio_origen + pd.DateOffset(years=d2) for d2 in v_values]
   G = [min(G[k],cota) for k in v_values]
   G = [Factor_S_Demo(G[k], Res, tam)[-1][1] for k in range(len(G))]
   return G
