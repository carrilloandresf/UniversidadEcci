def main():
    while True:
        respuesta = input("¿Desea continuar Si/No? ").strip().lower()
        
        if respuesta == 'no':
            print("Programa terminado.")
            break
        elif respuesta == 'si':
            print("Continuando...")
        else:
            print("Respuesta no válida. Por favor, responda con 'Si' o 'No'.")

if __name__ == "__main__":
    main()
