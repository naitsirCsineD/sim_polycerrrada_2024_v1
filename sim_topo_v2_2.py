# -*- coding: utf-8 -*-



import pandas as pd
import numpy as np
import random
import datetime
import scipy.stats as stats
import time
from datetime import datetime
from datetime import datetime, timedelta
import random
import multiprocessing as mp


def calcular_acimut(df_topo):
  """
  Calcula el campo 'acimut' en df_topo usando la fórmula:
  '2R' * 2 * '_1R' + 'signo' * 'tan_beta'

  Args:
    df_topo: DataFrame con las columnas '2R', '_1R', 'signo' y 'tan_beta'.

  Returns:
    DataFrame df_topo con la columna 'acimut' agregada.
  """

  # Ensure all columns used in the formula are numeric
  df_topo['2R'] = pd.to_numeric(df_topo['2R'], errors='coerce')
  df_topo['signo'] = pd.to_numeric(df_topo['signo'], errors='coerce')
  df_topo['tan_beta'] = pd.to_numeric(df_topo['tan_beta'], errors='coerce')

  # Calculate 'acimut' using the formula
  df_topo['acimut'] = df_topo['2R'] * 2 * _1R[0] + df_topo['signo'] * df_topo['tan_beta']
  #df_topo['inclin'] = np.arctan(df_topo['tan_alfa']) * 2 * _1R[0] / np.pi
  #df_topo['inclin'] = df_topo['tan_alfa'].apply(np.arctan) * 2 * _1R[0] / np.pi
  #df_topo['inclin'] = df_topo['tan_alfa'].apply(np.arctan) * 2 * _1R[0] / np.pi



  return df_topo

def calcular_inclinacion(df_topo, _1R):
  """
  Calcula la inclinación usando la tangente alfa y la constante _1R.

  Args:
    df_topo: DataFrame con la columna 'tan_alfa'.
    _1R: Constante _1R.

  Returns:
    DataFrame df_topo con la columna 'inclin' agregada.
  """
  #print((df_topo['tan_alfa']))


  df_topo['inclin'] = np.arctan(df_topo['tan_alfa'].astype(float)) * 2 * _1R[0] / np.pi


  return df_topo

def calcular_ang_total(df_topo, new_df, _1R):
    """
    Calcula el campo 'ang_total' en df_topo según las condiciones especificadas.

    Args:
        df_topo: DataFrame con las columnas 'acimut' y 'e_anghz'.
        new_df: DataFrame con las columnas 'TipoObjeto' y 'Reiteración'.
        _1R: Valor de _1R.

    Returns:
        DataFrame df_topo con la columna 'ang_total' agregada.
    """

    # Obtén el valor de 'Reiteración' cuando 'TipoObjeto' es "Calaje" en new_df
    reiteracion_calaje = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'Reiteración'].values[0]

    # Obtén los valores de 'acimut' para 'Directo' y 'Calaje' en df_topo
    acimut_directo = df_topo.loc[df_topo['Tipo_obs'] == 'Directo', 'acimut'].values[0]
    acimut_calaje = df_topo.loc[df_topo['Tipo_obs'] == 'Calaje', 'acimut'].values[0]
    acimut_transito = df_topo.loc[df_topo['Tipo_obs'] == 'Transito', 'acimut'].values[0]

    # Calcula la diferencia inicial
    diferencia1 = acimut_directo - acimut_calaje + df_topo.loc[df_topo['Tipo_obs'] == 'Directo', 'e_anghz'].values[0] + df_topo.loc[df_topo['Tipo_obs'] == 'Calaje', 'e_anghz'].values[0]+ reiteracion_calaje
    diferencia2 = acimut_transito - acimut_calaje + df_topo.loc[df_topo['Tipo_obs'] == 'Transito', 'e_anghz'].values[0] + df_topo.loc[df_topo['Tipo_obs'] == 'Calaje', 'e_anghz'].values[0]+ reiteracion_calaje + 2*_1R[0]

    # Aplica las condiciones para ajustar la diferencia
    if diferencia1 < 0:
        diferencia1 += 4 * _1R[0]
    elif diferencia1 > 4 * _1R[0]:
        diferencia1 -= 4 * _1R[0]

    # Aplica las condiciones para ajustar la diferencia
    if diferencia2 < 0:
        diferencia2 += 4 * _1R[0]
    elif diferencia2 > 4 * _1R[0]:
        diferencia2 -= 4 * _1R[0]

    # Asigna la diferencia final a la columna 'ang_total' en df_topo para la fila 'Directo'
    df_topo.loc[df_topo['Tipo_obs'] == 'Directo', 'ang_total'] = diferencia1
    df_topo.loc[df_topo['Tipo_obs'] == 'Transito', 'ang_total'] = diferencia2

    return df_topo

def calcular_cuadrante(df_topo):
  """
  Calcula el campo 'cuadrante' de df_topo según las condiciones especificadas.

  Args:
    df_topo: DataFrame con las columnas 'dx' (N17 en Excel) y 'dy' (O17 en Excel).

  Returns:
    DataFrame df_topo con la columna 'cuadrante' agregada.
  """

  for index, row in df_topo.iterrows():
    dx = row['dx']
    dy = row['dy']

    if dy == 0:
      if dx >= 0:
        cuadrante = 2
      else:
        cuadrante = 4
    elif dy > 0:
      if dx >= 0:
        cuadrante = 1
      else:
        cuadrante = 4  # Corregido: Era 3, pero debe ser 4 según la fórmula
    else:  # dy < 0
      if dx >= 0:
        cuadrante = 2  # Corregido: Era 1, pero debe ser 2 según la fórmula
      else:
        cuadrante = 3

    df_topo.loc[index, 'cuadrante'] = cuadrante

  return df_topo

