#!/usr/bin/env python
# coding: utf-8


def formatear(df, number):
    import pandas as pd
    import numpy as np
    from camelot import read_pdf

    # Se probara un primer formato con algunas páginas del pdf para tener mejor control

    # Anteriormente se uso un archivo exportado csv, para mayor rapidez se usara
    # un data frame, esto no muestra ningun NA, solo muestra espacios en blanco,
    # debido a que ya se habia creado el programa , solamente se reemplazaran con NA
    # ya que así funcionaba el programa.

    # También despues se observo que para algunas tablas se dispersaban los datos por los cual fue necesario unir columnas dentro de las tablas.

    df.replace("", np.nan, inplace=True)  # Se hacen NA los ""
    condicion = df.isna().sum(axis=0) > 25
    columnas = df.columns[condicion]  # Para >25 los datos estan separados
    df.replace(np.nan, "", inplace=True)  # Para unir se vuelven hacer ""

    for col in columnas:
        df.iloc[:, col + 1] += df.iloc[:, col]  # Se unen los datos dispersos

    df.drop(columns=columnas, inplace=True)  # Se elimina la columna inecesaria
    df.replace("", np.nan, inplace=True)

    # El siguiente ciclo es para unir filas, ya que el nombre del alimento estaba separado en varias filas. Despues se desechan las filas con los nombres de los alimentos repetidos.

    for i in range(3, 7):
        # En nutriente debe detenderse ya que acaba el name
        if df.loc[i].iloc[0] == "Nutriente":
            break
        df.loc[i].fillna("", inplace=True)  # Esto para que se puedan unir bien los name

    for j in range(4, i):
        df.loc[3] += " " + df.loc[j]  # Se unen las filas

    df.drop(index=(range(4, i + 1)), inplace=True)

    # Se eliminara tambien la fila que hace referencia a la energía medida en kilo Joules, y se quedara unicamente con la que es medida en kilo calorias

    kilo_joules = df[df.iloc[:, 0] == "Energía"].index + 1
    df.drop(index=kilo_joules, inplace=True)

    # Por convención se eliminaran aquellas filas con un numero mayor a catorce de valores nulos.

    nulos = df.isnull().sum(axis=1)
    df.drop(df[nulos > 8].index, inplace=True)

    # Se juntan las columnas numero 0 y 2 para ahorrar espacio y se más entendible, ahora
    # se pondra lo que se han medido y las unidades de medida utilizadas.
    #
    # Después se eliminaran las columnas que ya no se requieren, en este caso serán las que hacen referencia a las unidades de medida y el tagname, ya que pandas lee el simbolo de sodio Na como un valor nulo.

    info_nutri = df.iloc[:, 0] + " (" + df.iloc[:, 2] + ")"  # se fusionan columnas

    df.iloc[:, 0] = info_nutri  # Se reemplazan columnas

    # Se eliminan las columnas que ya no se necesitan
    column1 = df.iloc[:, 1].name
    column2 = df.iloc[:, 2].name
    df.drop(columns=[column1, column2], inplace=True)

    # Después se eliminaran las columnas que muestran las referencias a papers. Esto depende de para que se quiera el proyecto. Por último se eliminara la última fila.

    df.iloc[-1].fillna("", inplace=True)  # Se cambian los NA del la ultima fila
    fin = df.shape[1]
    columnas = [
        df.iloc[:, col].name for col in range(1, fin, 2)
    ]  # Se localizan las col
    df.drop(
        columns=columnas, inplace=True
    )  # Se eliminan las columnas referencias papers

    df.drop(df.iloc[-1].name, inplace=True)  # Se elimina la ultima fila

    # Ahora se aplicara la traspuesta al DataFrame

    df = df.transpose()

    # Se cambiara el nombre de las columnas por el nombre de los elementos de la primera fila, y despues se eliminará.

    columnas_nom = df.iloc[0]
    df.columns = columnas_nom
    df.drop(df.index[0], inplace=True)

    # Se reemplazan los simbolos "-" por NA, esto hace referencia que no se midio

    df.replace(["-"], np.nan, inplace=True)

    # En seguida se buscara si existen asteriscos en el data frame y se eliminaran

    def ast(x):
        """
        Esta funcion elimina los astericos en los datos
        """
        if "*" in x:
            x = x.replace("*", "")
        return x

    for columna in df.columns:
        try:
            df[columna] = df[columna].apply(ast)
        except TypeError:
            pass
        except KeyError:
            pass

    # Ahora se cambiara el tipo de dato, ya que la mayoria de las columnas se encuentran como tipos objetos

    for columna in df.columns:
        try:
            df[columna] = pd.to_numeric(df[columna])
        except ValueError:
            pass

    df.to_csv("alimentos" + str(number) + ".csv", index=False)
