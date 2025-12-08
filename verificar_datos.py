"""
Script para verificar los datos guardados en la base de datos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models.mensaje import Mensaje
from app.models.caso import Caso

def verificar_datos():
    db = SessionLocal()

    try:
        # 1. Contar mensajes totales
        total_mensajes = db.query(Mensaje).count()
        print(f"\n{'='*80}")
        print(f"📊 TOTAL DE MENSAJES EN LA BASE DE DATOS: {total_mensajes}")
        print(f"{'='*80}\n")

        # 2. Mostrar últimos 20 mensajes
        if total_mensajes > 0:
            print("📝 ÚLTIMOS 20 MENSAJES:")
            print("-" * 80)
            mensajes = db.query(Mensaje).order_by(Mensaje.timestamp.desc()).limit(20).all()
            for m in mensajes:
                texto_corto = m.texto[:70] + "..." if len(m.texto) > 70 else m.texto
                print(f"ID: {m.id:3d} | Caso: {m.caso_id:2d} | {m.remitente:10s} | {m.timestamp}")
                print(f"  → {texto_corto}")
                print()
        else:
            print("⚠️  No hay mensajes en la base de datos\n")

        # 3. Mensajes por caso
        print(f"\n{'='*80}")
        print("📋 MENSAJES POR CASO:")
        print("-" * 80)
        casos = db.query(Caso).all()
        for caso in casos:
            count = db.query(Mensaje).filter(Mensaje.caso_id == caso.id).count()
            if count > 0:
                print(f"Caso {caso.id:2d} ({caso.nombre_solicitante}): {count} mensajes")

        # 4. Mostrar últimos 3 casos con todos sus detalles
        print(f"\n{'='*80}")
        print("🗂️  ÚLTIMOS 3 CASOS (DETALLADO):")
        print("-" * 80)
        casos_recientes = db.query(Caso).order_by(Caso.id.desc()).limit(3).all()

        for caso in casos_recientes:
            print(f"\n📄 CASO ID: {caso.id}")
            print(f"   User ID: {caso.user_id}")
            print(f"   Tipo: {caso.tipo_documento}")
            print(f"   Estado: {caso.estado}")
            print(f"   Nombre: {caso.nombre_solicitante}")
            print(f"   Email: {caso.email_solicitante}")
            print(f"   Entidad accionada: {caso.entidad_accionada if caso.entidad_accionada else '❌ NO LLENADO'}")

            if caso.hechos:
                hechos_preview = caso.hechos[:100] + "..." if len(caso.hechos) > 100 else caso.hechos
                print(f"   Hechos: {hechos_preview}")
            else:
                print(f"   Hechos: ❌ NO LLENADO")

            print(f"   Derechos vulnerados: {caso.derechos_vulnerados if caso.derechos_vulnerados else '❌ NO LLENADO'}")
            print(f"   Pretensiones: {caso.pretensiones[:100] + '...' if caso.pretensiones and len(caso.pretensiones) > 100 else caso.pretensiones if caso.pretensiones else '❌ NO LLENADO'}")
            print(f"   Session ID: {caso.session_id}")
            print(f"   Room name: {caso.room_name}")
            print(f"   Inicio sesión: {caso.fecha_inicio_sesion}")
            print(f"   Fin sesión: {caso.fecha_fin_sesion if caso.fecha_fin_sesion else '⏳ En progreso'}")

            # Mostrar mensajes del caso
            mensajes_caso = db.query(Mensaje).filter(Mensaje.caso_id == caso.id).order_by(Mensaje.timestamp).all()
            print(f"   Total mensajes: {len(mensajes_caso)}")

            if len(mensajes_caso) > 0:
                print(f"\n   💬 CONVERSACIÓN COMPLETA:")
                for i, msg in enumerate(mensajes_caso, 1):
                    emisor = "👤 Usuario" if msg.remitente == "usuario" else "🤖 Asistente"
                    print(f"   {i}. {emisor}: {msg.texto}")

            print("\n" + "="*80)

        # 5. Análisis del problema
        print(f"\n{'='*80}")
        print("🔍 ANÁLISIS DEL PROBLEMA:")
        print("-" * 80)

        caso_mas_reciente = casos_recientes[0] if casos_recientes else None
        if caso_mas_reciente:
            campos_vacios = []
            if not caso_mas_reciente.entidad_accionada:
                campos_vacios.append("entidad_accionada")
            if not caso_mas_reciente.hechos:
                campos_vacios.append("hechos")
            if not caso_mas_reciente.derechos_vulnerados:
                campos_vacios.append("derechos_vulnerados")
            if not caso_mas_reciente.pretensiones:
                campos_vacios.append("pretensiones")

            if campos_vacios:
                print(f"❌ PROBLEMA DETECTADO: Los siguientes campos NO se llenaron automáticamente:")
                for campo in campos_vacios:
                    print(f"   - {campo}")

                print(f"\n💡 CAUSA:")
                print("   El sistema actual SOLO guarda los mensajes en la tabla 'mensajes',")
                print("   pero NO extrae información estructurada para llenar los campos del caso.")

                print(f"\n✅ SOLUCIÓN PROPUESTA:")
                print("   1. Al finalizar la sesión, analizar toda la conversación con IA")
                print("   2. Extraer la información estructurada (entidad, hechos, derechos, etc.)")
                print("   3. Actualizar los campos del caso automáticamente")
                print("   4. Implementar endpoint /sesiones/{id}/procesar que use OpenAI para extraer datos")
            else:
                print("✅ Todos los campos están llenos correctamente")

        print(f"{'='*80}\n")

    finally:
        db.close()

if __name__ == "__main__":
    verificar_datos()
