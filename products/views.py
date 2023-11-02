from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import rest_framework.status as api_status
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    name = request.GET.get("name")
    if name:
        message = f"Hello, {name}"
    else:
        message = "Hello World!"
    return Response({"message": message}, status=api_status.HTTP_200_OK)
    #return JsonResponse({"message": message}, status=api_status.HTTP_200_OK, content_type="application/json")
     