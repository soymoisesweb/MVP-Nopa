from pathlib import Path
from category_manager import CategoryManager
from product_integrator import ProductIntegrator
import logging
from datetime import datetime

def setup_logging(base_dir: Path):
    """Configurar logging para el proceso completo"""
    log_dir = base_dir / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=log_dir / f'catalog_process_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    # Configuración de directorios
    BASE_DIR = Path("/Users/heydagen/Corporate Ecommerce")
    DATA_DIR = Path("/Users/heydagen/Documents/Proyectos/NOPA")
    OUTPUT_DIR = BASE_DIR / "data_analysis/output"
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Configurar logging
    setup_logging(BASE_DIR)
    logging.info("Iniciando procesamiento del catálogo")
    
    # Rutas de archivos
    CATEGORIES_CSV = DATA_DIR / "Categorias/categorias_convertidas.csv"
    PRODUCTS_CSV = DATA_DIR / "Lista de productos/CSV/Productos_Nopa.csv"
    JSON_PATH = DATA_DIR / "Lista de productos/JSON/Starcenter.json"
    
    try:
        # 1. Procesar categorías
        logging.info("Iniciando procesamiento de categorías")
        category_manager = CategoryManager(str(BASE_DIR))
        
        if not category_manager.load_categories(str(CATEGORIES_CSV)):
            raise Exception("Error al cargar categorías")
            
        # Exportar menú de categorías para WooCommerce
        woo_categories_path = OUTPUT_DIR / "woo_categories.csv"
        if not category_manager.export_category_menu(str(woo_categories_path)):
            raise Exception("Error al exportar categorías")
            
        # 2. Procesar productos
        logging.info("Iniciando procesamiento de productos")
        product_integrator = ProductIntegrator(str(BASE_DIR))
        
        # Cargar datos
        if not all([
            product_integrator.load_json_data(str(JSON_PATH)),
            product_integrator.load_csv_data(str(PRODUCTS_CSV), str(CATEGORIES_CSV))
        ]):
            raise Exception("Error al cargar datos de productos")
            
        # Generar reporte de comparación
        comparison_path = OUTPUT_DIR / "product_comparison"
        comparison_path.mkdir(exist_ok=True)
        if not product_integrator.export_comparison_report(str(comparison_path)):
            raise Exception("Error al generar reporte de comparación")
        
        logging.info("Procesamiento completado exitosamente")
        print(f"""
Proceso completado exitosamente. Archivos generados en {OUTPUT_DIR}:
1. woo_categories.csv - Menú de categorías listo para importar en WooCommerce
2. category_mapping.json - Mapeo de jerarquía de categorías
3. product_comparison.csv - Comparación detallada de productos
4. comparison_stats.json - Estadísticas de la comparación

Siguiente paso: Importar woo_categories.csv en WooCommerce usando el plugin de WebToffee
        """)
        
    except Exception as e:
        logging.error(f"Error en el procesamiento: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