def calcular_2R(df_topo):
  """
  Calcula el campo '2R' de df_topo como la parte entera de 'cuadrante' / 2.

  Args:
    df_topo: DataFrame con la columna 'cuadrante'.

  Returns:
    DataFrame df_topo con la columna '2R' agregada.
  """

  df_topo['2R'] = (df_topo['cuadrante'] / 2).astype(int)

  return df_topo
  # Ejemplo de uso:

def calcular_signo(df_topo):
  """
  Calcula el campo 'signo' de df_topo usando la fórmula (-1)^(cuadrante + 1).

  Args:
    df_topo: DataFrame con la columna 'cuadrante'.

  Returns:
    DataFrame df_topo con la columna 'signo' agregada.
  """
  df_topo['signo'] = (-1)**(df_topo['cuadrante'] + 1)
  return df_topo

def calcular_distancia(df_topo):
  """
  Calcula la distancia usando dx, dy y dz de df_topo.

  Args:
    df_topo: DataFrame con las columnas 'dx', 'dy' y 'dz'.

  Returns:
    DataFrame df_topo con la columna 'distancia' agregada.
  """
    # Convert 'dx', 'dy', and 'dz' to float64 before calculation
  #df_topo['dx'] = df_topo['dx'].astype(np.float64)
  #df_topo['dy'] = df_topo['dy'].astype(np.float64)
  #df_topo['dz'] = df_topo['dz'].astype(np.float64)
  df_topo['DistanciaInclinada'] = np.sqrt(df_topo['dx']**2 + df_topo['dy']**2 + df_topo['dz']**2)
  
  return df_topo

def calcular_angulo_radianes_con_condicion(df_topo,_1R):
  """
  Calcula el ángulo en radianes del valor absoluto de la razón de dx y dy,
  con la condición de que si dy=0, el ángulo es pi/2.

  Args:
    df_topo: DataFrame con las columnas 'dx' y 'dy'.

  Returns:
    DataFrame df_topo con la columna 'angulo_radianes' agregada.
  """
  df_topo['tan_beta'] =np.where(df_topo['dy'] == 0, np.pi/2, np.arctan2(np.abs(df_topo['dy']), np.abs(df_topo['dx'])))*_1R[0]*2/np.pi
  return df_topo

def calcular_tan_alfax(df_topo):
  """
  Calcula tan_alfa para df_topo usando la fórmula (dz + HI_sim - HJ_sim) / dh.

  Args:
    df_topo: DataFrame con las columnas 'dz', 'HI_sim', 'HJ_sim', y 'dh'.

  Returns:
    DataFrame df_topo con la columna 'tan_alfa' actualizada.
  """
  df_topo['tan_alfa'] = (df_topo['dz']+ df_topo['HI_sim'] - df_topo['HJ_sim']) / df_topo['dh']
  return df_topo

def calcular_tan_alfa(df_topo):
  """
  Calcula tan_alfa para df_topo usando la fórmula (dz + HI_sim - HJ_sim) / dh.

  Args:
      df_topo: DataFrame con las columnas 'dz', 'HI_sim', 'HJ_sim', y 'dh'.

  Returns:
      DataFrame df_topo con la columna 'tan_alfa' actualizada.
  """
  # Convertir las columnas a numérico y reemplazar errores con NaN
  for col in ['dz', 'HI_sim', 'HJ_sim', 'dh']:
      df_topo[col] = pd.to_numeric(df_topo[col], errors='coerce')

  # Asegurar que no haya divisiones por cero en la columna 'dh'
  df_topo['tan_alfa'] = np.where(
      df_topo['dh'] != 0,
      (df_topo['dz'] + df_topo['HI_sim'] - df_topo['HJ_sim']) / df_topo['dh'],
      np.nan  # Si dh es 0, asignamos NaN para evitar error de división
  )

  return df_topo

def calcular_diferencias(df_topo, new_df):
  """
  Calcula las diferencias dx, dy y dz para df_topo utilizando los valores de new_df.
  Args:
    df_topo: DataFrame con las columnas "Tipo_obs", "CODIGO", "Nombre_Punto", etc.
    new_df: DataFrame con las columnas "station_type", "primary_key", "X1", "X2", "X3", etc.
  Returns:
    DataFrame df_topo con las columnas "dx", "dy", "dz" actualizadas.
  """

  for index,row in df_topo.iterrows():
    df_topo.loc[index, 'Nombre_Punto']=new_df.loc[index,'primary_key']


  df_topo.loc[2, 'Nombre_Punto']=df_topo.loc[2, 'Nombre_Punto']
  df_topo.loc[1, 'Nombre_Punto']=df_topo.loc[2, 'Nombre_Punto']




  # Obtén las coordenadas X, Y, Z de la estación y los puntos de observación
  estacion_coords = new_df[new_df['TipoObjeto'] == 'Estación'][['X', 'Y', 'Z']].values[0]
  #print(estacion_coords)
  calaje_coords = new_df[new_df['TipoObjeto'] == 'Calaje'][['X', 'Y', 'Z']].values[0]
  #print(calaje_coords)
  observacion_coords = new_df[new_df['TipoObjeto'] == 'Observación'][['X', 'Y', 'Z']].values[0]




  #print(observacion_coords)
  # Itera sobre las filas de df_topo y calcula las diferencias
  for index, row in df_topo.iterrows():
    if row['Tipo_obs'] == 'Calaje':
      # Diferencia entre Calaje - Estación
      df_topo.loc[index, ['dx', 'dy', 'dz']] = calaje_coords[0] - estacion_coords

    elif row['Tipo_obs'] =='Directo':
      df_topo.loc[index, ['dx', 'dy', 'dz']] = observacion_coords[0] - estacion_coords
    elif row['Tipo_obs']  =='Transito':
      df_topo.loc[index, ['dx', 'dy', 'dz']] = observacion_coords[0] - estacion_coords
  return df_topo

