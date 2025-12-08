# -*- coding: utf-8 -*-
"""
Script de migracion para agregar columnas de analisis de IA a la tabla casos
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import os

# Fix encoding for Windows console
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

print("=" * 60)
print("MIGRACION: Agregar columnas de analisis de IA")
print("=" * 60)
print()

# Credenciales de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "abogadai_db",
    "user": "abogadai_user",
    "password": "abogadai123"
}

try:
    # Conectar a la base de datos
    print("[1/5] Conectando a la base de datos...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    print("      [OK] Conectado exitosamente")

    # Verificar si la tabla casos existe
    print("\n[2/5] Verificando tabla 'casos'...")
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'casos'
        );
    """)
    tabla_existe = cur.fetchone()[0]

    if not tabla_existe:
        print("      [ERROR] La tabla 'casos' no existe")
        print("      Por favor, ejecuta primero la aplicacion para crear las tablas")
        exit(1)

    print("      [OK] Tabla 'casos' encontrada")

    # Verificar que columnas existen
    print("\n[3/5] Verificando columnas existentes...")
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'casos'
        AND column_name IN (
            'analisis_fortaleza',
            'analisis_calidad',
            'analisis_jurisprudencia',
            'sugerencias_mejora'
        );
    """)
    columnas_existentes = [row[0] for row in cur.fetchall()]

    columnas_a_crear = []
    for col in ['analisis_fortaleza', 'analisis_calidad', 'analisis_jurisprudencia', 'sugerencias_mejora']:
        if col not in columnas_existentes:
            columnas_a_crear.append(col)
        else:
            print(f"      - Columna '{col}' ya existe")

    if not columnas_a_crear:
        print("\n      [OK] Todas las columnas ya existen, no se necesita migracion")
        cur.close()
        conn.close()
        print()
        print("=" * 60)
        print("[OK] VERIFICACION COMPLETADA")
        print("=" * 60)
        exit(0)

    # Agregar columnas faltantes
    print(f"\n[4/5] Agregando {len(columnas_a_crear)} columnas faltantes...")

    for columna in columnas_a_crear:
        try:
            sql = f"ALTER TABLE casos ADD COLUMN IF NOT EXISTS {columna} JSON;"
            cur.execute(sql)
            print(f"      [OK] Columna '{columna}' agregada")
        except Exception as e:
            print(f"      [ERROR] Error al agregar '{columna}': {e}")

    # Verificar que las columnas se crearon correctamente
    print("\n[5/5] Verificando migracion...")
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'casos'
        AND column_name IN (
            'analisis_fortaleza',
            'analisis_calidad',
            'analisis_jurisprudencia',
            'sugerencias_mejora'
        )
        ORDER BY column_name;
    """)

    columnas_finales = cur.fetchall()
    print("\n      Columnas de analisis en la tabla:")
    for col_name, col_type in columnas_finales:
        print(f"        - {col_name}: {col_type}")

    cur.close()
    conn.close()

    print()
    print("=" * 60)
    print("[OK] MIGRACION COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Ahora puedes iniciar el servidor backend:")
    print("  cd C:\\Users\\jeiso\\Desktop\\abogadai-backend")
    print("  venv\\Scripts\\activate")
    print("  uvicorn app.main:app --reload --port 8000")
    print()

except psycopg2.OperationalError as e:
    print()
    print("=" * 60)
    print("[ERROR] ERROR DE CONEXION")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("Verifica que:")
    print("  1. PostgreSQL este corriendo")
    print("  2. La base de datos 'abogadai_db' exista")
    print("  3. El usuario 'abogadai_user' tenga permisos")
    print()

except Exception as e:
    print()
    print("=" * 60)
    print("[ERROR] ERROR INESPERADO")
    print("=" * 60)
    print()
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()
    import traceback
    traceback.print_exc()

print()
input("Presiona Enter para salir...")
