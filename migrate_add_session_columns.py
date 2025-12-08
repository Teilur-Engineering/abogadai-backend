"""
Script de migración para agregar columnas de sesión a la tabla casos
y crear la tabla mensajes
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.config import settings

def migrate():
    print("🔧 Iniciando migración...")
    print(f"📁 Base de datos: {settings.DATABASE_URL}")

    # Crear engine
    engine = create_engine(settings.DATABASE_URL)

    try:
        with engine.connect() as conn:
            # 1. Agregar columnas a la tabla casos
            print("\n📝 Agregando columnas de sesión a tabla 'casos'...")

            columnas_agregar = [
                ("session_id", "VARCHAR(100)"),
                ("room_name", "VARCHAR(100)"),
                ("fecha_inicio_sesion", "TIMESTAMP"),
                ("fecha_fin_sesion", "TIMESTAMP")
            ]

            for columna, tipo in columnas_agregar:
                try:
                    conn.execute(text(f"ALTER TABLE casos ADD COLUMN IF NOT EXISTS {columna} {tipo}"))
                    conn.commit()
                    print(f"   ✅ Columna '{columna}' agregada")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower() or "ya existe" in str(e).lower():
                        print(f"   ⏭️  Columna '{columna}' ya existe, saltando...")
                    else:
                        print(f"   ❌ Error en columna '{columna}': {e}")

            # 2. Crear índices
            print("\n📑 Creando índices...")
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_casos_session_id ON casos(session_id)"))
                conn.commit()
                print("   ✅ Índice 'idx_casos_session_id' creado")
            except Exception as e:
                print(f"   ⏭️  Índice ya existe o error: {e}")

            # 3. Crear tabla mensajes
            print("\n📝 Creando tabla 'mensajes'...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS mensajes (
                        id SERIAL PRIMARY KEY,
                        caso_id INTEGER NOT NULL,
                        remitente VARCHAR(50) NOT NULL,
                        texto TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        duracion_audio INTEGER,
                        confianza INTEGER,
                        FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
                    )
                """))
                conn.commit()
                print("   ✅ Tabla 'mensajes' creada")

                # Crear índices para mensajes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_mensajes_caso_id ON mensajes(caso_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_mensajes_timestamp ON mensajes(timestamp)"))
                conn.commit()
                print("   ✅ Índices de 'mensajes' creados")

            except OperationalError as e:
                if "already exists" in str(e).lower():
                    print("   ⏭️  Tabla 'mensajes' ya existe, saltando...")
                else:
                    print(f"   ❌ Error creando tabla: {e}")

            print("\n✅ Migración completada exitosamente!")
            print("\n📊 Resumen:")
            print("   - Tabla 'casos': 4 columnas nuevas agregadas")
            print("   - Tabla 'mensajes': Creada con índices")
            print("   - Sistema listo para sesiones con avatar\n")

    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
