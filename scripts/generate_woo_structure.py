import json
import pandas as pd
import os

def generate_category_structure():
    """
    Genera la estructura jerárquica de categorías basada en categorias_convertidas.csv
    """
    # Leer el archivo CSV de categorías convertidas
    csv_path = os.path.join('output', 'categorias_convertidas.csv')
    df = pd.read_csv(csv_path)
    
    # Generar CSV de categorías
    cat_rows = []
    
    # Procesar categorías principales
    for main_cat in df['Categoría Principal'].unique():
        cat_rows.append({
            'Category ID': f'cat_{main_cat.lower().replace(" ", "_")}',
            'Category Name': main_cat,
            'Category Slug': main_cat.lower().replace(" ", "-").replace("(", "").replace(")", ""),
            'Parent Category': '',
            'Description': f'Productos de {main_cat}'
        })
        
        # Procesar subcategorías
        sub_cats = df[df['Categoría Principal'] == main_cat]['Subcategoría'].unique()
        for sub_cat in sub_cats:
            # Eliminar números del inicio (ej: "8.1. ")
            sub_cat_clean = sub_cat.split('. ')[-1] if '. ' in sub_cat else sub_cat
            cat_rows.append({
                'Category ID': f'cat_{main_cat.lower().replace(" ", "_")}_{sub_cat_clean.lower().replace(" ", "_")}',
                'Category Name': sub_cat_clean,
                'Category Slug': sub_cat_clean.lower().replace(" ", "-").replace("(", "").replace(")", ""),
                'Parent Category': main_cat,
                'Description': f'Productos de {sub_cat_clean}'
            })
            
            # Procesar sub-subcategorías
            subsub_cats = df[(df['Categoría Principal'] == main_cat) & 
                           (df['Subcategoría'] == sub_cat)]['Sub-subcategoría']
            for subsub_cat in subsub_cats:
                if pd.notna(subsub_cat):
                    # Eliminar asterisco del inicio
                    subsub_cat_clean = subsub_cat.replace('* ', '')
                    cat_rows.append({
                        'Category ID': f'cat_{main_cat.lower().replace(" ", "_")}_{sub_cat_clean.lower().replace(" ", "_")}_{subsub_cat_clean.lower().replace(" ", "_")}',
                        'Category Name': subsub_cat_clean,
                        'Category Slug': subsub_cat_clean.lower().replace(" ", "-").replace("(", "").replace(")", ""),
                        'Parent Category': sub_cat_clean,
                        'Description': f'Productos de {subsub_cat_clean}'
                    })
    
    return pd.DataFrame(cat_rows)

def generate_product_csv(csv_file='output/productos_starcenter.csv'):
    """
    Genera el CSV de productos para importar en WooCommerce
    Args:
        csv_file: Archivo CSV con los productos convertidos
    Returns:
        DataFrame con los productos en formato WooCommerce
    """
    # Cargar productos del CSV
    productos_df = pd.read_csv(csv_file)
    
    # Convertir la marca a atributo global
    def set_marca_attributes(row):
        marca = str(row.get('Meta: _marca', '')).strip()
        if pd.notna(marca) and marca != 'nan' and marca != '':
            row['Attribute 1 name'] = 'Marca'
            row['Attribute 1 value(s)'] = marca
            row['Attribute 1 visible'] = 1
            row['Attribute 1 global'] = 1
        return row
    
    # Aplicar la conversión
    productos_df = productos_df.apply(set_marca_attributes, axis=1)
    
    return productos_df

def generate_attributes_sql(products_df, table_prefix='wp_'):
    """
    Genera el SQL para crear el atributo global 'Marca'
    """
    sql = f"""-- Crear atributo global Marca
INSERT INTO {table_prefix}woocommerce_attribute_taxonomies 
(attribute_name, attribute_label, attribute_type, attribute_orderby, attribute_public) 
VALUES 
('marca', 'Marca', 'select', 'name', 1);

-- Actualizar caché de atributos
DELETE FROM {table_prefix}options WHERE option_name = '_transient_wc_attribute_taxonomies';
"""
    return sql

def generate_menu_sql(categories_df, table_prefix='wp_'):
    """
    Genera el SQL para crear el menú en WordPress
    Args:
        categories_df: DataFrame con las categorías
        table_prefix: Prefijo de las tablas (por defecto 'wp_')
    """
    menu_name = "Mega Electronics"
    sql = f"""-- Crear el menú principal
INSERT INTO {table_prefix}terms (name, slug) 
VALUES ('{menu_name}', 'mega-electronics');

SET @menu_term_id = LAST_INSERT_ID();

INSERT INTO {table_prefix}term_taxonomy (term_id, taxonomy) 
VALUES (@menu_term_id, 'nav_menu');

SET @menu_tt_id = LAST_INSERT_ID();

-- Configurar la ubicación del menú
INSERT INTO {table_prefix}options (option_name, option_value, autoload) 
VALUES ('nav_menu_locations', CONCAT('a:1:{{s:7:"primary";i:', @menu_term_id, ';}}'), 'yes')
ON DUPLICATE KEY UPDATE option_value = VALUES(option_value);"""

    # Agregar items del menú
    menu_order = 0
    for _, cat in categories_df.iterrows():
        if not cat['Parent Category']:  # Solo categorías principales
            menu_order += 1
            sql += f"""

-- Agregar categoría: {cat['Category Name']}
INSERT INTO {table_prefix}posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', {menu_order}, '{cat['Category Name']}');

SET @item_id = LAST_INSERT_ID();

INSERT INTO {table_prefix}postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM {table_prefix}terms WHERE slug = '{cat['Category Slug']}' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{{i:0;s:0:""}}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO {table_prefix}term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);"""
    
    return sql.strip()

def main():
    # Generar estructura de categorías
    categories_df = generate_category_structure()
    
    # Crear directorio de salida
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar CSV de categorías
    categories_df.to_csv(os.path.join(output_dir, 'woo_categories.csv'), index=False)
    
    # Generar y guardar CSV de productos
    products_df = generate_product_csv()
    products_df.to_csv(os.path.join(output_dir, 'woo_products.csv'), index=False)
    
    # Generar y guardar SQL del menú
    menu_sql = generate_menu_sql(categories_df)
    with open(os.path.join(output_dir, 'menu_structure.sql'), 'w') as f:
        f.write(menu_sql)
    
    # Generar y guardar SQL para atributos
    attr_sql = generate_attributes_sql(products_df)
    with open(os.path.join(output_dir, 'attributes_structure.sql'), 'w') as f:
        f.write(attr_sql)
    
    print("\nArchivos generados exitosamente:")
    print("1. woo_categories.csv - Importar primero en WooCommerce")
    print("2. woo_products.csv - Importar después de las categorías")
    print("3. attributes_structure.sql - Ejecutar antes de importar productos")
    print("4. menu_structure.sql - Ejecutar en la base de datos de WordPress")
    print("\nPasos para importar en Local WP:")
    print("1. Primero importa woo_categories.csv usando WooCommerce")
    print("2. Ejecuta attributes_structure.sql en TablePlus")
    print("3. Luego importa woo_products.csv en WooCommerce")
    print("4. Finalmente, ejecuta menu_structure.sql en TablePlus")

if __name__ == '__main__':
    main()
