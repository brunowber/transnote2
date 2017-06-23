from detransapp.models import LogSincronizacao


def registro_log_sinc(solicitacao):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            LogSincronizacao.objects.registrar(request.POST['imei'], request.user.id, solicitacao)

            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    return _dec
