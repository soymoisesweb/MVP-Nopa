# MVP NOPA - WooCommerce Product Importer

Sistema de importación de productos para WooCommerce, diseñado específicamente para la migración del catálogo de StarCenter.

## Estructura del Proyecto

```
MVP NOPA/
├── data/           # Datos y recursos
│   ├── CSV/       # Datos de origen, catálogos
│   ├── JSON/      # Configuraciones y mapeos
│   └── SQL/       # Scripts y respaldos de base de datos
├── scripts/        # Código fuente
│   ├── config.py              # Configuraciones
│   ├── db_connection.py       # Conexión a base de datos
│   ├── woo_importer.py       # Core de importación
│   ├── category_manager.py    # Gestión de categorías
│   └── ...                    # Otros módulos
└── requirements.txt           # Dependencias
```

## Requisitos

- Python 3.8+
- MySQL/MariaDB
- WooCommerce instalado en WordPress

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd MVP-NOPA
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la base de datos:
   - Copiar `config.py.example` a `config.py`
   - Actualizar las credenciales de la base de datos

## Uso

1. Procesar el catálogo:
```bash
python scripts/process_catalog.py
```

2. Generar estructura WooCommerce:
```bash
python scripts/generate_woo_structure.py
```

3. Importar productos:
```bash
python scripts/generate_woo_products.py
```

## Características

- Importación masiva de productos
- Gestión de categorías
- Mapeo de atributos
- Validación de datos
- Gestión de errores y logs

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto es privado y propietario. Todos los derechos reservados.
