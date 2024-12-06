"""
Script para eliminar todos los productos de WooCommerce
"""

from woo_importer import WooCommerceImporter

def main():
    importer = WooCommerceImporter()
    try:
        print("Iniciando eliminación de productos...")
        # Eliminar todos los productos
        count = importer.delete_all_products()
        print(f"\nOperación completada. {count} productos eliminados.")
    finally:
        importer.close()

if __name__ == '__main__':
    main()
