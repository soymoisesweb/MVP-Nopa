import json
import pandas as pd
import os
from datetime import datetime
import logging

def setup_logging():
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'woo_products_generator_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clean_description(desc):
    """Solo limpia espacios extras y saltos de línea innecesarios"""
    if not desc:
        return ""
    return desc.strip()

def process_images(images):
    """Procesa las URLs de las imágenes manteniendo la estructura original"""
    if not images:
        return []
    base_url = 'https://starcenter.com.uy/'
    return [base_url + img['urlImage'] for img in images]

def extract_tags_from_description(description, title):
    """Extrae etiquetas relevantes de la descripción y título"""
    if not description and not title:
        return "producto, tecnología"
        
    # Palabras clave importantes para productos tecnológicos
    tech_keywords = {
        'USB': 'USB, conectividad',
        'WIFI': 'WiFi, conectividad, redes',
        'BLUETOOTH': 'Bluetooth, wireless, conectividad',
        'HD': 'HD, alta definición',
        'WIRELESS': 'wireless, inalámbrico',
        'GAMING': 'gaming, juegos, gamer',
        'MEMORIA': 'memoria, almacenamiento',
        'AUDIO': 'audio, sonido',
        'VIDEO': 'video, multimedia',
        'IMPRESORA': 'impresora, impresión',
        'ROUTER': 'router, redes, conectividad',
        'TECLADO': 'teclado, periférico',
        'MOUSE': 'mouse, periférico',
        'CABLE': 'cable, conectividad',
        'AURICULAR': 'auriculares, audio',
    }
    
    tags = set()
    text = (description + ' ' + title).upper()
    
    # Extraer palabras clave técnicas
    for keyword, tag_group in tech_keywords.items():
        if keyword in text:
            tags.update(tag_group.split(', '))
    
    # Asegurar que siempre tengamos al menos algunas etiquetas
    if not tags:
        tags = {'tecnología', 'producto'}
    
    return ', '.join(sorted(tags))

def translate_title(title):
    """Mantiene términos técnicos en inglés pero preserva nombres de marca"""
    # Términos que no se deben traducir (marcas, modelos, etc.)
    preserve_terms = ['ARGOM', 'FELLOWES', 'HUAWEI', 'APPLE', 'BROTHER', 'SOHO', 'USB', 'WIFI', 'HD']
    
    # Mapeo de términos comunes
    translations = {
        'AURICULAR': 'Headphone',
        'AURICULARES': 'Headphones',
        'TECLADO': 'Keyboard',
        'MOUSE': 'Mouse',
        'CABLE': 'Cable',
        'CARGADOR': 'Charger',
        'ROUTER': 'Router',
        'MEMORIA': 'Memory',
        'FUENTE': 'Power Supply',
        'PAPEL': 'Paper',
        'SOBRE': 'Envelope',
        'MARCADOR': 'Marker',
        'IMPRESORA': 'Printer',
        'PARLANTE': 'Speaker',
        'PURIFICADOR': 'Air Purifier',
        'INALAMBRICO': 'Wireless',
        'MULTIFUNCION': 'Multifunction',
    }
    
    # Preservar términos específicos
    for term in preserve_terms:
        if term in title.upper():
            translations[term] = term
    
    # Traducir título
    translated = title
    for es, en in translations.items():
        translated = translated.replace(es.upper(), en)
        translated = translated.replace(es.capitalize(), en)
        translated = translated.replace(es.lower(), en)
    
    return translated

def generate_woo_products():
    logger = setup_logging()
    logger.info("Iniciando generación de productos WooCommerce")
    
    try:
        # Cargar datos del JSON
        json_path = '/Users/heydagen/Documents/Proyectos/NOPA/Lista de productos/JSON/Starcenter.json'
        logger.info(f"Cargando datos desde {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        logger.info(f"Se cargaron {len(products)} productos del archivo JSON")

        # Preparar datos para WooCommerce
        woo_products = []
        for product in products:
            # Procesar imágenes
            image_urls = process_images(product.get('image', []))
            
            # Procesar descripción y título
            description = clean_description(product.get('description', ''))
            if not description:
                description = f"Producto {product['title']} disponible en NOPA Uruguay. Consulte especificaciones y disponibilidad."
            
            # Traducir título al inglés
            english_title = translate_title(product['title'])
            
            # Generar etiquetas basadas en la descripción y título
            tags = extract_tags_from_description(description, product['title'])
            
            woo_product = {
                'Type': 'simple',
                'Title': english_title,
                'Description': description,
                'Short description': description[:150] + '...' if len(description) > 150 else description,
                'SKU': product['code'],
                'Published': 1,
                'Featured': 0,
                'Visibility in catalog': 'visible',
                'Tax status': 'taxable',
                'Tax class': '',
                'In stock?': 1 if product['stock'] > 0 else 0,
                'Stock': product['stock'],
                'Backorders allowed?': 0,
                'Sold individually?': 0,
                'Allow customer reviews?': 1,
                'Regular price': product['price'],
                'Categories': f'StarCenter_{product["category_id"]}',
                'Tags': tags,
                'Images': '|'.join(image_urls) if image_urls else '',
                'Position': 0
            }
            
            woo_products.append(woo_product)

        # Crear DataFrame y guardar como CSV
        df = pd.DataFrame(woo_products)
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'woo_products.csv')
        df.to_csv(output_file, index=False)
        
        logger.info(f"Proceso completado exitosamente")
        logger.info(f"Archivo generado: {output_file}")
        logger.info("Este archivo está listo para ser importado en WooCommerce")
        
        print(f"Proceso completado exitosamente.")
        print(f"Archivo generado: {output_file}")
        print("Este archivo está listo para ser importado en WooCommerce.")

    except Exception as e:
        logger.error(f"Error al generar archivo de productos: {str(e)}")
        print(f"Error: Error al generar archivo de productos")

if __name__ == '__main__':
    generate_woo_products()
