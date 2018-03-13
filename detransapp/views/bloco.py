# coding: utf-8
"""View para gerar os blocos"""
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.bloco import FormBloco
from detransapp.models import Bloco
from detransapp.decorators import validar_imei, permissao_geral_required
from detransapp.rest import JSONResponse
from detransapp.models.bloco_padrao import BlocoPadrao
from detransapp.models.infracao import Infracao
from detransapp.serializers import BlocoSerializer


class CadastroBlocoView(View):
    template = 'bloco/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, bloco_id=None):

        if bloco_id:
            bloco = BlocoPadrao.objects.get(pk=bloco_id)
            form = FormBloco(instance=bloco)
        else:

            form = FormBloco()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, bloco_id=None):
        bloco_id = bloco_id
        form = FormBloco(request.POST)

        is_input = True

        if bloco_id:
            bloco_padrao = BlocoPadrao.objects.get(pk=bloco_id)
            form = FormBloco(instance=bloco_padrao, data=request.POST)
            is_input = False
            mensagem = 'Bloco editado com sucesso!'

        else:

            form = FormBloco(request.POST)
            mensagem = 'Bloco criado com sucesso!'

        if form.is_valid():

            if int(request.POST['inicio_intervalo']) < 0 or \
                            int(request.POST['inicio_intervalo']) > \
                            int(request.POST['fim_intervalo']):
                return redirect('/bloco/')

            if is_input:
                post = form.save(commit=False)

                # Controle de bloco campo 'ativo'

                bloco = BlocoPadrao.objects.filter(ativo=True)
                if len(bloco) >= 1:
                    post.ativo = False
                    form.save()
                else:
                    form.save()

            else:

                form.save()

            messages.success(request, mensagem)
            return redirect('/bloco/consulta/')

        return render(request, self.template, {'form': form})


class ConsultaBlocoView(View):
    template_name = 'bloco/consulta.html'

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

        blocos_page = BlocoPadrao.objects.get_page(page, procurar)

        return render(request, self.template_name, {'blocos': blocos_page, 'procurar': procurar})

    def get(self, request):

        return self.__page(request)

    def post(self, request):

        return self.__page(request)


# View que mandará as informações para o client

class GetBlocoRestView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        if not Bloco.objects.filter(usuario=request.user) or \
                Bloco.objects.filter(usuario=request.user, ativo=True):
            bloco = AddBloco(request)

            # caso não houver bloco padrão cadastrado
            if not bloco:
                return JSONResponse({'error': 'Não há bloco mestre cadastrado'})

            bloco.save()

            serializer = BlocoSerializer(bloco)

            js_core = []
            js_core.append(serializer.data)
            return JSONResponse(js_core)
        else:
            bp = BlocoPadrao.objects.get(ativo=True)

            bloco = Bloco.objects.filter(usuario=request.user, ativo=True).order_by('-data')[0]

            inf = Infracao.objects.filter(
                id__range=[bloco.fim_intervalo - (bp.numero_paginas - 1), bloco.fim_intervalo])

            # Se excedeu o número de páginas necessárias para a reposição
            if (bp.numero_paginas - len(inf)) <= bloco.minimo_pag_restantes:

                core_js = []

                bloco_antigo = Bloco.objects.filter(
                    usuario=request.user).order_by('-data_alterado')[0]
                bloco_antigo.ativo = False
                if (bp.numero_paginas - len(inf)) > 0:
                    bloco_antigo.inicio_intervalo = (inf[len(inf) - 1].id) + 1
                    bloco_antigo.minimo_pag_restantes = 0
                    seria = BlocoSerializer(bloco_antigo)
                    core_js.append(seria.data)

                bloco_antigo.save()

                bloco_novo = AddBloco(request)
                bloco_novo.save()

                serializer = BlocoSerializer(bloco_novo)
                core_js.append(serializer.data)
                return JSONResponse(core_js)

            else:
                bloco = Bloco.objects.filter(usuario=request.user).order_by('-data')
                core_js = []
                bp = BlocoPadrao.objects.get(ativo=True)

                if len(bloco) > 1:
                    inf1 = Infracao.objects.filter(
                        id__range=[bloco[1].fim_intervalo - (
                            bp.numero_paginas - 1), bloco[1].fim_intervalo])
                    if bp.minimo_pag_restantes >= (bp.numero_paginas - len(inf1)) > 0:
                        bloco1 = Bloco.objects.get(id=bloco[1].id)

                        bloco1.inicio_intervalo = (inf1[len(inf1) - 1].id) + 1
                        bloco1.minimo_pag_restantes = 0
                        bloco1.status = False
                        bloco1.data_alterado = timezone.now()
                        bloco1.save()
                        serializer = BlocoSerializer(bloco1)
                        core_js.append(serializer.data)

                pos = len(inf)
                bloco = Bloco.objects.get(id=bloco[0].id)
                bloco.data_alterado = timezone.now()

                if pos > 0:
                    bloco.inicio_intervalo = inf[pos - 1].id + 1

                bloco.save()
                serializer = BlocoSerializer(bloco)
                core_js.append(serializer.data)
                return JSONResponse(core_js)


def AddBloco(request):
    try:
        bp = BlocoPadrao.objects.get(ativo=True)
    except Exception:
        return False

    bloco = Bloco()
    bloco.fim_intervalo = (bp.contador + bp.numero_paginas) - 1
    bloco.inicio_intervalo = bp.contador

    if bloco.fim_intervalo > bp.fim_intervalo:
        bloco.fim_intervalo = bp.fim_intervalo
        bp.ativo = False
        try:
            prox_bloco = BlocoPadrao.objects.filter(ativo=False)
            prox_bloco[0].ativo = True
        except Exception:
            pass

    bloco.usuario = request.user
    bloco.ativo = True
    bloco.minimo_pag_restantes = bp.minimo_pag_restantes
    bloco.bloco_padrao = bp
    bp.contador += bp.numero_paginas
    bp.save()

    return bloco
