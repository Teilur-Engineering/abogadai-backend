"""
Script temporal para revisar los datos de la sesión 45
"""
import sys
import os
from sqlalchemy.orm import Session

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.caso import Caso
from app.models.mensaje import Mensaje
import json

def revisar_session_45(caso_id=45):
    db = SessionLocal()
    try:
        # Buscar el caso con id especificado
        print("=" * 80)
        print(f"BUSCANDO CASO {caso_id}...")
        print("=" * 80)

        # Intentar por ID
        caso = db.query(Caso).filter(Caso.id == caso_id).first()

        if not caso:
            print("\n[ERROR] No se encontro ningun caso con ID 45 o session_id '45'")

            # Mostrar últimos casos creados
            print("\nUltimos 10 casos creados:")
            ultimos_casos = db.query(Caso).order_by(Caso.created_at.desc()).limit(10).all()
            for c in ultimos_casos:
                print(f"  - ID: {c.id}, Session ID: {c.session_id}, Nombre: {c.nombre_solicitante}, Creado: {c.created_at}")

            return

        print(f"\n[OK] Caso encontrado:")
        print(f"  - ID: {caso.id}")
        print(f"  - Session ID: {caso.session_id}")
        print(f"  - User ID: {caso.user_id}")
        print(f"  - Tipo documento: {caso.tipo_documento}")
        print(f"  - Estado: {caso.estado}")

        print("\n" + "=" * 80)
        print("DATOS DEL SOLICITANTE")
        print("=" * 80)
        print(f"Nombre: {caso.nombre_solicitante}")
        print(f"Identificación: {caso.identificacion_solicitante}")
        print(f"Dirección: {caso.direccion_solicitante}")
        print(f"Teléfono: {caso.telefono_solicitante}")
        print(f"Email: {caso.email_solicitante}")

        print("\n" + "=" * 80)
        print("REPRESENTACIÓN")
        print("=" * 80)
        print(f"Actúa en representación: {caso.actua_en_representacion}")
        print(f"Nombre representado: {caso.nombre_representado}")
        print(f"Identificación representado: {caso.identificacion_representado}")
        print(f"Relación: {caso.relacion_representado}")
        print(f"Tipo representado: {caso.tipo_representado}")

        print("\n" + "=" * 80)
        print("ENTIDAD ACCIONADA")
        print("=" * 80)
        print(f"Entidad: {caso.entidad_accionada}")
        print(f"Dirección: {caso.direccion_entidad}")
        print(f"Representante legal: {caso.representante_legal}")

        print("\n" + "=" * 80)
        print("CONTENIDO DEL CASO")
        print("=" * 80)
        print(f"\nHECHOS:")
        print(caso.hechos if caso.hechos else "(vacío)")
        print(f"\nDERECHOS VULNERADOS:")
        print(caso.derechos_vulnerados if caso.derechos_vulnerados else "(vacío)")
        print(f"\nPRETENSIONES:")
        print(caso.pretensiones if caso.pretensiones else "(vacío)")
        print(f"\nFUNDAMENTOS DE DERECHO:")
        print(caso.fundamentos_derecho if caso.fundamentos_derecho else "(vacío)")
        print(f"\nPRUEBAS:")
        print(caso.pruebas if caso.pruebas else "(vacío)")

        # Revisar mensajes de la conversación
        print("\n" + "=" * 80)
        print("MENSAJES DE LA CONVERSACIÓN")
        print("=" * 80)
        mensajes = db.query(Mensaje).filter(Mensaje.caso_id == caso.id).order_by(Mensaje.timestamp).all()
        print(f"\nTotal de mensajes: {len(mensajes)}")

        for i, msg in enumerate(mensajes, 1):
            print(f"\n[{i}] {msg.remitente.upper()} ({msg.timestamp}):")
            print(f"    {msg.texto[:200]}{'...' if len(msg.texto) > 200 else ''}")

        # Revisar análisis
        print("\n" + "=" * 80)
        print("ANÁLISIS")
        print("=" * 80)

        if caso.analisis_fortaleza:
            print("\nAnalisis de Fortaleza:")
            print(json.dumps(caso.analisis_fortaleza, indent=2, ensure_ascii=False))
        else:
            print("\nAnalisis de Fortaleza: (no disponible)")

        print("\n" + "=" * 80)
        print(f"Creado: {caso.created_at}")
        print(f"Actualizado: {caso.updated_at}")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    caso_id = int(sys.argv[1]) if len(sys.argv) > 1 else 45
    revisar_session_45(caso_id)
