import boto3

# Inicializar cliente EC2
ec2 = boto3.client('ec2', region_name='us-east-1')  

# Diccionario con los nombres y IDs de tus instancias
INSTANCIAS = {
    "ejemplo_3": "i-08dfac4c90516b039",
    "ejemplo_666": "i-097a26baf2e2ed2aa",
    "ejemplo_4": "i-0e6f9bdff2b35948d",
    "ejemplo_2": "i-0d8a1d8d3f750c2ce"
}

def listar_instancias():
    """Lista todas las instancias y muestra su estado."""
    try:
        response = ec2.describe_instances()
        print("\n📌 Lista de instancias disponibles:")
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instancia_id = instance['InstanceId']
                estado = instance['State']['Name']
                nombre = next((key for key, value in INSTANCIAS.items() if value == instancia_id), "Desconocido")
                print(f"🖥️ {nombre} (ID: {instancia_id}) - Estado: {estado}")
    except Exception as e:
        print(f"❌ Error al listar instancias: {e}")

def gestionar_instancia(instancia_nombre, accion):
    """Inicia o detiene una instancia por su nombre."""
    if instancia_nombre not in INSTANCIAS:
        print(f"⚠️ Instancia '{instancia_nombre}' no encontrada. Verifica el nombre.")
        return

    instancia_id = INSTANCIAS[instancia_nombre]

    try:
        if accion == "start":
            ec2.start_instances(InstanceIds=[instancia_id])
            print(f"✅ Instancia {instancia_nombre} iniciada.")
        elif accion == "stop":
            ec2.stop_instances(InstanceIds=[instancia_id])
            print(f"🛑 Instancia {instancia_nombre} detenida.")
        else:
            print(f"⚠️ Acción '{accion}' no válida. Usa 'start' o 'stop'.")
    except Exception as e:
        print(f"❌ Error gestionando la instancia {instancia_nombre}: {e}")

if __name__ == "__main__":
    listar_instancias()

    while True:
        instancia_nombre = input("\n👉 Ingresa el nombre de la instancia que quieres gestionar (o 'salir' para terminar): ").strip()
        if instancia_nombre.lower() == "salir":
            break
        
        accion = input("⚡ ¿Qué deseas hacer con esta instancia? (start/stop): ").strip().lower()
        gestionar_instancia(instancia_nombre, accion)