def calcular_dh(df):
    # Convertir las columnas a numéricas, reemplazando errores con NaN
    df[['dx', 'dy']] = df[['dx', 'dy']].apply(pd.to_numeric, errors='coerce')

    # Calcular la distancia inclinada
    df['dh'] = np.sqrt(df['dx']**2 + df['dy']**2 )
    return df

def calcular_di(df):
    # Convertir las columnas a numéricas, reemplazando errores con NaN
    df[['dx', 'dy', 'dz']] = df[['dx', 'dy', 'dz']].apply(pd.to_numeric, errors='coerce')

    # Calcular la distancia inclinada
    df['DistanciaInclinada'] = np.sqrt(df['dx']**2 + df['dy']**2 + df['dz']**2)
    return df

def estimar_valor(valor_medio, variacion):
  """
  Estima un valor dependiente de su valor medio y su variación,
  asumiendo que la variación corresponde al 95% de las observaciones.

  Args:
    valor_medio: El valor medio de la variable.
    variacion: La variación de la variable (que abarca el 95% de las observaciones).

  Returns:
    Una estimación del valor, considerando la variación.
  """

  # Asumiendo una distribución normal, la variación del 95%
  # corresponde a aproximadamente ±1.96 desviaciones estándar.
  desviacion_estandar = variacion / (2 * 1.96)

  # Genera un valor aleatorio a partir de una distribución normal
  # con la media y la desviación estándar calculadas.
  return np.random.normal(loc=valor_medio, scale=abs(desviacion_estandar))

def random_date(start, end):
    # Calcular un segundo aleatorio en el rango entre las dos fechas
    random_second = random.randint(0, int((end - start).total_seconds()))
    # Usar timedelta para sumar los segundos aleatorios a la fecha de inicio
    return start + timedelta(seconds=random_second)

def crear_coodenadas(num_dat):


  # Define el número de filas en el DataFrame
  num_rows = num_dat  # Puedes cambiar este valor

  # Crea una lista de tipos de estación
  station_types = ['EGeo'] + ['ELoc'] * (num_rows - 1)

  # Crea una lista de códigos numéricos únicos (primary key)
  primary_keys = [f'PK-{i:04d}' for i in range(1, num_rows + 1)]

  # Crea un DataFrame con los campos especificados
  data = {
      'station_type': station_types,
      'primary_key': primary_keys,
      'X': [random.randint(1000, 10000) for _ in range(num_rows)],
      'Y': [random.randint(1000, 10000) for _ in range(num_rows)],
      'Z': [random.randint(1000, 10000) for _ in range(num_rows)],
  }



  # Crear el DataFrame sin especificar dtype
  df = pd.DataFrame(data)

  # Cambiar el tipo de datos después de la creación del DataFrame
  df = df.astype({
      'station_type': 'string',
      'primary_key': 'string',
      'X': 'float64',
      'Y': 'float64',
      'Z': 'float64'
  })

  # Mostrar el DataFrame y los tipos de datos
  #print(df)
  #print(df.dtypes)


  # Muestra el DataFrame
  #print(df)
  return df

def parametros_topograficos(df,Equipo_topografico = ["1A", "1B", "2A", "2B"],
                            Instrumentos = ["TRIMBLE01", "M3", "TRIMBLE02"],
                            _1R=[100],
                            REITERACIONES = list(range(0, 450, 50)),
                            USOREFLECTOR=["Si","No"],
                            AlturaInst=[1.2,1.3,1.4,1.5,1.6],
                            AlturaJal=[-2.5,-2.2,-2.0,-1.5,-1.0,1,1.5,2,2.2,2.5],
                            Error0_Distancia=[3],
                            ErrorPPM_Distancia=[2.5],
                            ErrorAngula_Hz=[0.0003],
                            ErrorAngular_Vt=[0.0003],
                            ErrorAltura_Instrumento=[0.01],
                            ErrorAltura_Jalon=[0.05],
                            Error_Inst=[0.05]):



    #print(Equipo_topografico)
    #print(Instrumentos)
    #print(REITERACIONES)

    # Suponiendo que 'df' es tu DataFrame original

    # Filtra el DataFrame para obtener solo las filas con station_type = "ELoc"
    filtered_df = df[df['station_type'] == 'ELoc']
    #print('_'*50)

    x=[i for i in filtered_df.index]

    #print('x=',x)

    # Selecciona un índice aleatorio de las filas filtradas
    try:
      random_index = random.choice(x)
    except:
      print('falló')
      exit()
    # Obtén los índices de las filas anterior y siguiente
    previous_index = random_index - 1
    next_index = random_index + 1

    # Si el índice seleccionado es el último, usa el índice 2 para el siguiente
    if random_index == df.index[-1]:
        next_index = df.index[1]  # Aquí se selecciona como n+1, el registro N°2
    # Crea un nuevo DataFrame con las filas seleccionadas
    new_df = pd.concat([df.loc[[previous_index]], filtered_df.loc[[random_index]], df.loc[[next_index]]])

    # Reinicia el índice del nuevo DataFrame
    new_df = new_df.reset_index(drop=True)

    #print(new_df)



    # Suponiendo que 'new_df' es tu DataFrame

    # Define las nuevas columnas
    new_columns = ["TipoObjeto", "Reiteración", "REFLECTOR", "AlturaInstrumental", "AlturaJalón",
                  "Error0_Distancia", "ErrorPPM_Distancia", "ErrorAngula_Hz", "ErrorAngular_Vt",
                  "ErrorAltura_Instrumento", "ErrorAltura_Jalón","Error_Instalación"]

    tipos=[str,float,str,float,float,float,float,float,float,float,float,float]



    # Agrega las nuevas columnas al DataFrame con valores NaN
    for column in new_columns:
        new_df[column] = float('nan')  # o pd.NA si prefieres usar pandas.NA

    #print(new_df)



    for i, j in zip(tipos, new_columns):
        # Asegúrate de que 'i' es un tipo de dato válido como 'float', 'int', 'str', etc.
        new_df[j] = new_df[j].astype(i)  # Convierte la columna j al tipo especificado en 'i'
    return new_df


