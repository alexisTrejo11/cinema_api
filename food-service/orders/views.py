from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from models import Order
from serializers import OrderSerializer
from services import OrderService

@extend_schema(tags=['Orders'])
class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer

    @extend_schema(
        description="List all orders with filtering capabilities",
        responses={200: OrderSerializer(many=True)}
    )
    def list(self, request):
        status_filter = request.query_params.get('status')
        user_id = request.query_params.get('user_id')
        
        filters = {}
        if status_filter:
            filters['status'] = status_filter
        if user_id:
            filters['user_id'] = user_id
            
        orders = Order.objects.filter(**filters).order_by('-created_at')
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Create a new order",
        request=OrderSerializer,
        responses={201: OrderSerializer}
    )
    def create(self, request):
        try:
            order = OrderService.create_order(
                user_id=request.data['user_id'],
                items=request.data['items'],
                combos=request.data.get('combos', [])
            )
            serializer = self.serializer_class(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Update order status",
        methods=['POST'],
        responses={200: OrderSerializer}
    )
    @action(detail=True, methods=['POST'])
    def update_status(self, request, pk=None):
        try:
            new_status = request.data.get('status')
            if not new_status:
                return Response({"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            order = OrderService.update_order_status(pk, new_status)
            serializer = self.serializer_class(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Apply promotions to order",
        methods=['POST'],
        responses={200: OrderSerializer}
    )
    @action(detail=True, methods=['POST'])
    def apply_promotions(self, request, pk=None):
        try:
            promotion_codes = request.data.get('promotion_codes', [])
            order = OrderService.apply_promotions(pk, promotion_codes)
            serializer = self.serializer_class(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)