import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from oficina.models import Oficina

def run (*args):
    if not args:
        print("Error: No se proporcionó la ruta del archivo.")
        print("Uso:./manage.py run script importar_oficinas.py --script-args--<ruta del archivo>")
        sys.exit(1)

    csv_file = args[0]

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:

            reader = csv.DictReader(f)
            oficina_a_crear = []
            for row in reader:
                nombre = row.get('nombre')
                nombre_corto = row.get('nombre_corto')
                
                if not nombre or not nombre_corto:
                    print(f"Error en la fila: {row} (nombre o nombre_corto falta un campo)")
                    continue
                try:
                    oficina = Oficina(
                        nombre=row.get('nombre'),
                        nombre_corto=row.get('nombre_corto')
                   )
                    oficina.full_clean()  # Validar el modelo antes de guardar
                    oficina_a_crear.append(oficina)
                except ValidationError as e:
                    print(f"Error de validacion en la fila {row}: Detalle: {e}")
                except Exception as e:
                    print(f"Error inesperado en la fila {row}: Detalle: {e}")

        with transaction.atomic():
            Oficina.objects.bulk_create(oficina_a_crear)
            print(f"Se han creado {len(oficina_a_crear)} oficinas creadasexitosamente.")
    except FileNotFoundError as e:
        print(f"Error: El archivo {csv_file} no existe.")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado en la importacion: {e}")