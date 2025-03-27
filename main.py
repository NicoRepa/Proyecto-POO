from gestionar_obras import *
from modelo_orm import *


def main():
    print("Menu de opciones:")
    print(" 1)crear estructura de obra\n","2) cargar datos\n","3) crear 2 obras\n","4)obtener indicadores\n","5)salir")

    while True:
        eleccion = int(input('elija una opcion segun su numero: '))
        if 0 < eleccion <6:
            break
        else:
            print('ingrese una opcion valida')
    match eleccion:
        case 1:
            lista = [barrios, areas_responsables, comunas, empresa,etapas, Obra, tipo_obra, tipo_contratacion, financiamiento]
            GestionarObra().mapear_orm(sqlite_db, lista)
            print("Estructura creada con éxito")

        case 2:
            GestionarObra().cargar_datos(comunas, areas_responsables, etapas, financiamiento, tipo_contratacion, tipo_obra, empresa, barrios, Obra)

        case 3:
            print("Ingrese los datos de obra 1")
            obra1 = GestionarObra().nueva_obra(Obra, tipo_obra, areas_responsables, barrios, etapas)
            print("Ingrese los datos de obra 2")
            obra2 = GestionarObra().nueva_obra(Obra, tipo_obra, areas_responsables, barrios, etapas)
            print("Obras creadas con exito")
            print("\n¿Desea pasar por los diferentes estados de la obra?")
            lista=["si","no"]
            i=1
            for opcion in lista:
                print(str(i)+") "+opcion)
                i=i+1
            respuesta = int(input("Elija el número de opción: "))
            opcion_elegida = lista[respuesta-1]
            if opcion_elegida == "si":
                print("\nIngrese los datos de proyecto 1")
                obra1.nuevo_proyecto()

                print("Proyectos creados con exito")

                obra1.save()
                print("\nIngrese la contratación de la obra 1: ")
                obra1.iniciar_contratacion()
                obra1.save()

                print("\nIngrese la adjudicación de la obra 1: ")
                obra1.adjudicar_obra()
                print("\nIngrese el inicio de la obra 1: ")
                obra1.iniciar_obra()
                obra1.save()

                print("\nIngrese el porcentaje de avance de la obra 1: ")
                obra1.actualizar_porcentaje_avance()
                obra1.save()
                print('desea incrementar los datos de la obra 1? ')
                print('1)si \n 2)no')
                opcionn = int(input('ingrese la opcion q decida: '))
                if opcionn == 1:
                    print("\nIngrese el plazo incrementado de la obra 1: ")
                    obra1.incrementar_plazo()
                    obra1.save()

                    print("\nIngrese la cantidad de empleados que desea agregar a la obra 1: ")
                    obra1.incrementar_mano_obra()
                    obra1.save()
                elif opcionn == 2:
                    print('no vas a incrementar los datos')
                    obra1.save()

                print('\ncon la obra 1 desea rescindir o finalizarla?')
                print('1)rescindir \n 2)finalizar')
                opcion1 = int(input('elija la opcion: '))
                if opcion1 == 1:
                    obra1.rescindir_obra()
                    print('se rescindio la obra 1')
                elif opcion1 == 2:
                    obra1.finalizar_obra()
                    print('se finalizo la obra 1')
                obra1.save()
#------------------------------------------------------------------------
                print("\nIngrese los datos de proyecto 2")
                obra2.nuevo_proyecto()
                obra2.save()

                print("\nIngrese la contratación de la obra 2:")
                obra2.iniciar_contratacion()
                obra2.save()

                print("\nIngrese la adjudicación de la obra 2: ")
                obra2.adjudicar_obra()
                obra2.save()

                print("\nIngrese el inicio de la obra 2: ")
                obra2.iniciar_obra()
                obra2.save()

                print("\nIngrese el avance de la obra 2: ")
                obra2.actualizar_porcentaje_avance()
                obra2.save()

                print('desea incrementar los datos de la obra 2? ')
                print('1)si \n 2)no')
                opcionn = int(input('ingrese la opcion q decida: '))
                if opcionn == 1:
                    print("\nIngrese el plazo incrementado de la obra 2: ")
                    obra2.incrementar_plazo()
                    obra2.save()

                    print("\nIngrese la cantidad de empleados que desea agregar a la obra 2: ")
                    obra2.incrementar_mano_obra()
                    obra2.save()
                elif opcionn == 2:
                    print('no vas a incrementar los datos')
                print('\ncon la obra 2 desea rescindir o finalizarla?')
                print('1)rescindir \n 2)finalizar')
                opcion1 = int(input('elija la opcion: '))
                if opcion1 == 1:
                    obra2.rescindir_obra()
                    print('se rescindio la obra 2')
                elif opcion1 == 2:
                    obra2.finalizar_obra()
                    print('se finalizo la obra 2')
                obra2.save()

        case 4:
            GestionarObra().obtener_indicadores(Obra, tipo_obra,areas_responsables, barrios, etapas)

        case 5:
            print('saliendo del sistema')
            sqlite_db.close()
main()