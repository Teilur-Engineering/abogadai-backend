"""
Script para otorgar permisos de administrador a usuarios especificos
"""
from sqlalchemy import create_engine, text
import sys

# URL de la base de datos de produccion en Render
RENDER_DATABASE_URL = "postgresql://abogadai_db_user:zz2U57KjeZbinZqNAwIr2SICUnU68Ezj@dpg-d4stu1chg0os73csqgqg-a.virginia-postgres.render.com/abogadai_db"

# Correos a los que se les otorgara permisos de admin
ADMIN_EMAILS = [
    "valdesmelanie1@gmail.com",
    "jeison@teilur.com"
]

print("=" * 80)
print("OTORGAR PERMISOS DE ADMINISTRADOR")
print("=" * 80)
print()

print("Se otorgaran permisos de administrador a los siguientes correos:")
for email in ADMIN_EMAILS:
    print(f"  - {email}")
print()

try:
    # Conectar a la base de datos de produccion
    print("Conectando a la base de datos de Render...")
    engine = create_engine(RENDER_DATABASE_URL)

    with engine.connect() as conn:
        print("[OK] Conectado exitosamente\n")

        # Verificar que los usuarios existen
        print("Verificando usuarios...")
        for email in ADMIN_EMAILS:
            query = text("SELECT id, nombre, apellido, is_admin FROM users WHERE email = :email")
            result = conn.execute(query, {"email": email})
            user = result.fetchone()

            if user:
                status = "YA ES ADMIN" if user.is_admin else "NO ES ADMIN"
                print(f"  [OK] {email} - {user.nombre} {user.apellido} - {status}")
            else:
                print(f"  [ERROR] {email} - NO ENCONTRADO")
                print("\nAbortando operacion...")
                sys.exit(1)

        print()
        print("Actualizando permisos de administrador...")

        # Actualizar permisos
        for email in ADMIN_EMAILS:
            query = text("UPDATE users SET is_admin = true WHERE email = :email")
            conn.execute(query, {"email": email})
            print(f"  [OK] Permisos otorgados a: {email}")

        conn.commit()

        print("\nVerificando cambios...")
        # Verificar que los cambios se aplicaron
        query = text("""
            SELECT id, email, nombre, apellido, is_admin
            FROM users
            WHERE email = ANY(:emails)
            ORDER BY id
        """)
        result = conn.execute(query, {"emails": ADMIN_EMAILS})
        users = result.fetchall()

        print()
        print("-" * 80)
        for user in users:
            status = "ADMIN" if user.is_admin else "NO ADMIN"
            print(f"ID: {user.id} | {user.email} | {user.nombre} {user.apellido} | {status}")
        print("-" * 80)

    print()
    print("=" * 80)
    print("[OK] PERMISOS DE ADMINISTRADOR OTORGADOS EXITOSAMENTE")
    print("=" * 80)
    print()

except Exception as e:
    print()
    print("=" * 80)
    print("[ERROR] ERROR AL OTORGAR PERMISOS")
    print("=" * 80)
    print()
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()

    import traceback
    print("Detalles del error:")
    traceback.print_exc()
    print()
    sys.exit(1)
