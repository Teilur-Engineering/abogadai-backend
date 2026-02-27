"""
Script para agregar columnas faltantes a las tablas existentes
"""
import sys
from sqlalchemy import create_engine, inspect, text

# URL de la base de datos de produccion en Render
RENDER_DATABASE_URL = "postgresql://abogadai_db_user:zz2U57KjeZbinZqNAwIr2SICUnU68Ezj@dpg-d4stu1chg0os73csqgqg-a.virginia-postgres.render.com/abogadai_db"

print("=" * 70)
print("AGREGAR COLUMNAS FALTANTES A TABLAS EXISTENTES")
print("=" * 70)
print()

try:
    # Conectar a la base de datos de producción
    print("[1/2] Conectando a la base de datos de Render...")
    engine = create_engine(RENDER_DATABASE_URL)

    with engine.connect() as conn:
        print("      [OK] Conectado exitosamente")

        # Obtener columnas actuales de cada tabla
        inspector = inspect(engine)

        # Columnas que deberían existir en la tabla users
        print("\n[2/2] Verificando y agregando columnas faltantes...")

        # TABLA USERS
        print("\n  Verificando tabla 'users'...")
        users_columns = [col['name'] for col in inspector.get_columns('users')]

        columnas_users = [
            ("nivel_usuario", "INTEGER DEFAULT 0 NOT NULL"),
            ("pagos_ultimo_mes", "INTEGER DEFAULT 0 NOT NULL"),
            ("ultimo_recalculo_nivel", "TIMESTAMP NULL"),
            ("sesiones_extra_hoy", "INTEGER DEFAULT 0 NOT NULL"),
            ("reset_password_token", "VARCHAR(255) NULL"),
            ("reset_token_expires", "TIMESTAMP NULL"),
        ]

        for col_name, col_def in columnas_users:
            if col_name not in users_columns:
                print(f"    Agregando columna '{col_name}'...")
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"))
                conn.commit()
                print(f"      [OK] Columna '{col_name}' agregada")
            else:
                print(f"    Columna '{col_name}' ya existe")

        # TABLA CASOS
        print("\n  Verificando tabla 'casos'...")
        casos_columns = [col['name'] for col in inspector.get_columns('casos')]

        columnas_casos = [
            ("fecha_vencimiento", "TIMESTAMP NULL"),
            ("reembolso_solicitado", "BOOLEAN DEFAULT FALSE NOT NULL"),
            ("fecha_solicitud_reembolso", "TIMESTAMP NULL"),
            ("motivo_rechazo", "TEXT NULL"),
            ("evidencia_rechazo_url", "VARCHAR(500) NULL"),
            ("fecha_reembolso", "TIMESTAMP NULL"),
            ("comentario_admin_reembolso", "TEXT NULL"),
            ("historial_reembolsos", "JSON NULL"),
            ("visto_por_usuario", "BOOLEAN DEFAULT TRUE NOT NULL"),
        ]

        for col_name, col_def in columnas_casos:
            if col_name not in casos_columns:
                print(f"    Agregando columna '{col_name}'...")
                conn.execute(text(f"ALTER TABLE casos ADD COLUMN {col_name} {col_def}"))
                conn.commit()
                print(f"      [OK] Columna '{col_name}' agregada")
            else:
                print(f"    Columna '{col_name}' ya existe")

    print()
    print("=" * 70)
    print("[OK] COLUMNAS AGREGADAS EXITOSAMENTE")
    print("=" * 70)
    print()
    print("Todas las columnas faltantes han sido agregadas.")
    print("Los datos existentes se mantuvieron intactos.")
    print()

except Exception as e:
    print()
    print("=" * 70)
    print("[ERROR] ERROR AL AGREGAR COLUMNAS")
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
