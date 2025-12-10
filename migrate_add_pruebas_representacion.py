"""
Script de migración para agregar columnas de pruebas y representación de terceros
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.config import settings

def migrate():
    print("Iniciando migracion...")
    print(f"Base de datos: {settings.DATABASE_URL}")

    # Crear engine
    engine = create_engine(settings.DATABASE_URL)

    try:
        with engine.connect() as conn:
            print("\nAgregando nuevas columnas a tabla 'casos'...")

            columnas_agregar = [
                ("pruebas", "TEXT"),
                ("actua_en_representacion", "BOOLEAN DEFAULT FALSE"),
                ("nombre_representado", "VARCHAR(200)"),
                ("identificacion_representado", "VARCHAR(50)"),
                ("relacion_representado", "VARCHAR(100)"),
                ("tipo_representado", "VARCHAR(100)"),
            ]

            for columna, tipo in columnas_agregar:
                try:
                    conn.execute(text(f"ALTER TABLE casos ADD COLUMN IF NOT EXISTS {columna} {tipo}"))
                    conn.commit()
                    print(f"   [OK] Columna '{columna}' agregada")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower() or "ya existe" in str(e).lower():
                        print(f"   [SKIP] Columna '{columna}' ya existe, saltando...")
                    else:
                        print(f"   [ERROR] Error en columna '{columna}': {e}")

            print("\n[OK] Migracion completada exitosamente!")
            print("\nResumen:")
            print("   - Columna 'pruebas': Agregada para documentos y pruebas anexas")
            print("   - Columnas de representacion: Agregadas para casos con representante")
            print("   - Sistema actualizado con nuevos campos\n")

    except Exception as e:
        print(f"\n[ERROR] Error durante la migracion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
