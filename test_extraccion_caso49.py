"""
Script para probar la extracción de datos del caso 49 directamente
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.caso import Caso
from app.models.mensaje import Mensaje
from app.services import openai_service
import json

def test_extraccion_caso_49():
    db = SessionLocal()
    try:
        print("=" * 80)
        print("TEST DE EXTRACCION - CASO 49")
        print("=" * 80)

        # Obtener el caso 49
        caso = db.query(Caso).filter(Caso.id == 49).first()

        if not caso:
            print("\n[ERROR] No se encontro el caso 49")
            return

        print(f"\n[OK] Caso 49 encontrado")
        print(f"  User ID: {caso.user_id}")
        print(f"  Estado: {caso.estado}")

        # Obtener mensajes
        mensajes = db.query(Mensaje).filter(
            Mensaje.caso_id == 49
        ).order_by(Mensaje.timestamp.asc()).all()

        print(f"\n[OK] Mensajes encontrados: {len(mensajes)}")

        if not mensajes:
            print("\n[ERROR] No hay mensajes")
            return

        # Mostrar algunos mensajes
        print("\n" + "=" * 80)
        print("MENSAJES DE LA CONVERSACION (primeros 5):")
        print("=" * 80)
        for i, msg in enumerate(mensajes[:5], 1):
            print(f"\n[{i}] {msg.remitente.upper()}:")
            print(f"    {msg.texto[:100]}{'...' if len(msg.texto) > 100 else ''}")

        # Convertir mensajes a formato para el servicio de IA
        mensajes_formateados = [
            {
                "remitente": msg.remitente,
                "texto": msg.texto,
                "timestamp": str(msg.timestamp)
            }
            for msg in mensajes
        ]

        print("\n" + "=" * 80)
        print("LLAMANDO A openai_service.extraer_datos_conversacion()...")
        print("=" * 80)

        # Extraer datos con IA
        try:
            datos_extraidos = openai_service.extraer_datos_conversacion(mensajes_formateados)

            print("\n" + "=" * 80)
            print("DATOS EXTRAIDOS - JSON COMPLETO:")
            print("=" * 80)
            print(json.dumps(datos_extraidos, indent=2, ensure_ascii=False))

            print("\n" + "=" * 80)
            print("RESUMEN DE CAMPOS EXTRAIDOS:")
            print("=" * 80)

            campos = [
                ('tipo_documento', 'Tipo documento'),
                ('razon_tipo_documento', 'Razon tipo documento'),
                ('nombre_solicitante', 'Nombre solicitante'),
                ('identificacion_solicitante', 'Identificacion'),
                ('direccion_solicitante', 'Direccion'),
                ('telefono_solicitante', 'Telefono'),
                ('email_solicitante', 'Email'),
                ('actua_en_representacion', 'Actua en representacion'),
                ('entidad_accionada', 'Entidad'),
                ('direccion_entidad', 'Direccion entidad'),
                ('hechos', 'Hechos'),
                ('derechos_vulnerados', 'Derechos vulnerados'),
                ('pretensiones', 'Pretensiones'),
                ('fundamentos_derecho', 'Fundamentos'),
                ('pruebas', 'Pruebas'),
                ('hubo_derecho_peticion_previo', 'Derecho peticion previo'),
            ]

            for campo, label in campos:
                valor = datos_extraidos.get(campo, '')
                if isinstance(valor, bool):
                    estado = '[SI]' if valor else '[NO]'
                    print(f"  {label:30} {estado}")
                elif isinstance(valor, str):
                    if valor and valor.strip():
                        preview = valor[:60] + '...' if len(valor) > 60 else valor
                        print(f"  {label:30} [OK] {preview}")
                    else:
                        print(f"  {label:30} [VACIO]")
                else:
                    print(f"  {label:30} {valor}")

            print("\n" + "=" * 80)
            print("COMPARACION CON LO QUE ESTA EN LA BASE DE DATOS:")
            print("=" * 80)
            print(f"\nExtraccion IA -> Base de Datos")
            print(f"  Nombre:  '{datos_extraidos.get('nombre_solicitante', '')}' -> '{caso.nombre_solicitante}'")
            print(f"  Cedula:  '{datos_extraidos.get('identificacion_solicitante', '')}' -> '{caso.identificacion_solicitante}'")
            print(f"  Direccion: '{datos_extraidos.get('direccion_solicitante', '')}' -> '{caso.direccion_solicitante}'")
            print(f"  Telefono:  '{datos_extraidos.get('telefono_solicitante', '')}' -> '{caso.telefono_solicitante}'")
            print(f"  Email:  '{datos_extraidos.get('email_solicitante', '')}' -> '{caso.email_solicitante}'")
            print(f"  Dir Entidad: '{datos_extraidos.get('direccion_entidad', '')}' -> '{caso.direccion_entidad}'")
            print(f"  Pruebas: '{datos_extraidos.get('pruebas', '')[:50]}...' -> '{caso.pruebas[:50] if caso.pruebas else ''}...'")

        except Exception as e:
            print(f"\n[ERROR] Error al extraer datos: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"\n[ERROR] Error general: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_extraccion_caso_49()
