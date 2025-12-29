"""
Script para verificar el esquema final de la base de datos
"""
from sqlalchemy import create_engine, inspect

# URL de la base de datos de produccion en Render
RENDER_DATABASE_URL = "postgresql://abogadai_db_user:zz2U57KjeZbinZqNAwIr2SICUnU68Ezj@dpg-d4stu1chg0os73csqgqg-a.virginia-postgres.render.com/abogadai_db"

print("=" * 70)
print("VERIFICACION FINAL DEL ESQUEMA DE BASE DE DATOS")
print("=" * 70)
print()

try:
    # Conectar a la base de datos de producción
    print("Conectando a la base de datos de Render...")
    engine = create_engine(RENDER_DATABASE_URL)

    print("[OK] Conectado exitosamente\n")

    # Verificar las tablas
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print(f"Total de tablas: {len(tables)}\n")

    for table_name in sorted(tables):
        columns = inspector.get_columns(table_name)
        print(f"[TABLA] {table_name} ({len(columns)} columnas)")
        for col in sorted(columns, key=lambda x: x['name']):
            col_type = str(col['type'])
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = f" DEFAULT {col.get('default', '')}" if col.get('default') else ""
            print(f"  - {col['name']}: {col_type} {nullable}{default}")
        print()

    print("=" * 70)
    print("[OK] VERIFICACION COMPLETADA")
    print("=" * 70)

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
