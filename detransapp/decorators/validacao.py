from rest_framework import status

from detransapp.models import Dispositivo
from detransapp.rest import JSONResponse


def validar_imei():
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            print request.POST
            
            if 'imei' in request.POST:
                print request.POST['imei']
                dispositivo = Dispositivo.objects.existe_dispositivo(request.POST['imei'])

                if dispositivo:
                    return view_func(request, *args, **kwargs)

            return JSONResponse({'status': 'Dispositivo nao encontrado!'},
                                status=status.HTTP_403_FORBIDDEN)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    return _dec
