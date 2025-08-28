import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from oficina.models import Oficina
from persona.models import Persona

def run (*args):
    if not args:
        print("Error: No se proporcionó la ruta del archivo.")
        print("Uso:./manage.py run script importar_personas.py --script-args--<ruta del archivo>")
        sys.exit(1)

    csv_file = args[0]

    oficina_map= {oficina.nombre_corto: oficina for oficina in Oficina.objects.all()}

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            persona_a_crear = []
            for row in reader:
                nombre = row.get('nombre')
                apellido = row.get('apellido')
                edad = row.get('edad')
                oficina_nombre_corto = row.get('oficina_nombre_corto')

                if not nombre or not apellido or not edad or not oficina_nombre_corto:
                    print(f"Error en la fila: {row} (nombre, apellido, edad u oficina falta un campo)")
                    continue
                try:
                    edad_int = int(edad)
                except (ValueError, TypeError):
                    print(f"Error en la fila: {row} (edad no es un número válido)")
                    continue


                oficina_obj = None
                if oficina_nombre_corto:
                    oficina_obj = oficina_map.get(oficina_nombre_corto)

                    if not oficina_obj:
                        print(f"Error en la fila: {row} (oficina no encontrada)")
                        print(f"Se creara el registro sin oficina")
                        continue

                try:
                    persona = Persona(
                        nombre=nombre,
                        apellido=apellido,
                        edad=edad_int,
                        oficina=oficina_obj
                    )
                    persona.full_clean()  # Validar el modelo antes de guardar
                    persona_a_crear.append(persona)
                except ValidationError as e:
                    print(f"Error de validacion en la fila {row}: Detalle: {e}")
                except Exception as e:
                    print(f"Error inesperado en la fila {row}: Detalle: {e}")

        with transaction.atomic():
            Persona.objects.bulk_create(persona_a_crear)
            print(f"Se han creado {len(persona_a_crear)} personas creadas exitosamente.")
    except FileNotFoundError as e:
        print(f"Error: El archivo {csv_file} no existe.")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado en la importacion: {e}")