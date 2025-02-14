import logging
from django.core.cache import cache
from repository import ProductRepository
from logging import log_action

logger = logging.getLogger(__name__)
CACHE_TIMEOUT = 60 * 15  # 15 minutes

class ProductService:
    
    @staticmethod
    def list_schema_params():
        """
        Define schema parameters for Swagger documentation.
        """
        return [
            {
                "name": "category",
                "in": "query",
                "required": False,
                "schema": {"type": "string"}
            },
            {
                "name": "min_price",
                "in": "query",
                "required": False,
                "schema": {"type": "number"}
            },
            {
                "name": "max_price",
                "in": "query",
                "required": False,
                "schema": {"type": "number"}
            }
        ]
    
    @classmethod
    def get_all_products(cls, filters=None):
        """
        Retrieve all products with optional filters.
        """
        cache_key = f"products_{str(filters)}"
        
        # Cache Layer
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for products with filters: {filters}")
            return cached_data
        
        # Database Layer
        try:
            logger.debug(f"Fetching products from DB with filters: {filters}")
            products = ProductRepository.get_filtered_products(filters)
            
            # Cache population
            cache.set(cache_key, products, CACHE_TIMEOUT)
            logger.info(f"Cache updated for key: {cache_key}")
            
            return products
        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}")
            raise

    @classmethod
    def create_product(cls, data, user):
        """
        Create a new product.
        """
        try:
            logger.info(f"Attempting to create product by user: {user.id}")
            product = ProductRepository.create_product(data)
            
            # Log the action
            log_action(
                user=user,
                action="product_create",
                details=f"New product created: {product.id}",
                metadata=data
            )
            
            # Invalidate related cache
            cls._invalidate_product_cache()
            
            return product
        except Exception as e:
            logger.critical(f"Error creating product: {str(e)}", exc_info=True)
            raise

    @classmethod
    def get_product_by_id(cls, product_id):
        """
        Retrieve a product by its ID.
        """
        return ProductRepository.get_product_by_id(product_id)

    @classmethod
    def update_product(cls, product_id, data, user):
        """
        Update a product by its ID.
        """
        product = ProductRepository.update_product(product_id, data)
        log_action(
            user=user,
            action="product_update",
            details=f"Product updated: {product_id}",
            metadata=data
        )
        cls._invalidate_product_cache()
        return product

    @classmethod
    def delete_product(cls, product_id, user):
        """
        Delete a product by its ID.
        """
        ProductRepository.delete_product(product_id)
        log_action(
            user=user,
            action="product_delete",
            details=f"Product deleted: {product_id}"
        )
        cls._invalidate_product_cache()

    @classmethod
    def _invalidate_product_cache(cls):
        """
        Invalidate all product-related cache keys.
        """
        cache_keys = [key for key in cache.keys() if "products_" in key]
        cache.delete_many(cache_keys)
        logger.info(f"Cache invalidated for {len(cache_keys)} product keys")