def Prep_Sim(new_df,REITERACIONES,USOREFLECTOR,AlturaInst,ErrorAltura_Instrumento,Error_Inst,AlturaJal,Error0_Distancia,ErrorPPM_Distancia,ErrorAngula_Hz,ErrorAngular_Vt,ErrorAltura_Jalon,contx):

  # Suponiendo que 'new_df' es tu DataFrame

  # Define la lista de valores para la columna "TipoObjeto"
  tipo_objeto_values = ["Calaje", "Estación", "Observación"]

  # Asigna los valores a la columna "TipoObjeto"
  new_df['TipoObjeto'] = np.tile(tipo_objeto_values, len(new_df) // len(tipo_objeto_values) + 1)[:len(new_df)]

  #new_df['TipoObjeto'] = ["Calaje", "Estación", "Observación"]


  # Filtra el DataFrame para obtener solo las filas con TipoObjeto = "Calaje"
  calaje_rows = new_df[new_df['TipoObjeto'] == 'Calaje']

  # Asigna valores aleatorios de REITERACIONES a la columna "Reiteración" para las filas filtradas
  new_df.loc[calaje_rows.index, 'Reiteración'] = random.choices(REITERACIONES, k=len(calaje_rows))
  


  # Suponiendo que 'new_df' es tu DataFrame y 'USOREFLECTOR' es tu lista

  # Filtra el DataFrame para obtener las filas con TipoObjeto = "Calaje" o "Observación"
  filtered_rows = new_df[(new_df['TipoObjeto'] == 'Calaje') | (new_df['TipoObjeto'] == 'Observación')]
  #new_df['REFLECTOR']=new_df['REFLECTOR'].astype(str)
  # Asigna valores aleatorios de USOREFLECTOR a la columna "REFLECTOR" para las filas filtradas
  new_df.loc[filtered_rows.index, 'REFLECTOR'] = random.choices(USOREFLECTOR, k=len(filtered_rows))

  # Si solo necesitas un valor aleatorio en lugar de una lista:
  # new_df.loc[filtered_rows.index, 'REFLECTOR'] = random.choice(USOREFLECTOR)

  # Filtra el DataFrame para obtener solo las filas con TipoObjeto = "Calaje"
  estacion_rows = new_df[new_df['TipoObjeto'] == 'Estación']

  # Asigna valores aleatorios de REITERACIONES a la columna "Reiteración" para las filas filtradas
  new_df.loc[estacion_rows.index, 'AlturaInstrumental'] = random.choices(AlturaInst, k=len(estacion_rows))
  # Asigna valores aleatorios de REITERACIONES a la columna "Reiteración" para las filas filtradas
  new_df.loc[estacion_rows.index, 'ErrorAltura_Instrumento'] = random.choices(ErrorAltura_Instrumento, k=len(estacion_rows))
  new_df.loc[estacion_rows.index, 'Error_Instalación'] = random.choices(Error_Inst, k=len(estacion_rows))



  # Filtra el DataFrame para obtener las filas con TipoObjeto = "Calaje" o "Observación"
  filtered_rows = new_df[(new_df['TipoObjeto'] == 'Calaje') | (new_df['TipoObjeto'] == 'Observación')]

  # Asigna valores aleatorios de USOREFLECTOR a la columna "REFLECTOR" para las filas filtradas
  new_df.loc[filtered_rows.index, 'AlturaJalón'] = random.choices(AlturaJal, k=len(filtered_rows))
  # Asigna valores aleatorios de USOREFLECTOR a la columna "REFLECTOR" para las filas filtradas
  new_df.loc[filtered_rows.index, 'Error0_Distancia'] = random.choices(Error0_Distancia, k=len(filtered_rows))
  # Asigna valores aleatorios de USOREFLECTOR a la columna "REFLECTOR" para las filas filtradas
  new_df.loc[filtered_rows.index, 'ErrorPPM_Distancia'] = random.choices(ErrorPPM_Distancia, k=len(filtered_rows))
  # Asigna valores aleatorios de USOREFLECTOR a la columna "REFLECTOR" para las filas filtradas
  new_df.loc[filtered_rows.index, 'ErrorAngula_Hz'] = random.choices(ErrorAngula_Hz, k=len(filtered_rows))
  # Asigna valores aleatorios de USOREFLECTOR a la columna "REFLECTOR" para las filas filtradas
  new_df.loc[filtered_rows.index, 'ErrorAngular_Vt'] = random.choices(ErrorAngular_Vt, k=len(filtered_rows))
  # Asigna valores aleatorios de USOREFLECTOR a la columna "REFLECTOR" para las filas filtradas
  new_df.loc[filtered_rows.index, 'ErrorAltura_Jalón'] = random.choices(ErrorAltura_Jalon, k=len(filtered_rows))
  new_df.loc[filtered_rows.index, 'Error_Instalación'] = random.choices(Error_Inst, k=len(filtered_rows))


  #print(new_df)


  #print('_'*5  0)
  '''
  for j in ['X','Y','Z']:
    for i in new_df['TipoObjeto']:
      # Obtén el valor medio y la variación de new_df para TipoObjeto == "Estación"
      esperado=new_df.loc[new_df['TipoObjeto'] == i, j].values[0]
      variacion=new_df.loc[new_df['TipoObjeto'] == i, 'Error_Instalación'].values[0]
      new_df.loc[new_df['TipoObjeto'] == i, j]=estimar_valor(esperado, variacion)
  '''
  # Add this line to rename the column 'Reiteración' to 'REITERACION_CALAJE'
  # for rows where 'TipoObjeto' is 'Calaje'
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'REITERACION_CALAJE'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'Reiteración']

  # Add similar lines for other columns you want to rename:
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'REFLECTOR_CALAJE'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'REFLECTOR']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'REFLECTOR_OBSERVACIÓN'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'REFLECTOR']
  new_df.loc[new_df['TipoObjeto'] == 'Estación', 'ALTURA_INSTRUMENTO'] = new_df.loc[new_df['TipoObjeto'] == 'Estación', 'AlturaInstrumental']
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ALTURA_JALÓN_CALAJE'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'AlturaJalón']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ALTURA_JALÓN_OBJETIVO'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'AlturaJalón']
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorDistancia_Base_Calaje'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'Error0_Distancia']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorDistancia_Base_Objetivo'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'Error0_Distancia']
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorDistancia_ppm_Calaje'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorPPM_Distancia']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorDistancia_ppm_Objetivo'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorPPM_Distancia']
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAnguloHz_Calaje'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAngula_Hz']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAnguloHz_Objetivo'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAngula_Hz']
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAnguloVt_Calaje'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAngular_Vt']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAnguloVt_Objetivo'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAngular_Vt']
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAlturaInstrumental'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAltura_Instrumento']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAlturaJalón_Calaje'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAltura_Jalón']
  new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAlturaJalón_Objetivo'] = new_df.loc[new_df['TipoObjeto'] == 'Calaje', 'ErrorAltura_Jalón']
  new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAlturaJalón_Objetivo'] = new_df.loc[new_df['TipoObjeto'] == 'Observación', 'ErrorAltura_Jalón']
  new_df.loc[new_df['TipoObjeto'] == 'Estación', 'NombreEstación'] = new_df.loc[new_df['TipoObjeto'] == 'Estación', 'primary_key']
  new_df.loc[new_df['TipoObjeto'] == 'Estación', 'Tipo'] = 'Estación Topográfica'

  #new_df['COD_LEVANTAMIENTO']=crear_texto_con_prefijo_numeral_sufijo(contx)

  return new_df

