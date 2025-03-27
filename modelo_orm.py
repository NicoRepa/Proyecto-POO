from peewee import *
from gestionar_obras import *

sqlite_db = GestionarObra().conectar_db()

class BaseModel(Model):

    class Meta:
        database = sqlite_db

class areas_responsables (BaseModel):
    nombre = CharField()
    class Meta:
        db_table = 'area_responsable'

class comunas (BaseModel):
    nro_comuna = IntegerField()
    class Meta:
        db_table = 'comunas'

class barrios (BaseModel):
    nombre = CharField()
    nro_comuna = ForeignKeyField(comunas, backref='comunas')
    class Meta:
        db_table = 'barrios'

class empresa (BaseModel):
    cuit = CharField()
    nombre = CharField()
    class Meta:
        db_table = 'empresa'

class etapas (BaseModel):
    tipos_etapas = CharField()
    class Meta:
        db_table = 'etapas'

class financiamiento (BaseModel):
    descripcion = CharField()
    class Meta:
        db_table = 'financiamiento'

class tipo_contratacion (BaseModel):
    tipos = CharField()
    class Meta:
        db_table = 'contratacion_tipo'

class tipo_obra (BaseModel):
    tipos = CharField()
    class Meta:
        db_table = 'tipo_obra'

class Obra (BaseModel):
    entorno = CharField()
    nombre = CharField()
    descripcion = CharField()
    monto_contrato = IntegerField()
    direccion = CharField()
    fecha_inicio = DateField(default='0/0/0000')
    fecha_fin_inicial = DateField(default='0/0/0000')
    plazo_meses = IntegerField()
    porcentaje_avance = DoubleField(default=0.0)
    licitacion_anio = DateField(default='0/0/0000')
    nro_contratacion = CharField(default='0')
    beneficiarios = CharField()
    mano_obra = CharField(default='0')
    expediente_numero = CharField(default='0')
    etapa = ForeignKeyField(etapas, backref='etapas')
    empresa = ForeignKeyField(empresa, backref='empresa')
    tipo_obra = ForeignKeyField(tipo_obra, backref='tipo_obra')
    area_responsable = ForeignKeyField(
        areas_responsables, backref='areas_responsables')
    barrio = ForeignKeyField(barrios, backref='barrios')
    tipo_contratacion = ForeignKeyField(
        tipo_contratacion, backref='tipo_contratacion')
    financiamiento = CharField()
    
    class Meta:
        db_table = 'Obra'

    def __str__(self):
        return "el entorno es: " + str(self.entorno) + "\nEl nombre de la obra es: " + str(self.nombre) + "\nEstá en la etapa de: " + str(self.etapa) + "\nEl tipo de obra es: " + str(self.tipo_obra) + "\nEl área responsable es: " + str(self.area_responsable) + "\nLa descripción es: " + str(self.descripcion) + "\nEl monto del contrato es: " + str(self.monto_contrato) + "\nUbicada en el barrio de: " + str(self.barrio) + "\nLa dirección es: " + str(self.direccion) + "\nFecha de inicio: " + str(self.fecha_inicio) + "\nLa fecha prevista para la finalizacion es: " + str(self.fecha_fin_inicial) + "\nEl plazo de meses estimado es de: " + str(self.plazo_meses) + " meses" + "\nEl porcentaje de avance es de: " + str(self.porcentaje_avance) + "%" + "\nLa empresa a cargo es: " + str(self.empresa) + "\nLa licitación es del año: " + str(self.licitacion_anio) + "\nEl tipo de contratación es: " + str(self.tipo_contratacion) + "\nEl número de contratación es: " + str(self.nro_contratacion) + "\nLos beneficiarios son: " + str(self.beneficiarios) + "\nLa mano de obra está compuesta por: " + str(self.mano_obra) + " empleados" + "\nEl expediente es el número: " + str(self.expediente_numero) + " \n " + str(self.fuente_financiamiento)

    def nuevo_proyecto(self):
        self.etapa = 'Proyecto'
        sqlite_db = GestionarObra().conectar_db()
        print("Conexión exitosa a la base de datos")


        # Consulta a la base de datos
        query = tipo_obra.select().where(tipo_obra.tipos != ' ')
        resultados = list(query)

        # Recorre los resultados y muestra las opciones
        print("Los tipos de obras son:")

        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.tipos)
            i = i+1
            lista.append(resultado.tipos)

        sqlite_db.close()


        opcion_elegida = int(input("Elija el número de opción: "))
        while True:
            if opcion_elegida > 0 and opcion_elegida < 12:
                try:
                    self.tipo_obra = lista[opcion_elegida-1]
                except:
                    print("Ingrese una opcion correcta")
                break
            else:
                print("Ingrese un número entre 1 y 11")
                opcion_elegida = int(input("Elija el número de opción: "))

        
        sqlite_db = GestionarObra().conectar_db()
        print("Conexión exitosa a la base de datos")

        query = areas_responsables.select().where(areas_responsables.nombre != ' ')
        resultados = list(query)
        print("Las areas responsables son:")
        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.nombre)
            i = i+1
            lista.append(resultado.nombre)
        sqlite_db.close()

        opcion_elegida = int(input("Elija el número de opción: "))
        while True:
            if opcion_elegida > 0 and opcion_elegida < 11:
                try:
                    self.area_responsable = lista[opcion_elegida-1]
                except:
                    print("Ingrese una opcion correcta")
                break
            else:
                print("Ingrese un número entre 1 y 10")
                opcion_elegida = int(input("Elija el número de opción: "))
                
        sqlite_db = GestionarObra().conectar_db()
        print("Conexión exitosa a la base de datos")

        query = barrios.select().where(barrios.nombre != ' ')
        resultados = list(query)
        print("Los barrios son:")

        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.nombre)
            i = i+1
            lista.append(resultado.nombre)
        sqlite_db.close()

        opcion_elegida = int(input("Elija el número de opción: "))
        while True:
            if opcion_elegida > 0 and opcion_elegida < 64:
                try:
                    self.barrio = lista[opcion_elegida-1]
                except:
                    print("Ingrese una opcion correcta")
                break
            else:
                print("Ingrese un número entre 1 y 63")
                opcion_elegida = int(input("Elija el número de opción: "))

    def iniciar_contratacion(self):
        sqlite_db = GestionarObra().conectar_db()
        print("Conexión exitosa a la base de datos")
        query = tipo_contratacion.select().where(tipo_contratacion.tipos != ' ')
        resultados = list(query)
        print("Los tipos de contratacion son:")

        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.tipos)
            i = i+1
            lista.append(resultado.tipos)
        sqlite_db.close()

        opcion_elegida = int(input("Elija el número de opción: "))
        while True:
            if opcion_elegida > 0 and opcion_elegida < 10:
                try:
                    self.tipo_contratacion = lista[opcion_elegida-1]
                except:
                    print("Ingrese una opcion correcta")
                break
            else:
                print("Ingrese un número entre 1 y 10")
                opcion_elegida = int(input("Elija el número de opción: "))

        self.nro_contratacion = int(input("Ingrese el número de contratación: "))

    def adjudicar_obra(self):
        sqlite_db = GestionarObra().conectar_db()
        print("Conexión exitosa a la base de datos")
        query = empresa.select().where(empresa.nombre != ' ')
        resultados = list(query)
        print("Los tipos son:")
        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.nombre)
            i = i+1
            lista.append(resultado.nombre)
        sqlite_db.close()

        opcion_elegida = int(input("Elija el número de opción: "))
        while True:
            if opcion_elegida > 0 and opcion_elegida < 466:
                try:
                    self.empresa = lista[opcion_elegida-1]
                except:
                    print("Ingrese una opcion correcta")
                break
            else:
                print("Ingrese un número entre 1 y 465")
                opcion_elegida = int(input("Elija el número de opción: "))

        self.expediente_numero = input("Ingrese el número de expediente: ")

    def iniciar_obra(self):

        self.fecha_inicio = input("Ingrese la fecha de inicio: ")
        self.fecha_fin_inicial = input("Ingrese la fecha estimada de fin: ")
        sqlite_db = GestionarObra().conectar_db()
        print("Conexión exitosa a la base de datos")

        query = financiamiento.select().where(
            financiamiento.descripcion != ' ')
        resultados = list(query)
        print("Las fuentes de financiamiento son:")

        i = 1
        lista = []
        for resultado in resultados:
            print(str(i)+" "+resultado.descripcion)
            i = i+1
            lista.append(resultado.descripcion)
        sqlite_db.close()

        opcion_elegida = int(input("Elija el número de opción: "))
        while True:
            if opcion_elegida > 0 and opcion_elegida < 8:
                try:
                    self.financiamiento= lista[opcion_elegida-1]
                except:
                    print("Ingrese una opcion correcta")
                break
            else:
                print("Ingrese un número entre 1 y 7")
                opcion_elegida = int(input("Elija el número de opción: "))

        self.mano_obra = int(input("Ingrese la cantidad de mano de obra: "))
    
    def actualizar_porcentaje_avance(self):
        self.porcentaje_avance =self.porcentaje_avance+ int(input("Ingrese el porcentaje de avance: "))

    def incrementar_plazo(self):
        incremento=int(input("Ingrese la cantidad de meses a incrementar: "))
        self.plazo_meses = int(self.plazo_meses) + incremento

    def incrementar_mano_obra(self):
        self.mano_obra = self.mano_obra + int(input("Ingrese la cantidad de mano de obra a incrementar: "))

    def finalizar_obra(self):
        self.porcentaje_avance = 100
        self.etapa = "Finalizada"

    def rescindir_obra(self):
        self.etapa = 'Rescindida'
