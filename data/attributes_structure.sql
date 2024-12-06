-- Crear atributo global Marca
INSERT INTO wp_woocommerce_attribute_taxonomies 
(attribute_name, attribute_label, attribute_type, attribute_orderby, attribute_public) 
VALUES 
('marca', 'Marca', 'select', 'name', 1);

-- Actualizar caché de atributos
DELETE FROM wp_options WHERE option_name = '_transient_wc_attribute_taxonomies';