def crear_texto_con_prefijo_numeral_sufijo(cont,prefijo = "SIM01_",sufijo = "_v1"):
  """
  Crea un texto con un prefijo, un numeral con ceros a la izquierda y un sufijo.

  Args:
    cont: El número a usar en el numeral.

  Returns:
    El texto con el formato "prefijo_numeral_sufijo".
  """



  # Calcula el número de ceros a la izquierda
  num_ceros = 5 - len(str(cont))

  # Crea el numeral con ceros a la izquierda
  numeral = str(cont).zfill(5)  # zfill agrega ceros a la izquierda

  # Crea el texto completo
  texto_completo = prefijo + numeral + sufijo

  return texto_completo


def procesar_fila(args):
    tipo_objeto, j, new_df = args
    esperado = new_df.loc[new_df['TipoObjeto'] == tipo_objeto, j].values[0]
    variacion = new_df.loc[new_df['TipoObjeto'] == tipo_objeto, 'Error_Instalación'].values[0]
    return tipo_objeto, j, estimar_valor(esperado, variacion)

def actualizar_df(new_df):
    # Crear una lista de tareas para ejecutar en paralelo
    tareas = [(i, j, new_df) for i in new_df['TipoObjeto'] for j in ['X', 'Y', 'Z']]

    # Usar Pool para ejecutar las tareas en paralelo
    with mp.Pool(processes=mp.cpu_count()) as pool:
        resultados = pool.map(procesar_fila, tareas)

    # Actualizar el DataFrame con los resultados obtenidos
    for tipo_objeto, j, valor in resultados:
        new_df.loc[new_df['TipoObjeto'] == tipo_objeto, j] = valor
########################################################################################################################################

######################################################################################################################################

######################################################################################################################################

######################################################################################################################################

######################################################################################################################################

######################################################################################################################################

######################################################################################################################################

######################################################################################################################################

######################################################################################################################################

 

tiempos=0

Num_estaciones=20
Num_sim=1000

# Ejemplo de uso:
Equipo_topografico = ["1A", "1B", "2A", "2B"]
Instrumentos = ["TRIMBLE01", "M3", "TRIMBLE02"]
_1R=[100]
REITERACIONES = list(range(0, 450, 50))
USOREFLECTOR=["Si","No"]
AlturaInst=[1.2,1.3,1.4,1.5,1.6]
AlturaJal=[-2.5,-2.2,-2.0,-1.5,-1.0,1,1.5,2,2.2,2.5]
Error0_Distancia=[3]
ErrorPPM_Distancia=[2.5]
ErrorAngula_Hz=[0.0003]
ErrorAngular_Vt=[0.0003]
ErrorAltura_Instrumento=[0.01]
ErrorAltura_Jalon=[0.05]
Error_Inst=[0.05]



