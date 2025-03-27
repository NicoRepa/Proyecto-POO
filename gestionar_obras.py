from peewee import *
import pandas as pd
from abc import ABCMeta
import numpy as np


class GestionarObra(metaclass=ABCMeta):
    def __init__(self):
        pass

    #4.A
    @classmethod
    def extraer_datos(self):
        try:
            archivo_csv = "observatorio-de-obras-urbanas.csv"
            df = pd.read_csv(archivo_csv, sep=",")
            return df
        except FileNotFoundError as e:
            print("Error al conectar con el dataset.", e)
            return False

    #4.B
    @classmethod
    def conectar_db(self):
        sqlite_db = SqliteDatabase('obras_urbanas.db', pragmas={'journal_mode': 'wal'})
        try:
            sqlite_db.connect()
            return sqlite_db
        except OperationalError as e:
            print("Se ha generado un error en la conexion a la BD.", e)
            exit()

    #4.C
    @classmethod
    def mapear_orm(self, sqlite_db, lista):
        sqlite_db.create_tables(lista)

    #4.D
    @classmethod
    def limpiar_datos(self):
        df = self.extraer_datos()
        print(df)
        print("limpiando datos")
        df.dropna(subset=["monto_contrato", "comuna", "barrio", "direccion", "etapa","tipo", "area_responsable", "descripcion"], axis=0, inplace=True)
#-----------------------------------------------------------------------------------------------------------------------------------------------
        df['contratacion_tipo'] = df['contratacion_tipo'].str.lower()
        valores_a_eliminar = ['licitación', '-', 'lpu', 'convenio', 'obra de emergencia', '2095', 'bac', 'desestimada','sin efecto']
        df = df[~df['contratacion_tipo'].isin(valores_a_eliminar)]

        valores_a_reemplazar = ['556/2010', '556/10 y 433/16','556/10 y 433/16 ', '433/16 (decr necesidad y urgencia)','decreto n° 433/16', 'decreto 433/16', 'decreto 433', 'decreto 433/2016', '433']
        df['contratacion_tipo'] = df['contratacion_tipo'].replace(valores_a_reemplazar, 'decreto 433/16')

        valores_a_reemplazar_cdirecta=[ 'contratacion directa','contratacií“n directa','contratación directa','contratación directa - contratación menor','contratación de varias empresas','contratacion','contratacion de varias empresas']
        df['contratacion_tipo'] = df['contratacion_tipo'].replace(valores_a_reemplazar_cdirecta, 'contratacion directa')
        
        valores_a_reemplazar_mantenimiento=[ 'ad mantenimiento','anexo contratación mantenimiento','ad. mantenimiento','adicional de mantenimiento']
        df['contratacion_tipo'] = df['contratacion_tipo'].replace(valores_a_reemplazar_mantenimiento, 'adicional de mantenimiento')

        valores_a_reemplazar_privado= [ 'licitación privada','licitacion privada','licitación privada de obra menor','licitación privada obra menor','compulsa privada de precios']
        df['contratacion_tipo'] = df['contratacion_tipo'].replace(valores_a_reemplazar_privado, 'licitacion privada')

        valores_a_reemplazar_publico= ['licitación pública','licicitación pública ','licitaciã³n pãºblica','licitacion pública','licitacion pública ','licitación publica','licitacion publica','licitación pública nacional','licitacion pí¹blica','licitacíón pública','licitación pública internacional','obra publica','licitación pública ','licitación pública de obra mayor nâ° 682/sigaf/2020,','licitación pública abreviada.','licitaciones públicas\ncontrataciones menores\nconvenios marco']
        df['contratacion_tipo'] = df['contratacion_tipo'].replace(valores_a_reemplazar_publico, 'licitacion publica')
    
        varios_dict = {'contratación menor' : 'contratacion menor'}
        df['contratacion_tipo'] = df['contratacion_tipo'].replace(varios_dict)
#-----------------------------------------------------------------------------------------------
        df['tipo'] = df['tipo'].str.lower()
        varios_dict = {'hidráulica e infraestructura/ espacio público' : 'espacio público', 'vivienda nueva': 'vivienda'}
        df['tipo'] = df['tipo'].replace(varios_dict)
#-------------------------------------------------------------------------------------------------------
        df['etapa'] = df['etapa'].str.lower()
        varios_dict = {'en proyecto' : 'proyecto', 'finalizado' : 'finalizada', 'etapa 3 - frente 1' : 'proyecto', 'en ejecución ' : 'en ejecución', 'piloto 1' : 'piloto', 'piloto 2' : 'piloto'}
        df['etapa'] = df['etapa'].replace(varios_dict)
        return df

