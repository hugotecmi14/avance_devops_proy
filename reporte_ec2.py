import boto3
import pandas as pd
from datetime import datetime, timedelta

# Inicializar clientes
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

# Obtener instancias
reservations = ec2.describe_instances()['Reservations']

reporte = []

for reserva in reservations:
    for instancia in reserva['Instances']:
        instance_id = instancia['InstanceId']
        estado = instancia['State']['Name']
        tipo = instancia['InstanceType']
        zona = instancia['Placement']['AvailabilityZone']
        etiquetas = instancia.get('Tags', [])

        nombre = "Desconocido"
        for etiqueta in etiquetas:
            if etiqueta['Key'] == 'Name':
                nombre = etiqueta['Value']
        
        # Obtener uso promedio de CPU (última hora)
        ahora = datetime.utcnow()
        hace_una_hora = ahora - timedelta(hours=1)

        metrica = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=hace_una_hora,
            EndTime=ahora,
            Period=3600,
            Statistics=['Average']
        )

        cpu = metrica['Datapoints'][0]['Average'] if metrica['Datapoints'] else 0.0

        reporte.append({
            'Nombre': nombre,
            'ID': instance_id,
            'Estado': estado,
            'Tipo': tipo,
            'Zona': zona,
            'CPU (%) última hora': round(cpu, 2)
        })

# Crear DataFrame
df = pd.DataFrame(reporte)

# Guardar en Excel
archivo = 'reporte_ec2.xlsx'
df.to_excel(archivo, index=False)

# Imprimir en consola
print("\n📊 Reporte de uso de instancias EC2:\n")
print(df.to_string(index=False))

print(f"\n✅ Reporte guardado en: {archivo}")