#*************************************************************************************************************
#                                                                                                                |
#                                                                                            Se crean Coordenadas|

df=crear_coodenadas(Num_estaciones)

df.to_csv('coordenadas.csv',index=False)


columnas=[
  "FECHA", 
  "EQUIPO_TOPO", 
  "INSTRUMENTO", 
  "_1R", 
  "REITERACION_CALAJE", 
  "REFLECTOR_CALAJE", 
  "REFLECTOR_OBSERVACIÓN", 
  "ALTURA_INSTRUMENTO", 
  "ALTURA_JALÓN_CALAJE", 
  "ALTURA_JALÓN_OBJETIVO", 
  "ErrorDistancia_Base_Calaje", 
  "ErrorDistancia_Base_Objetivo", 
  "ErrorDistancia_ppm_Calaje", 
  "ErrorDistancia_ppm_Objetivo", 
  "ErrorAnguloHz_Calaje", 
  "ErrorAnguloHz_Objetivo", 
  "ErrorAnguloVt_Calaje", 
  "ErrorAnguloVt_Objetivo", 
  "ErrorAlturaInstrumental", 
  "ErrorAlturaJalón_Calaje", 
  "ErrorAlturaJalón_Objetivo", 
  "NombreEstación", 
  "Tipo", 
  "COD", 
  "Nombre Punto", 
  "DistanciaInclinada", 
  "Ang_Hz", 
  "Ang_vt", 
  "DistanciaHorizontal", 
  "DX", 
  "DY", 
  "DZ"
  ]
dbaseTopografica=pd.DataFrame(columns=columnas)

dtype = {
    'CODIGO': 'str',
    'FechaHora': 'datetime64[ns]',
    'EQUIPOTRABAJO': 'str',
    'INSTRUMENTO': 'str'
}
#                                                                                                                |
#                                   Crear un DataFrame vacío con los nombres de las columnas y los tipos de datos|
df_lev = pd.DataFrame(data=None, columns=dtype.keys()).astype(dtype)

par_lev={}
par_topo=[]
lev=[]


start_time=time.time() # inicio reloj control timepo Total


