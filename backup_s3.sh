#!/bin/bash

BUCKET_NAME="act2devops" 
DIR_ORIGEN="resp_ec2"
BACKUP_FILE="backup_$(date +%F).tar.gz"
LOG_FILE="backup.log"

if [ ! -d "$DIR_ORIGEN" ]; then
    echo "$(date): ERROR - El directorio $DIR_ORIGEN no existe." >> $LOG_FILE
    exit 1
fi

echo "$(date): Iniciando respaldo..." >> $LOG_FILE
tar -czf $BACKUP_FILE $DIR_ORIGEN >> $LOG_FILE 2>&1

if aws s3 cp $BACKUP_FILE s3://$BUCKET_NAME/ >> $LOG_FILE 2>&1; then
    echo "$(date): Respaldo subido exitosamente a S3." >> $LOG_FILE
else
    echo "$(date): ERROR al subir respaldo a S3." >> $LOG_FILE
fi

# Esto es un cambio de prueba para backup S3
