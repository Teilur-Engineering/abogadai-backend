"""
Migración: Agregar campos de validación de subsidiariedad al modelo Caso

Este script agrega los siguientes campos al modelo Caso:
- hubo_derecho_peticion_previo: Boolean
- detalle_derecho_peticion_previo: Text
- tiene_perjuicio_irremediable: Boolean
- es_procedente_tutela: Boolean
- razon_improcedencia: Text

Estos campos son necesarios para validar el principio de subsidiariedad
de la acción de tutela según el Art. 86 C.P. y Decreto 2591/1991
"""

import sys
import os

# Agregar el directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import text
from app.core.database import engine
from app.models.caso import Caso  # Importar para asegurar que el modelo esté registrado

def migrate():
    """Ejecuta la migracion para agregar campos de validacion de subsidiariedad"""

    print("Iniciando migracion: Agregar campos de subsidiariedad...")

    with engine.connect() as conn:
        try:
            # 1. Agregar campo hubo_derecho_peticion_previo
            print("   Agregando campo 'hubo_derecho_peticion_previo'...")
            conn.execute(text("""
                ALTER TABLE casos
                ADD COLUMN hubo_derecho_peticion_previo BOOLEAN DEFAULT FALSE
            """))
            conn.commit()
            print("   OK: Campo 'hubo_derecho_peticion_previo' agregado")

            # 2. Agregar campo detalle_derecho_peticion_previo
            print("   Agregando campo 'detalle_derecho_peticion_previo'...")
            conn.execute(text("""
                ALTER TABLE casos
                ADD COLUMN detalle_derecho_peticion_previo TEXT
            """))
            conn.commit()
            print("   OK: Campo 'detalle_derecho_peticion_previo' agregado")

            # 3. Agregar campo tiene_perjuicio_irremediable
            print("   Agregando campo 'tiene_perjuicio_irremediable'...")
            conn.execute(text("""
                ALTER TABLE casos
                ADD COLUMN tiene_perjuicio_irremediable BOOLEAN DEFAULT FALSE
            """))
            conn.commit()
            print("   OK: Campo 'tiene_perjuicio_irremediable' agregado")

            # 4. Agregar campo es_procedente_tutela
            print("   Agregando campo 'es_procedente_tutela'...")
            conn.execute(text("""
                ALTER TABLE casos
                ADD COLUMN es_procedente_tutela BOOLEAN DEFAULT FALSE
            """))
            conn.commit()
            print("   OK: Campo 'es_procedente_tutela' agregado")

            # 5. Agregar campo razon_improcedencia
            print("   Agregando campo 'razon_improcedencia'...")
            conn.execute(text("""
                ALTER TABLE casos
                ADD COLUMN razon_improcedencia TEXT
            """))
            conn.commit()
            print("   OK: Campo 'razon_improcedencia' agregado")

            print("EXITO: Migracion completada exitosamente")
            print("Los campos de validacion de subsidiariedad han sido agregados al modelo Caso")

        except Exception as e:
            print(f"ERROR durante la migracion: {str(e)}")
            print(f"   Tipo de error: {type(e).__name__}")
            conn.rollback()
            raise

if __name__ == "__main__":
    migrate()