for cont in range(Num_sim):  #ciclo para simular 10 toma de datos de topografias
  #Generador de fechas aleatorias para asignar un afecha a un dato, solo es para tener registro de fechas
  
  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -9
  inicio=time.time() #Control tiempos
  
  #*************************************************************************************************************
  #                                                                                                              |
  #                                                                                            Generador de Fecha|
  start_date = datetime(2023, 1, 1,8,30)
  end_date = datetime(2023, 12, 31,18,30)
  random_date_generated = random_date(start_date, end_date)


  #elapsed_time = time.time() - inicio # control Tiempos
  #tiempos=elapsed_time+tiempos #control Tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -8 este bloque gasta el 39% del tiempo de calculo
  #inicio=time.time()
  
  #*************************************************************************************************************
  
  #                                                                                          Se crea el df new_df|
  new_df=parametros_topograficos(df)

  #                                                                        se pobla el df con la función Prep_sim|
  new_df=Prep_Sim(
    new_df,
    REITERACIONES,
    USOREFLECTOR,
    AlturaInst,
    ErrorAltura_Instrumento,
    Error_Inst,AlturaJal,
    Error0_Distancia,
    ErrorPPM_Distancia,
    ErrorAngula_Hz,
    ErrorAngular_Vt,
    ErrorAltura_Jalon,cont)

  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos

  #                                                     adherir error en la instlación del isntrumento y jalones|
  
  for j in ['X','Y','Z']:
    for i in new_df['TipoObjeto']:
      # Obtén el valor medio y la variación de new_df para TipoObjeto == "Estación"
      esperado=new_df.loc[new_df['TipoObjeto'] == i, j].values[0]
      variacion=new_df.loc[new_df['TipoObjeto'] == i, 'Error_Instalación'].values[0]
      nuevo_valor=estimar_valor(esperado, variacion)
      new_df.loc[new_df['TipoObjeto'] == i, j]=nuevo_valor
  

  #                                                                             asignar el codigo de levatameinto|

  new_df['COD_LEVANTAMIENTO']=crear_texto_con_prefijo_numeral_sufijo(cont)

  #Hasta acá los parámetros ya estan asigados los parámetros a cada punto a utilizar

  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -7 este bloque gasta el 12% del tiempo de calculo
  #inicio=time.time()

  #                                                        crear el diciconario para parametros de levantamiento|
  par_lev[cont]={
    'CODIGO':crear_texto_con_prefijo_numeral_sufijo(cont),
    'FechaHora':random_date_generated,
    'EQUIPOTRABAJO':random.choice(Equipo_topografico),
    'INSTRUMENTO': random.choice(Instrumentos)
  }
  #                                         convertir datos de new_df en diccionario para parametros topograficos|
  for i in new_df.to_dict(orient='records'):
    par_topo.append(i)

 
  #                                                                         crear el dataframe para Levantamiento|
  # Define los nombres de las columnas
  column_names = ["Tipo_obs", "CODIGO", "Nombre_Punto", "DistanciaInclinada", "Ang_Hz", "Ang_Vt",
                  "dx", "dy", "dz", "dh", "tan_alfa", "tan_beta", "cuadrante", "2R", "signo",
                  "e_dist", "e_anghz", "e_angvt", "acimut", "inclin", "HI_sim", "HJ_sim", "ang_total"]

  # Crea un DataFrame vacío con las columnas especificadas
  df_topo = pd.DataFrame(columns=column_names).astype({
    "Tipo_obs":'string', 
    "CODIGO":'string', 
    "Nombre_Punto":'string', 
    "DistanciaInclinada":'float', 
    "Ang_Hz":'float', 
    "Ang_Vt":'float',
    "dx":'float', 
    "dy":'float', 
    "dz":'float', 
    "dh":'float', 
    "tan_alfa":'float', 
    "tan_beta":'float', 
    "cuadrante":'float', 
    "2R":'float', 
    "signo":'float',
    "e_dist":'float', 
    "e_anghz":'float', 
    "e_angvt":'float', 
    "acimut":'float', 
    "inclin":'float', 
    "HI_sim":'float', 
    "HJ_sim":'float', 
    "ang_total":'float'
  })


  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -6 este bloque gasta el 10% del tiempo de calculo
  #inicio=time.time()
  # Define la lista de valores para la columna "TipoObjeto"
  #                                                                                  calcular una fecha aleatoria
  dbaseTopografica['FECHA']=random_date(start_date, end_date)
  #                                                                                                             |
  #                                                                      definir el tipo de objetivo en el visor|


  df_topo['Tipo_obs'] = ["Calaje", "Directo", "Transito"]
  #Hasta acá la fila 0 es calaje, fila 1 Directo, fila 2 es Transito

  '''
    # Calcula el valor de HI_sim para cada fila de df_topo
    for index, row in df_topo.iterrows():
      df_topo.loc[index, 'dx'] = estimar_valor(df_topo.loc[index, 'dx'], variación)
      df_topo.loc[index, 'dy'] = estimar_valor(df_topo.loc[index, 'dy'], variación)
      df_topo.loc[index, 'dz'] = estimar_valor(df_topo.loc[index, 'dz'], variación)
  '''
  #                                                                                                             |
  #                                                                         calculo de diferencia de coordeandas|

  df_topo=calcular_diferencias(df_topo, new_df)

  #Nota[1] se calcualn las coordanadas ya con el error de isntalación, pero la lectura de directo 
  # y transito no incluyen, ene esta etapa el error angular


  #                                                                                                             |
  #                                                                      adherir el error de altura instrumental|

  # Obtén el valor medio y la variación de new_df para TipoObjeto == "Estación"
  valor_medio_HI = new_df.loc[new_df['TipoObjeto'] == 'Estación', 'AlturaInstrumental'].values[0]
  variacion_HI = new_df.loc[new_df['TipoObjeto'] == 'Estación', 'ErrorAltura_Instrumento'].values[0]

  
  # Calcula el valor de HI_sim para cada fila de df_topo
  for index, row in df_topo.iterrows():
    df_topo.loc[index, 'HI_sim'] = estimar_valor(valor_medio_HI, variacion_HI)



  df_topo['CODIGO']=crear_texto_con_prefijo_numeral_sufijo(cont)

  #                                                                                                             |
  #                                                                       Adherir el error de altura en el jalón|   

  for i in new_df['TipoObjeto']:
    # Obtén el valor medio y la variación de new_df para TipoObjeto == "Estación"
    valor_medio_HJ = new_df.loc[new_df['TipoObjeto'] == i, 'AlturaJalón'].values[0]
    variacion_HJ = new_df.loc[new_df['TipoObjeto'] == i, 'ErrorAltura_Jalón'].values[0]
    # Calcula el valor de HI_sim para las filas donde Tipo_obs NO es "Calaje"
    for index, row in df_topo.iterrows():
        if row['Tipo_obs'] == i:
            df_topo.loc[index, 'HJ_sim'] = estimar_valor(valor_medio_HJ, variacion_HJ)
        else:
            df_topo.loc[index, 'HJ_sim'] = estimar_valor(valor_medio_HJ, variacion_HJ)



  #                                                                                                             |
  #                                                                                Adherir el error de distancia| 

  #                                                         calcular distancia inclinada inicial de las lecturas|
  df_topo = calcular_di(df_topo)

  #                                                                      registrara error de distancia en new_df|

  for i in ['Calaje','Observación']:
    # Obtén el valor medio y la variación de new_df para TipoObjeto == "Estación"
    valor_medio_Error0_Distancia = new_df.loc[new_df['TipoObjeto'] == i, 'Error0_Distancia'].values[0]
    valor_medio_ErrorPPM_Distancia = new_df.loc[new_df['TipoObjeto'] == i, 'ErrorPPM_Distancia'].values[0]
    e_anghz = new_df.loc[new_df['TipoObjeto'] == i, 'ErrorAngula_Hz'].values[0]
    # Check if 'ErrorAngula_Vt' column exists before accessing it
    if 'ErrorAngula_Vt' in new_df.columns:
      e_angvt = new_df.loc[new_df['TipoObjeto'] == i, 'ErrorAngula_Vt'].values[0]
    else:
      # Handle the case where the column is missing, e.g., set a default value
      e_angvt = 0.003  # or any other appropriate value

  #                               Se calculan los errores de distancia inclinada, angulos horizontale y vertical|
      
  
    for index, row in df_topo.iterrows():

      valormedio=df_topo.loc[index, 'DistanciaInclinada']
           
      variacion=(valormedio*valor_medio_ErrorPPM_Distancia*0.001+valor_medio_Error0_Distancia)*0.001
      if (df_topo.loc[index, 'Tipo_obs']=='Calaje' and i=='Calaje'):
        #print(f'Levantamiento  {i} - {df_topo.loc[index, 'Tipo_obs']} ')
        indice=0
        df_topo.loc[indice, 'e_dist'] = estimar_valor(0, variacion)
        #print(f'{df_topo.loc[indice, 'e_dist']}=estimar_valor(0,{variacion})')
        df_topo.loc[indice, 'e_dist'] = estimar_valor(0, variacion)
        df_topo.loc[indice, 'DistanciaInclinada'] = estimar_valor(valormedio, variacion)
        df_topo.loc[indice, 'e_anghz'] = estimar_valor(0, e_anghz)
        df_topo.loc[indice, 'e_angvt'] = estimar_valor(0, e_angvt)
      elif (df_topo.loc[index, 'Tipo_obs']=='Directo' and i!='Calaje'):
        #print(f'Levantamiento  {i} - {df_topo.loc[index, 'Tipo_obs']} ')
        indice=1
        df_topo.loc[indice, 'e_dist'] = estimar_valor(0, variacion)
        #print(f'{df_topo.loc[indice, 'e_dist']}=estimar_valor(0,{variacion})')
        df_topo.loc[indice, 'e_dist'] = estimar_valor(0, variacion)
        df_topo.loc[indice, 'DistanciaInclinada'] = estimar_valor(valormedio, variacion)
        df_topo.loc[indice, 'e_anghz'] = estimar_valor(0, e_anghz)
        df_topo.loc[indice, 'e_angvt'] = estimar_valor(0, e_angvt)
      elif (df_topo.loc[index, 'Tipo_obs']=='Transito' and i !='Calaje'):
        #print(f'Levantamiento  {i} - {df_topo.loc[index, 'Tipo_obs']} ')
        indice=2   
        df_topo.loc[indice, 'e_dist'] = estimar_valor(0, variacion)
        #print(f'{df_topo.loc[indice, 'e_dist']}=estimar_valor(0,{variacion})')
        df_topo.loc[indice, 'e_dist'] = estimar_valor(0, variacion)
        df_topo.loc[indice, 'DistanciaInclinada'] = estimar_valor(valormedio, variacion)
        
        df_topo.loc[indice, 'e_anghz'] = estimar_valor(0, e_anghz)
        df_topo.loc[indice, 'e_angvt'] = estimar_valor(0, e_angvt)    

    
    
    #                        Se calculan la distancia horizontal, con error de coordenadas, sin error instrumental|   
  # Hasta acá se han calculado las diferencias de coordendas entre el calaje y el objetivo, sin error
  df_topo = calcular_dh(df_topo)
  #print(df_topo)

  #Hasta acá se ha calcula la distancia horizontal
  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -5
  #inicio=time.time()

