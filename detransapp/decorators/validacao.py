import datetime
from rest_framework import status

from detransapp.models import Dispositivo, Acesso, Agente
from detransapp.rest import JSONResponse


def validar_imei():
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if 'imei' in request.POST:
                dispositivo = Dispositivo.objects.existe_dispositivo(request.POST['imei'])
                if dispositivo:
                    return view_func(request, *args, **kwargs)
                else:
                    acesso = Acesso.objects.get_or_create(imei=request.POST['imei'])[0]
                    try:
                        acesso.usuario = Agente.objects.get(id=request.POST['agente']).username
                    except:
                        acesso.usuario = Agente.objects.get(username=request.POST['username']).username
                    acesso.dt_acesso = datetime.datetime.now()
                    acesso.save()
            return JSONResponse({'status': 'Dispositivo nao encontrado!'},
                                status=status.HTTP_403_FORBIDDEN)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    return _dec
