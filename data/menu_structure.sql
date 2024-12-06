-- Crear el menú principal
INSERT INTO wp_terms (name, slug) 
VALUES ('Mega Electronics', 'mega-electronics');

SET @menu_term_id = LAST_INSERT_ID();

INSERT INTO wp_term_taxonomy (term_id, taxonomy) 
VALUES (@menu_term_id, 'nav_menu');

SET @menu_tt_id = LAST_INSERT_ID();

-- Configurar la ubicación del menú
INSERT INTO wp_options (option_name, option_value, autoload) 
VALUES ('nav_menu_locations', CONCAT('a:1:{s:7:"primary";i:', @menu_term_id, ';}'), 'yes')
ON DUPLICATE KEY UPDATE option_value = VALUES(option_value);

-- Agregar categoría: Colectores de Datos
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 1, 'Colectores de Datos');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'colectores-de-datos' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Componentes Informáticos
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 2, 'Componentes Informáticos');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'componentes-informáticos' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Computadoras y Periféricos
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 3, 'Computadoras y Periféricos');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'computadoras-y-periféricos' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Fotografía Instantánea y Digital Profesional
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 4, 'Fotografía Instantánea y Digital Profesional');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'fotografía-instantánea-y-digital-profesional' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Gaming
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 5, 'Gaming');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'gaming' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Impresoras y Consumibles
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 6, 'Impresoras y Consumibles');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'impresoras-y-consumibles' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Lentes
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 7, 'Lentes');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'lentes' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Licenciamiento y Servicios en la Nube
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 8, 'Licenciamiento y Servicios en la Nube');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'licenciamiento-y-servicios-en-la-nube' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Materiales de Oficina
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 9, 'Materiales de Oficina');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'materiales-de-oficina' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Redes y Comunicaciones
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 10, 'Redes y Comunicaciones');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'redes-y-comunicaciones' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Repuestos y Accesorios
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 11, 'Repuestos y Accesorios');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'repuestos-y-accesorios' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);

-- Agregar categoría: Servidores y Almacenamiento
INSERT INTO wp_posts 
(post_author, post_date, post_date_gmt, post_status, post_type, menu_order, post_title) 
VALUES 
(1, NOW(), NOW(), 'publish', 'nav_menu_item', 12, 'Servidores y Almacenamiento');

SET @item_id = LAST_INSERT_ID();

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES 
(@item_id, '_menu_item_type', 'taxonomy'),
(@item_id, '_menu_item_menu_item_parent', '0'),
(@item_id, '_menu_item_object_id', (SELECT term_id FROM wp_terms WHERE slug = 'servidores-y-almacenamiento' LIMIT 1)),
(@item_id, '_menu_item_object', 'product_cat'),
(@item_id, '_menu_item_target', ''),
(@item_id, '_menu_item_classes', 'a:1:{i:0;s:0:""}'),
(@item_id, '_menu_item_xfn', ''),
(@item_id, '_menu_item_url', '');

INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
VALUES (@item_id, @menu_tt_id);