#--------------------------------------------------------------------------------------------------------------------------
    #4 E
    @classmethod
    def cargar_datos(self, comunas, areas_responsables, etapas, financiamiento, tipo_contratacion, tipo, empresa, barrios, Obra):
        df = self.limpiar_datos()

        data_unique = list(df['comuna'].unique())
        print(data_unique)
        for elem in data_unique:
            print("Elemento:", elem)
            try:
                comunas.create(nro_comuna=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Comuna.", e)
        print("Se han persistido los datos en la BD.")

        data_unique = list(df['area_responsable'].unique())
        print(data_unique)
        for elem in data_unique:
            print("Elemento:", elem)
            try:
                areas_responsables.create(nombre=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Area Responsable.", e)
        print("Se han persistido los datos en la BD.")

        data_unique = list(df['etapa'].unique())
        print(data_unique)
        for elem in data_unique:
            print("Elemento:", elem)
            try:
                etapas.create(tipos_etapas=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Etapa.", e)
        print("Se han persistido los datos en la BD.")

        data_unique = list(df['financiamiento'].unique())
        print(data_unique)
        for elem in data_unique:
            if elem is not np.nan:
                print("Elemento:", elem)
                try:
                    financiamiento.create(descripcion=elem)
                except IntegrityError as e:
                    print("Error al insertar un nuevo registro en la tabla Financiamiento.", e)
        print("Se han persistido los datos en la BD.")

        data_unique = list(df['contratacion_tipo'].unique())
        print(data_unique)
        for elem in data_unique:
            if elem is not np.nan:
                print("Elemento:", elem)
                try:
                    tipo_contratacion.create(tipos=elem)
                except IntegrityError as e:
                    print("Error al insertar un nuevo registro en la tabla Tipo de Contratacion.", e)
        print("Se han persistido los datos en la BD.")

        data_unique = list(df['tipo'].unique())
        print(data_unique)
        for elem in data_unique:
            print("Elemento:", elem)
            try:
                tipo.create(tipos=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Tipo de Obra.", e)
        print("Se han persistido los datos en la BD.")

        df.drop_duplicates(subset=['nombre'], inplace=True)
        for elem in df.values:
            if elem[2] is not np.nan:
                try:
                    Obra.create(financiamiento=elem[35],entorno=elem[1], nombre=elem[2], descripcion=elem[6], monto_contrato=elem[7], direccion=elem[10], fecha_inicio=elem[13], fecha_fin_inicial=elem[14], plazo_meses=elem[15], porcentaje_avance=0.0, licitacion_anio=elem[22],
                                nro_contratacion=elem[24], beneficiarios=elem[26], mano_obra=elem[27], expediente_numero=elem[33], etapa=elem[3], empresa=elem[21], tipo_obra=elem[4], area_responsable=elem[5], barrio=elem[9], tipo_contratacion=elem[23])
                except IntegrityError as e:
                    print("Error al insertar un nuevo registro en la tabla obras", e)
        print("Se han persistido los datos en la BD.")

        df.drop_duplicates(subset=['licitacion_oferta_empresa'], inplace=True)
        for elem in df.values:
            if elem is not np.nan:
                print(elem)
                try:
                    empresa.create(cuit=elem[25], nombre=elem[21])
                except IntegrityError as e:
                    print("Error al insertar un nuevo registro en la tabla Empresa.", e)
        print("Se han persistido los datos en la BD.")

        df.drop_duplicates(subset=['barrio'], inplace=True)
        for elem in df.values:
            if elem is not np.nan:
                print(elem)
                try:
                    barrios.create(nombre=elem[9], nro_comuna=elem[8])
                except IntegrityError as e:
                    print("Error al insertar un nuevo registro en la tabla barrio.", e)
        print("Se han persistido los datos en la BD.")

#4.F
    @classmethod
    def nueva_obra(self, Obra, tipo_obra, area_responsable, barrio, etapas):
        tipo_obra = "Sin definir"
        entorno = input("Ingrese el entorno: ")
        nombre = input("Ingrese el nombre: ")
        area_responsable = "Sin definir"
        descripcion = input("Ingrese una descripción: ")
        monto_contrato = input("Ingrese el monto del contrato: ")
        barrio = "Sin definir"
        direccion = input("Ingrese la dirección: ")
        plazo_meses = input("Ingrese el plazo de meses: ")
        beneficiarios = input("Ingrese quienes son los beneficiarios: ")
        etapas = "sin asignar"
        empre = "sin asignar"
        tipo_contrat = "sin asignar"

        obra = Obra(entorno=entorno, nombre=nombre, tipo_obra=tipo_obra, area_responsable=area_responsable,
                    descripcion=descripcion, monto_contrato=monto_contrato, barrio=barrio, direccion=direccion,
                    plazo_meses=plazo_meses, beneficiarios=beneficiarios, etapa=etapas, empresa=empre, tipo_contratacion=tipo_contrat, financiamiento="sin asignar")

        obra.save()
        return obra

#4.G
    @classmethod
    def obtener_indicadores(self, Obra,tipo, area_responsable, barrios, etapas):
        # a
        sqlite_db = self.conectar_db()
        print("Conexión exitosa a la base de datos")
        query = area_responsable.select().where(
            area_responsable.nombre != ' ')
        resultados = list(query)
        print("Las areas responsables son:")
        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.nombre)
            i = i+1
            lista.append(resultado.nombre)
        sqlite_db.close()


        # b
        sqlite_db = self.conectar_db()
        print("Conexión exitosa a la base de datos")

        query = tipo.select().where(tipo.tipos != ' ')
        resultados = list(query)
        # Recorre los resultados y los muestra
        print("Los tipo de obra son :")

        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.tipos)
            i = i+1
            lista.append(resultado.tipos)
        sqlite_db.close()


        # c
        sqlite_db = self.conectar_db()
        print("Conexión exitosa a la base de datos")

        query = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'finalizada')
        query2 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'en ejecución')
        query3 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'rescindida')
        query4 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'proyecto')
        query5 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'en obra')
        query6 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'en licitación')
        query7 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'neutralizada')
        query8 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'piloto')
        query9 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'en curso')
        count = query.scalar()
        count2 = query2.scalar()
        count3 = query3.scalar()
        count4 = query4.scalar()
        count5 = query5.scalar()
        count6 = query6.scalar()
        count7 = query7.scalar()
        count8 = query8.scalar()
        count9 = query9.scalar()
        print("La cantidad de obras finalizadas son: "+str(count))
        print("La cantidad de obras en ejecución son: "+str(count2))
        print("La cantidad de obras rescindidas son: "+str(count3))
        print("La cantidad de obras en proyecto son: "+str(count4))
        print("La cantidad de obras en obra son: "+str(count5))
        print("La cantidad de obras en licitacion son: "+str(count6))
        print("La cantidad de obras neutralizada son: "+str(count7))
        print("La cantidad de obras en piloto son: "+str(count8))
        print("La cantidad de obras en curso son: "+str(count9))


        # d
        query = tipo.select().where(tipo.tipos != ' ')
        resultados = list(query)
        for resultado in resultados:
            query = Obra.select(fn.COUNT()).where(Obra.tipo_obra_id == resultado.tipos)
            count = query.scalar()
            print("La cantidad de tipos de obra "+str(resultado.tipos)+" son: "+str(count))


        #e
        query = barrios.select().where(barrios.nro_comuna_id == '1' or barrios.nro_comuna_id == '2' or barrios.nro_comuna_id == '3')
        resultados = list(query)
        for resultado in resultados:
            print("Los barrios de las comunas 1, 2 y 3 son: "+str(resultado.nombre))


        # f
        suma=0
        for resultado in resultados:
            query = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'Finalizada' and Obra.barrio_id == resultado.nombre)
            count = query.scalar()
            suma=suma+count
        print("La cantidad de obras finalizadas en la comuna 1 son: "+str(suma))


        # g
        query = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'Finalizada' and Obra.plazo_meses <= 24)
        count = query.scalar()
        print("La cantidad de obras finalizadas en un plazo menor o igual a 24 meses son: "+str(count))


        #h
        query = Obra.select(fn.COUNT()).where(Obra.nombre != ' ')
        query2 = Obra.select(fn.COUNT()).where(Obra.etapa_id == 'finalizada')
        count = query.scalar()
        count_query2 = query2.scalar()
        resultado_final = (count_query2 / count)*100
        print("el porcentaje total de obras finalizadas es: ", resultado_final, '%')


        #i
        query= Obra.select(fn.SUM(Obra.mano_obra))
        count = query.scalar()
        print('el total de la mano de obra es:', count)

        #j
        query= Obra.select(fn.SUM(Obra.monto_contrato))
        count = query.scalar()
        print('el total de inversion es:', count, '$')
