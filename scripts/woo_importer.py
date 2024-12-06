"""
WooCommerce Product Importer
Handles direct database operations for product import and updates
"""

from db_connection import WordPressDB
import pandas as pd
from datetime import datetime
import json

class WooCommerceImporter:
    def __init__(self):
        self.db = WordPressDB()
        self.prefix = self.db.prefix

    def get_product_by_sku(self, sku):
        """Busca un producto por SKU"""
        query = f"""
        SELECT p.ID, p.post_title, pm.meta_value as sku
        FROM {self.prefix}posts p
        JOIN {self.prefix}postmeta pm ON p.ID = pm.post_id
        WHERE pm.meta_key = '_sku'
        AND pm.meta_value = %s
        AND p.post_type = 'product'
        """
        return self.db.execute_query(query, (sku,))

    def get_product_categories(self, product_id):
        """Obtiene las categorías de un producto"""
        query = f"""
        SELECT t.term_id, t.name, t.slug
        FROM {self.prefix}terms t
        JOIN {self.prefix}term_taxonomy tt ON t.term_id = tt.term_id
        JOIN {self.prefix}term_relationships tr ON tt.term_taxonomy_id = tr.term_taxonomy_id
        WHERE tr.object_id = %s
        AND tt.taxonomy = 'product_cat'
        """
        return self.db.execute_query(query, (product_id,))

    def create_product(self, data):
        """Crea un nuevo producto"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insertar el post principal del producto
        post_query = f"""
        INSERT INTO {self.prefix}posts 
        (post_author, post_date, post_date_gmt, post_content, post_title, 
         post_excerpt, post_status, comment_status, ping_status, post_name, 
         post_modified, post_modified_gmt, post_parent, post_type,
         to_ping, pinged, post_content_filtered, menu_order, post_mime_type, guid)
        VALUES (1, %s, %s, %s, %s, %s, 'publish', 'open', 'closed', %s, 
                %s, %s, 0, 'product', '', '', '', 0, '', %s)
        """
        
        # Generar GUID (URL del producto)
        guid = f"http://nopasi.local/?post_type=product&#038;p="
        
        post_data = (
            now, now, 
            data.get('description', ''),
            data['name'],
            data.get('short_description', ''),
            data['slug'],
            now, now,
            guid
        )
        
        cursor = self.db.connection.cursor()
        try:
            cursor.execute(post_query, post_data)
            self.db.connection.commit()
            product_id = cursor.lastrowid
            
            # Actualizar GUID con el ID
            guid_update = f"""
            UPDATE {self.prefix}posts 
            SET guid = CONCAT(%s, {product_id})
            WHERE ID = {product_id}
            """
            cursor.execute(guid_update, (guid,))
            self.db.connection.commit()
            
            # Insertar meta datos
            meta_data = {
                '_sku': data['sku'],
                '_price': data.get('price', ''),
                '_regular_price': data.get('regular_price', ''),
                '_stock': data.get('stock', ''),
                '_stock_status': 'instock' if int(data.get('stock', 0)) > 0 else 'outofstock',
                '_manage_stock': 'yes',
                '_visibility': 'visible',
                '_virtual': 'no',
                '_downloadable': 'no',
                '_product_version': '8.6.1'
            }
            
            for key, value in meta_data.items():
                meta_query = f"""
                INSERT INTO {self.prefix}postmeta (post_id, meta_key, meta_value)
                VALUES (%s, %s, %s)
                """
                cursor.execute(meta_query, (product_id, key, value))
            
            self.db.connection.commit()
            return product_id
            
        except Exception as e:
            self.db.connection.rollback()
            raise e
        finally:
            cursor.close()

    def update_product(self, product_id, data):
        """Actualiza un producto existente"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Actualizar post
        post_query = f"""
        UPDATE {self.prefix}posts 
        SET post_content = %s,
            post_title = %s,
            post_excerpt = %s,
            post_modified = %s,
            post_modified_gmt = %s
        WHERE ID = %s
        """
        post_data = (
            data.get('description', ''),
            data['name'],
            data.get('short_description', ''),
            now,
            now,
            product_id
        )
        self.db.execute_query(post_query, post_data)
        
        # Actualizar meta datos
        meta_data = {
            '_price': data.get('price', ''),
            '_regular_price': data.get('regular_price', ''),
            '_stock': data.get('stock', ''),
            '_stock_status': 'instock' if int(data.get('stock', 0)) > 0 else 'outofstock'
        }
        
        for key, value in meta_data.items():
            meta_query = f"""
            UPDATE {self.prefix}postmeta 
            SET meta_value = %s
            WHERE post_id = %s AND meta_key = %s
            """
            self.db.execute_query(meta_query, (value, product_id, key))
        
        return True

    def delete_product(self, product_id):
        """Elimina un producto y todos sus metadatos"""
        try:
            # Eliminar metadatos
            meta_query = f"""
            DELETE FROM {self.prefix}postmeta 
            WHERE post_id = %s
            """
            self.db.execute_query(meta_query, (product_id,))
            
            # Eliminar relaciones de términos (categorías, etiquetas, etc.)
            term_query = f"""
            DELETE FROM {self.prefix}term_relationships 
            WHERE object_id = %s
            """
            self.db.execute_query(term_query, (product_id,))
            
            # Eliminar el post del producto
            post_query = f"""
            DELETE FROM {self.prefix}posts 
            WHERE ID = %s AND post_type = 'product'
            """
            self.db.execute_query(post_query, (product_id,))
            
            return True
        except Exception as e:
            print(f"Error eliminando producto {product_id}: {str(e)}")
            return False

    def delete_all_products(self):
        """Elimina todos los productos de WooCommerce"""
        try:
            # Obtener todos los IDs de productos
            query = f"""
            SELECT ID 
            FROM {self.prefix}posts 
            WHERE post_type = 'product'
            """
            products = self.db.execute_query(query)
            
            if not products:
                print("No se encontraron productos para eliminar")
                return 0
            
            count = 0
            for product in products:
                if self.delete_product(product['ID']):
                    count += 1
                    print(f"Producto {product['ID']} eliminado correctamente")
            
            print(f"Se eliminaron {count} productos en total")
            return count
            
        except Exception as e:
            print(f"Error eliminando productos: {str(e)}")
            return 0

    def import_product(self, data):
        """Importa o actualiza un producto"""
        existing_product = self.get_product_by_sku(data['sku'])
        
        if existing_product:
            print(f"Actualizando producto existente: {data['name']}")
            return self.update_product(existing_product[0]['ID'], data)
        else:
            print(f"Creando nuevo producto: {data['name']}")
            return self.create_product(data)

    def close(self):
        """Cierra la conexión a la base de datos"""
        self.db.close()

# Función de ayuda para importar desde CSV
def import_products_from_csv(csv_file):
    """Importa productos desde un archivo CSV"""
    importer = WooCommerceImporter()
    df = pd.read_csv(csv_file)
    
    for _, row in df.iterrows():
        # Convertir la fila a diccionario y limpiar los datos
        product_data = row.to_dict()
        product_data = {k: str(v) if not pd.isna(v) else '' for k, v in product_data.items()}
        
        try:
            importer.import_product(product_data)
        except Exception as e:
            print(f"Error importando producto {product_data.get('sku', 'Unknown SKU')}: {str(e)}")
    
    importer.close()
    print("Importación completada")
