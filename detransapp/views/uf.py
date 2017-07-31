# coding: utf-8
"""Rest das UFs"""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from detransapp.models import UF
from detransapp.serializers import UFSerializer
from detransapp.rest import JSONResponse
from detransapp.decorators import validar_imei


class GetUFsRestView(APIView):
    """View para enviar as Ufs do servidor para o Android"""

    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        """Envia as Ufs para o Android"""

        if 'data' in request.POST:
            ufs = UF.objects.get_ufs_sicronismo(request.POST['data'])
        else:
            ufs = UF.objects.get_ufs_sicronismo()

        json_ufs = []
        for estado in ufs:
            serializer = UFSerializer(estado)
            json_ufs.append(serializer.data)
        return JSONResponse(json_ufs)
