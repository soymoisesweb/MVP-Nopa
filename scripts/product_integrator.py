import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime
import unidecode
import re
from typing import Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductIntegrator:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.setup_logging()
        self.categories_df = None
        self.products_df = None
        self.raw_json_data = None
        self.vectorizer = TfidfVectorizer(
            analyzer='word',
            token_pattern=r'\w+',
            ngram_range=(1, 2),
            min_df=2,
            stop_words=['de', 'la', 'el', 'y', 'en', 'con', 'para', 'por', 'los', 'las']
        )
        
    def setup_logging(self):
        """Configurar sistema de logging"""
        log_dir = self.base_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / f'product_integration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def normalize_text(self, text: str) -> str:
        """Normalizar texto para comparaciones"""
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = unidecode.unidecode(text)
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        return ' '.join(text.split())
    
    def load_json_data(self, json_path: str) -> bool:
        """Cargar datos del JSON raw del proveedor"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.raw_json_data = json.load(f)
            logging.info(f"JSON data loaded successfully from {json_path}")
            return True
        except Exception as e:
            logging.error(f"Error loading JSON data: {str(e)}")
            return False
    
    def load_csv_data(self, products_csv: str, categories_csv: str) -> bool:
        """Cargar datos de los archivos CSV"""
        try:
            self.products_df = pd.read_csv(products_csv)
            self.categories_df = pd.read_csv(categories_csv)
            logging.info("CSV data loaded successfully")
            return True
        except Exception as e:
            logging.error(f"Error loading CSV data: {str(e)}")
            return False
    
    def find_best_category_match(self, product_name: str, description: str, tags: str) -> Dict:
        """Encontrar la mejor categoría para un producto usando TF-IDF y similitud del coseno"""
        if self.categories_df is None:
            return {}
            
        # Preparar texto del producto
        product_text = ' '.join(filter(None, [
            self.normalize_text(product_name),
            self.normalize_text(description),
            self.normalize_text(tags)
        ]))
        
        # Preparar textos de categorías
        category_texts = []
        category_info = []
        
        for _, row in self.categories_df.iterrows():
            cat_text = ' '.join(filter(None, [
                self.normalize_text(row['Categoría Principal']),
                self.normalize_text(row['Subcategoría']),
                self.normalize_text(row['Sub-subcategoría'])
            ]))
            category_texts.append(cat_text)
            category_info.append({
                'categoria_principal': row['Categoría Principal'],
                'subcategoria': row['Subcategoría'],
                'sub_subcategoria': row['Sub-subcategoría']
            })
        
        # Calcular similitudes
        if not category_texts:
            return {}
            
        tfidf_matrix = self.vectorizer.fit_transform([product_text] + category_texts)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        best_match_idx = similarities[0].argmax()
        
        return {
            **category_info[best_match_idx],
            'confidence_score': similarities[0][best_match_idx]
        }
    
    def compare_products(self) -> pd.DataFrame:
        """Comparar productos entre JSON y CSV, incluyendo mapeo de categorías"""
        if self.raw_json_data is None or self.products_df is None:
            logging.error("No data loaded for comparison")
            return pd.DataFrame()
            
        comparison_results = []
        
        # Crear diccionario de productos CSV para búsqueda rápida
        csv_products = {
            self.normalize_text(row['Name']): row 
            for _, row in self.products_df.iterrows()
        }
        
        # Comparar cada producto del JSON
        for json_product in self.raw_json_data:
            normalized_name = self.normalize_text(json_product.get('name', ''))
            csv_product = csv_products.get(normalized_name)
            
            # Encontrar mejor categoría
            category_match = self.find_best_category_match(
                json_product.get('name', ''),
                json_product.get('description', ''),
                json_product.get('tags', '')
            )
            
            comparison_results.append({
                'product_name': json_product.get('name', ''),
                'in_json': True,
                'in_csv': csv_product is not None,
                'json_category': json_product.get('category', ''),
                'csv_category': csv_product['Categories'] if csv_product is not None else '',
                'mapped_category': category_match.get('categoria_principal', ''),
                'mapped_subcategory': category_match.get('subcategoria', ''),
                'mapped_sub_subcategory': category_match.get('sub_subcategoria', ''),
                'category_confidence': category_match.get('confidence_score', 0),
                'match_score': self.calculate_match_score(json_product, csv_product) if csv_product is not None else 0
            })
            
        return pd.DataFrame(comparison_results)
    
    def calculate_match_score(self, json_product: Dict, csv_product: Dict) -> float:
        """Calcular puntuación de coincidencia entre productos"""
        score = 0.0
        total_fields = 0
        
        # Comparar nombre
        if self.normalize_text(json_product.get('name', '')) == self.normalize_text(csv_product['Name']):
            score += 1
        total_fields += 1
        
        # Comparar descripción
        json_desc = self.normalize_text(json_product.get('description', ''))
        csv_desc = self.normalize_text(csv_product.get('Description', ''))
        if json_desc and csv_desc:
            similarity = len(set(json_desc.split()) & set(csv_desc.split())) / len(set(json_desc.split()) | set(csv_desc.split()))
            score += similarity
            total_fields += 1
            
        return score / total_fields if total_fields > 0 else 0
    
    def export_comparison_report(self, output_path: str) -> bool:
        """Exportar reporte de comparación"""
        comparison_df = self.compare_products()
        if comparison_df.empty:
            logging.error("No comparison data to export")
            return False
            
        try:
            # Agregar estadísticas al reporte
            stats = {
                'total_products': len(comparison_df),
                'in_both_sources': len(comparison_df[comparison_df['in_json'] & comparison_df['in_csv']]),
                'only_in_json': len(comparison_df[comparison_df['in_json'] & ~comparison_df['in_csv']]),
                'only_in_csv': len(comparison_df[~comparison_df['in_json'] & comparison_df['in_csv']]),
                'high_match_score': len(comparison_df[comparison_df['match_score'] > 0.8]),
                'high_category_confidence': len(comparison_df[comparison_df['category_confidence'] > 0.8])
            }
            
            # Guardar reporte
            report_path = Path(output_path)
            comparison_df.to_csv(report_path / 'product_comparison.csv', index=False)
            
            with open(report_path / 'comparison_stats.json', 'w') as f:
                json.dump(stats, f, indent=4)
                
            logging.info(f"Comparison report exported to {output_path}")
            return True
        except Exception as e:
            logging.error(f"Error exporting comparison report: {str(e)}")
            return False
