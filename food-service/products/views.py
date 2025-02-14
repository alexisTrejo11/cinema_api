# api/views/product_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .services import ProductService
from .serializers import ProductSerializer
from models import Product

@extend_schema(tags=['Products'])
class ProductViewSet(viewsets.ViewSet):
    """
    API endpoints for managing products.
    """

    @extend_schema(
        description="Retrieve a list of products with optional filters.",
        responses={200: ProductSerializer(many=True)},
        parameters=ProductService.list_schema_params()
    )
    def list(self, request):
        """
        Retrieve a list of products.
        """
        try:
            filters = request.query_params.dict()
            products = ProductService.get_all_products(filters)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        description="Create a new product.",
        request=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def create(self, request):
        """
        Create a new product.
        """
        try:
            product = ProductService.create_product(request.data, request.user)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        description="Retrieve a specific product by ID.",
        responses={200: ProductSerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific product.
        """
        try:
            product = ProductService.get_product_by_id(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        description="Update a specific product by ID.",
        request=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def update(self, request, pk=None):
        """
        Update a specific product.
        """
        try:
            product = ProductService.update_product(pk, request.data, request.user)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        description="Delete a specific product by ID.",
        responses={204: None}
    )
    def destroy(self, request, pk=None):
        """
        Delete a specific product.
        """
        try:
            ProductService.delete_product(pk, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)