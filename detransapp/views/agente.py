# coding: utf-8
"""View sobre os agentes"""

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.agente import FormAgente
from detransapp.models.dispositivo import Dispositivo
from detransapp.models.agente import Agente
from detransapp.models.agente_login import Agente_login
from detransapp.serializers import AgenteSerializer
from detransapp.rest import JSONResponse
from detransapp.decorators import validar_imei, permissao_geral_required



class CadastroAgenteView(View):
    """Classe para fazer o cadastro dos agentes"""

    template = 'agente/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, agente_id=None):
        """Pega o formulario para fazer o cadastro
        ou editar os agentes"""

        if agente_id:
            agente = Agente.objects.get(pk=agente_id)
            form = FormAgente(instance=agente)
        else:
            form = FormAgente()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, agente_id=None):
        """Envia para o banco os agentes criados ou editados"""

        if agente_id:
            agente = Agente.objects.get(pk=agente_id)
            form = FormAgente(instance=agente, data=request.POST)
        else:
            form = FormAgente(request.POST)
        if form.is_valid():
            form.is_active = True
            agente = form.save()
            permissao_geral = form.cleaned_data['permissao_geral']
            if permissao_geral:
                permission = Permission.objects.get(codename='permissao_geral')
                agente.user_permissions.add(permission)

            return redirect('/')
        return render(request, self.template, {'form': form})


class ConsultaAgenteView(View):
    """Classe para fazer a consulta dos agentes"""

    template_name = 'agente/consulta.html'

    def __page(self, request):
        procurar = ''

        if request.method == 'POST':
            if 'procurar' in request.POST:
                procurar = request.POST['procurar']

        else:
            if 'procurar' in request.GET:
                procurar = request.GET['procurar']

        try:
            page = int(request.GET.get('page', 1))
        except Exception:
            page = 1

        agentes_page = Agente.objects.get_page(page, procurar)
        return render(request, self.template_name, {'agentes': agentes_page, 'procurar': procurar})

    def get(self, request):
        """Pega a primeira página da consulta"""

        return self.__page(request)

    def post(self, request):
        """Devolve os dados que foram procurados"""

        return self.__page(request)


class GetAgentesRestView(APIView):
    """Atualiza os agentes no Android"""

    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        """Atualiza todos os agentes depois da data da
        última atualização"""

        if 'data' in request.POST:
            agentes = Agente.objects.get_agentes_sicronismo(request.POST['data'])
        else:
            agentes = Agente.objects.get_agentes_sicronismo()
        agentes_js = []
        for agente in agentes:
            serializer = AgenteSerializer(agente)
            agentes_js.append(serializer.data)
        return JSONResponse(agentes_js)


class GetLoginVerifyRestView(APIView):
    """Classe para fazer a verificação no Android se o usuário e senha estão corretos
    ou se o usuário já não está 'logado' em outro aparelho"""

    permission_classes = (AllowAny,)

    @method_decorator(validar_imei())
    def post(self, request):
        """Função que envia do Android para o servidor verificar"""

        username = request.POST['username']
        password = request.POST['password']
        agente = authenticate(username=username, password=password)
        if agente is not None:
            agente_login = Agente_login.objects.filter(agente_id=agente, status=True)
            if not agente_login:
                return JSONResponse(1)
        return JSONResponse(0)


class GetControlLoginRestView(APIView):
    """Verificar se o usuário está logado ou existe"""

    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        """Verifica no servidor se o agente está logado para permissão"""

        status = True
        if int(request.POST['status']) == 0:
            status = False

        dispositivo = Dispositivo.objects.get(imei=str(request.POST['imei']))
        agente = int(request.POST['agente'])
        # Login
        if status:
            agente_login = Agente_login.objects.filter(agente_id=agente, status=True)
            if agente_login:
                return JSONResponse({'permission': 0})
            else:
                agente_login = Agente_login()
                agente_login.agente_id = agente
                agente_login.device_id = dispositivo.id
                agente_login.status = True
                agente_login.save()
                return JSONResponse({'permission': 1})
        else:
            agente_login = Agente_login.objects.get(agente_id=agente, status=True)
            if agente_login:
                agente_login.status = False
                agente_login.data_logout = timezone.now()
                agente_login.save()
                return JSONResponse({'permission': 1})
            else:
                return JSONResponse({'permission': 0})


class DesbloqueioAgenteView(View):
    """Desativar logins de agentes"""

    template = 'agente/desbloqueio.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, agente_id=None):
        """Pega os ids dos agentes logado e desloga o agente escolhido"""

        if agente_id:
            agente_des = Agente_login.objects.get(agente_id=agente_id, status=True)
            agente_des.status = False
            agente_des.save()
            return redirect('/agente/desbloqueio/')
        else:
            agentes_logados = Agente_login.objects.filter(status=True)
            return render(request, self.template, {'agentes_logados': agentes_logados})
