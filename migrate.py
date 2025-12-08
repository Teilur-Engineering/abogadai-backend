# -*- coding: utf-8 -*-
"""
Script de migracion para agregar columnas de analisis de IA a la tabla casos
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("Migracion: Agregar columnas de analisis de IA")
print("=" * 60)

# Credenciales de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "abogadai_db",
    "user": "abogadai_user",
    "password": "abogadai123"
}

try:
    print("[1/5] Conectando a la base de datos...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    print("[OK] Conectado")

    print("[2/5] Verificando tabla 'casos'...")
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'casos'
        );
    """)
    tabla_existe = cur.fetchone()[0]

    if not tabla_existe:
        print("[ERROR] La tabla 'casos' no existe")
        exit(1)

    print("[OK] Tabla encontrada")

    print("[3/5] Verificando columnas existentes...")
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
            print(f"  - Columna '{col}' ya existe")

    if not columnas_a_crear:
        print("[OK] Todas las columnas ya existen")
        cur.close()
        conn.close()
        exit(0)

    print(f"[4/5] Agregando {len(columnas_a_crear)} columnas...")
    for columna in columnas_a_crear:
        try:
            sql = f"ALTER TABLE casos ADD COLUMN IF NOT EXISTS {columna} JSON;"
            cur.execute(sql)
            print(f"  [OK] '{columna}' agregada")
        except Exception as e:
            print(f"  [ERROR] '{columna}': {e}")

    print("[5/5] Verificando migracion...")
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
    print("\nColumnas de analisis:")
    for col_name, col_type in columnas_finales:
        print(f"  - {col_name}: {col_type}")

    cur.close()
    conn.close()

    print("\n[OK] MIGRACION COMPLETADA")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
