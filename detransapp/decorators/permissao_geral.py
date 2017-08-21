from django.shortcuts import redirect


def permissao_geral_required():
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if not request.user.has_perm('global_permissions.permissao_geral'):
                print "403 - Sem permissao de acesso!"
                return redirect('/')
            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view
    return _dec
