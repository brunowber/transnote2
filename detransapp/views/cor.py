# coding: utf-8
"""CRUD de cores"""
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.cor import FormCor
from detransapp.forms.importacao import FormArquivo
from detransapp.models import Cor
from detransapp.decorators import validar_imei, permissao_geral_required, autenticado
from detransapp.rest import JSONResponse
from detransapp.serializers import CorSerializer


class CadastroCorView(View):
    """Cadastra as cores"""

    template = 'cor/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, cor_id=None):
        """Pega o formulário e envia para o template"""

        if cor_id:
            cor = Cor.objects.get(pk=cor_id)
            form = FormCor(instance=cor)
        else:
            form = FormCor()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, cor_id=None):
        """Envia as novas cores para a base no servidor"""

        if cor_id:
            cor = Cor.objects.get(pk=cor_id)
            form = FormCor(instance=cor, data=request.POST)
            mensagem = 'Cor editada com sucesso!'
        else:
            form = FormCor(request.POST)
            mensagem = 'Cor inserida com sucesso!'

        if form.is_valid():
            form.save(request)

            messages.success(request, mensagem)
            return redirect('/cor/consulta/')

        return render(request, self.template, {'form': form})


class ConsultaCorView(View):
    """Consulta as cores cadastradas"""

    template_name = 'cor/consulta.html'

    @method_decorator(autenticado())
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

        cores_page = Cor.objects.get_page(page, procurar)

        return render(request, self.template_name, {'cores': cores_page, 'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):
        """Pega a primeira página das cores"""
        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):
        """Faz a pesquisa requisitaad"""
        return self.__page(request)


class GetCoresRestView(APIView):
    """Pega as cores do servidor para o Android"""
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        """Envia as cores do Android para o servidor"""
        if 'data' in request.POST:
            cores = Cor.objects.get_cores_sicronismo(request.POST['data'])
        else:
            cores = Cor.objects.get_cores_sicronismo()

        cores_js = []
        for cor in cores:
            serializer = CorSerializer(cor)
            cores_js.append(serializer.data)
        return JSONResponse(cores_js)


class ImportaCor(View):
    """Importa as cores"""

    template_name = 'cor/importa.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        """Faz um formulário e envia para o template"""
        form = FormArquivo()

        return render(request, self.template_name, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        """Envia o arquivo de cores para a base de dados"""

        i = 0

        if 'arquivo' in request.FILES and str(request.FILES['arquivo'])[-4:] == ".txt":
            arq = request.FILES['arquivo']
            for linha in arq:
                try:
                    linha = linha.encode('UTF-8')

                    cod = linha[0:2]
                    cor = linha[2:].strip()
                    nova_cor = Cor.objects.filter(codigo=cod).first()

                    if nova_cor:
                        nova_cor.descricao = cor
                    else:
                        nova_cor = Cor(codigo=cod, descricao=cor)

                    nova_cor.save()
                    i += 1
                except Exception:
                    pass

            return render(request, self.template_name, {'qtd': i, 'envio': True})
        else:
            form = FormArquivo()
            return render(request, self.template_name, {'form': form, 'erro': 'arquivo inválido'})
