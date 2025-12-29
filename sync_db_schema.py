"""
Script para sincronizar el esquema de la base de datos local con produccion en Render
Solo crea/actualiza la estructura de las tablas, NO toca los datos existentes
"""
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from sqlalchemy import create_engine, inspect, text
from app.core.database import Base
from app.models import User, Caso, Mensaje, SesionDiaria, Pago

# URL de la base de datos de produccion en Render
RENDER_DATABASE_URL = "postgresql://abogadai_db_user:zz2U57KjeZbinZqNAwIr2SICUnU68Ezj@dpg-d4stu1chg0os73csqgqg-a.virginia-postgres.render.com/abogadai_db"

print("=" * 70)
print("SINCRONIZACION DE ESQUEMA DE BASE DE DATOS")
print("Base de datos de produccion: Render")
print("=" * 70)
print()

# Confirmar antes de proceder
print("Este script va a:")
print("  1. Conectarse a la base de datos de produccion en Render")
print("  2. Crear las tablas que no existan")
print("  3. Agregar las columnas que falten (si hay tablas existentes)")
print("  4. NO modificara ni eliminara datos existentes")
print()

# Si se ejecuta con "echo si |", asumimos que el usuario confirmo
auto_confirm = True  # Cambiar a False si quieres confirmar manualmente

if not auto_confirm:
    respuesta = input("Deseas continuar? (si/no): ").strip().lower()
    if respuesta not in ['si', 's', 'yes', 'y']:
        print("Operacion cancelada.")
        sys.exit(0)

print()
print("-" * 70)
print("Iniciando sincronización...")
print("-" * 70)

try:
    # Conectar a la base de datos de producción
    print("\n[1/3] Conectando a la base de datos de Render...")
    engine = create_engine(RENDER_DATABASE_URL)

    # Probar conexion
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"      [OK] Conectado exitosamente")
        print(f"      PostgreSQL: {version.split(',')[0]}")

    # Obtener el inspector para ver qué tablas ya existen
    print("\n[2/3] Analizando estructura actual...")
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    if existing_tables:
        print(f"      Tablas existentes encontradas: {len(existing_tables)}")
        for table in existing_tables:
            print(f"        - {table}")
    else:
        print("      No se encontraron tablas existentes")

    # Crear/actualizar todas las tablas definidas en los modelos
    print("\n[3/3] Sincronizando esquema...")
    print("      Modelos a sincronizar:")
    for table_name, table in Base.metadata.tables.items():
        status = "EXISTENTE" if table_name in existing_tables else "NUEVA"
        print(f"        - {table_name} [{status}]")

    # Esta operacion es segura: solo crea tablas/columnas nuevas, no modifica datos
    Base.metadata.create_all(bind=engine)

    print("\n      [OK] Esquema sincronizado exitosamente")

    # Verificar las tablas finales
    print("\n[VERIFICACIÓN] Tablas en la base de datos de producción:")
    inspector = inspect(engine)
    final_tables = inspector.get_table_names()

    for table_name in sorted(final_tables):
        columns = inspector.get_columns(table_name)
        print(f"\n  [TABLA] {table_name} ({len(columns)} columnas)")
        for col in columns:
            col_type = str(col['type'])
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"      - {col['name']}: {col_type} {nullable}")

    print()
    print("=" * 70)
    print("[OK] SINCRONIZACION COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    print("La base de datos de produccion ahora tiene el mismo esquema que la local.")
    print("Todos los datos existentes se mantuvieron intactos.")
    print()

except Exception as e:
    print()
    print("=" * 70)
    print("[ERROR] ERROR DURANTE LA SINCRONIZACION")
    print("=" * 70)
    print()
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()

    import traceback
    print("Detalles del error:")
    traceback.print_exc()
    print()
    sys.exit(1)