#                                   se calculan parámetros geometricos de la geometría de los puntos levantados| 

  df_topo = calcular_tan_alfa(df_topo)

  df_topo = calcular_angulo_radianes_con_condicion(df_topo,_1R)

  df_topo = calcular_cuadrante(df_topo)

  df_topo = calcular_2R(df_topo)

    # Ejemplo de uso:
  df_topo = calcular_signo(df_topo)




  #Hasta acá de ha calculado la altura de jalón del calaje y del objetivo, en directo y en transito
  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -4
  #inicio=time.time()
  #                                                                                                              |
  #            se calculan el acimut, la inclinación y el angulo horizontal que forman el cvalaje con el objetivo|
  df_topo = calcular_acimut(df_topo)
  df_topo = calcular_inclinacion(df_topo, _1R)
  df_topo=calcular_ang_total(df_topo, new_df, _1R)
  df_topo['CODIGO']=df_topo['CODIGO'].astype(str)




  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos

  
  #------------------------------------------------------------------------------------------------------------
  #bloque -3 #bloque -6 este bloque gasta el 12% del tiempo de calculo
  #inicio=time.time()
  #                                                                                                              |
  #                                                                       se asigananvalores finales de la tabla |

  calaje_rows = new_df[new_df['TipoObjeto'] == 'Calaje']
  df_topo['Ang_Hz']=df_topo['ang_total']
  df_topo.loc[0, 'Ang_Hz'] = new_df.loc[calaje_rows.index[0], 'Reiteración']
  df_topo['Ang_Vt']=df_topo['inclin']
  
  #elapsed_time = time.time() - inicio
  #tiempos=elapsed_time+tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -2
  #inicio=time.time()
  
  #                                                                                                              |
  #                                                     se convierten los datos del levantameinto de diccionario |
  for i in df_topo.to_dict(orient='records'):
    lev.append(i)
  


  elapsed_time = time.time() - inicio
  tiempos=elapsed_time+tiempos
  #------------------------------------------------------------------------------------------------------------
  #bloque -1
  #inicio=time.time()





df_lev=pd.DataFrame.from_dict(par_lev, orient='index')



par_topo1=pd.DataFrame(par_topo)
topo1=pd.DataFrame(lev)
# Calcula el tiempo transcurrido


df_lev.to_csv('parametros_levantamiento.csv',index=False)
par_topo1.to_csv('parametros_topograficos.csv',index=False)
topo1.to_csv('Levantamiento.csv',index=False)
#print(dbaseTopografica)
elapsed_time = time.time() - start_time
tiempos=tiempos/Num_sim
print(f"Tiempo de ejecución Total: {tiempos:.5f} segundos")
print(f"Tiempo de ejecución Total: {elapsed_time:.5f} segundos")