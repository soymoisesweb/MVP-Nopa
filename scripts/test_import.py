"""
Test script for WooCommerce product import
"""

from woo_importer import WooCommerceImporter

def test_single_product():
    importer = WooCommerceImporter()
    
    # Datos de prueba para un producto
    test_product = {
        'sku': 'TEST-001',
        'name': 'Producto de Prueba',
        'slug': 'producto-de-prueba',
        'description': 'Esta es una descripción de prueba',
        'short_description': 'Descripción corta',
        'price': '99.99',
        'regular_price': '129.99',
        'stock': '10'
    }
    
    try:
        result = importer.import_product(test_product)
        print(f"Resultado de la importación: {result}")
    except Exception as e:
        print(f"Error durante la importación: {str(e)}")
    finally:
        importer.close()

if __name__ == '__main__':
    test_single_product()
