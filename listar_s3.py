import boto3

# Inicializar el cliente de S3
s3 = boto3.client('s3')

def listar_buckets_y_objetos():
    try:
        # Obtener todos los buckets
        respuesta = s3.list_buckets()
        buckets = respuesta['Buckets']

        if not buckets:
            print("No se encontraron buckets en tu cuenta.")
            return

        print("📦 Buckets encontrados:\n")

        for bucket in buckets:
            nombre_bucket = bucket['Name']
            print(f"🔹 Bucket: {nombre_bucket}")
            print("   Objetos:")

            # Listar objetos dentro del bucket
            try:
                objetos = s3.list_objects_v2(Bucket=nombre_bucket)
                if 'Contents' in objetos:
                    for obj in objetos['Contents']:
                        print(f"     - {obj['Key']} ({obj['Size']} bytes)")
                else:
                    print("     (Vacío)")
            except Exception as e:
                print(f"     ⚠️ Error accediendo a objetos: {e}")

            print("")  # Separador visual

    except Exception as e:
        print(f"❌ Error al listar buckets: {e}")

if __name__ == "__main__":
    listar_buckets_y_objetos()

