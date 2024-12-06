import pandas as pd
import unidecode
import re
from pathlib import Path
import logging
from datetime import datetime
import json

class CategoryManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.setup_logging()
        self.categories_df = None
        self.unique_paths = set()
        
    def setup_logging(self):
        """Configurar sistema de logging"""
        log_dir = self.base_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / f'category_manager_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def clean_category_name(self, name: str) -> str:
        """Limpia el nombre de la categoría eliminando caracteres especiales y espacios innecesarios"""
        # Eliminar asteriscos y espacios extras
        name = name.replace('*', '').strip()
        # Eliminar espacios múltiples
        name = ' '.join(name.split())
        return name

    def generate_slug(self, path_parts: list) -> str:
        """Genera un slug SEO-friendly para la categoría"""
        # Unir las partes del path y limpiar
        full_path = '->'.join(path_parts) if isinstance(path_parts, list) else path_parts
        parts = [p.strip() for p in full_path.split('->')]
        
        # Generar slug para cada parte
        slug_parts = []
        for part in parts:
            # Limpiar el nombre primero
            clean_name = self.clean_category_name(part)
            # Convertir a minúsculas y quitar acentos
            text = unidecode.unidecode(clean_name.lower())
            # Reemplazar caracteres no alfanuméricos con guiones
            text = re.sub(r'[^a-z0-9]+', '-', text)
            # Eliminar guiones al inicio y final
            text = text.strip('-')
            slug_parts.append(text)
            
        return '-'.join(slug_parts)

    def load_categories(self, csv_path: str) -> bool:
        """Cargar categorías desde CSV"""
        try:
            self.categories_df = pd.read_csv(csv_path)
            
            # Extraer paths únicos
            for _, row in self.categories_df.iterrows():
                path_parts = []
                if pd.notna(row['Categoría Principal']):
                    path_parts.append(row['Categoría Principal'])
                if pd.notna(row['Subcategoría']):
                    path_parts.append(row['Subcategoría'])
                if pd.notna(row['Sub-subcategoría']):
                    path_parts.append(row['Sub-subcategoría'])
                
                if path_parts:
                    self.unique_paths.add('->'.join(path_parts))
            
            logging.info(f"Categorías cargadas exitosamente: {len(self.unique_paths)} paths únicos")
            return True
        except Exception as e:
            logging.error(f"Error al cargar categorías: {str(e)}")
            return False

    def generate_category_menu(self) -> pd.DataFrame:
        """Genera el menú de categorías para WooCommerce"""
        categories = []
        id_counter = 1
        parent_map = {}

        for path in self.unique_paths:
            parts = [p.strip() for p in path.split('->')]
            current_parent = 0
            
            for i, part in enumerate(parts):
                cleaned_name = self.clean_category_name(part)
                if cleaned_name not in parent_map:
                    slug = self.generate_slug(path[:i+1])
                    categories.append({
                        'ID': id_counter,
                        'Name': cleaned_name,
                        'Slug': slug,
                        'Parent': current_parent,
                        'Description': f'Productos de {cleaned_name}',
                        'Display type': 'default',
                        'Image': '',
                        'Menu order': 0,
                        'Count': 0
                    })
                    parent_map[cleaned_name] = id_counter
                    current_parent = id_counter
                    id_counter += 1
                else:
                    current_parent = parent_map[cleaned_name]

        return pd.DataFrame(categories)

    def export_category_menu(self, output_path: str) -> bool:
        """Exportar menú de categorías a CSV"""
        try:
            # Generar menú
            menu_df = self.generate_category_menu()
            
            # Exportar a CSV
            menu_df.to_csv(output_path, index=False)
            
            # Exportar mapeo de categorías para referencia
            category_mapping = {
                row['Name']: {
                    'id': row['ID'],
                    'slug': row['Slug'],
                    'parent': row['Parent']
                }
                for _, row in menu_df.iterrows()
            }
            
            mapping_path = str(Path(output_path).parent / 'category_mapping.json')
            with open(mapping_path, 'w', encoding='utf-8') as f:
                json.dump(category_mapping, f, indent=4, ensure_ascii=False)
            
            logging.info(f"Menú de categorías exportado exitosamente a {output_path}")
            return True
        except Exception as e:
            logging.error(f"Error al exportar menú de categorías: {str(e)}")
            return False

if __name__ == "__main__":
    # Configuración de rutas
    BASE_DIR = Path("/Users/heydagen/Corporate Ecommerce")
    CATEGORIES_CSV = "/Users/heydagen/Documents/Proyectos/NOPA/Categorias/categorias_convertidas.csv"
    OUTPUT_DIR = BASE_DIR / "data_analysis/output"
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Crear instancia y procesar categorías
    manager = CategoryManager(str(BASE_DIR))
    
    if manager.load_categories(CATEGORIES_CSV):
        # Exportar menú de categorías para WooCommerce
        manager.export_category_menu(str(OUTPUT_DIR / "woo_categories.csv"))
