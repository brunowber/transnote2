from django.shortcuts import redirect


def autenticado():
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if str(request.user) == "AnonymousUser":
                print "403 - Sem permissao de acesso!"
                return redirect('/')
            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view
    return _dec
