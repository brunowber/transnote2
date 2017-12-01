"""URLs"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from detransapp import views
from detransapp.views import settings, CadastroLeisView, \
    ConsultaLeisView, CadastroModeloView, ConsultaModeloView, CadastroTipoView, \
    ConsultaTipoView, CadastroTipoInfracaoView, ConsultaTipoInfracaoView, \
    CadastroCancelamentoView, ConsultaCancelamentoView, CarregaTiposInfracao, \
    CadastroEspecieView, ConsultaEspecieView, CadastroAgenteView, ConsultaAgenteView, \
    DesbloqueioAgenteView, CadastroCorView, ConsultaCorView, CadastroCategoriaView, \
    ConsultaCategoriaView, CadastroDispositivoView, ConsultaDispositivoView, \
    CadastroVeiculoView, ConsultaVeiculoView, CadastroProprietarioView, \
    ConsultaProprietarioView, CadastroBlocoView, ConsultaBlocoView, \
    RelatorioInfracaoView, RelatorioInfracaoDetalhesView, UploadDetransLogoView, \
    DownloadDetransView, UploadDetransApkView, DownloadDetransApkView, \
    GetAutuadorRestView, GetBlocoRestView, GetAgentesRestView, \
    GetControlLoginRestView, GetVeiculosRestView, GetTiposInfracaoRestView, \
    GetTiposVeiculoRestView, GetModelosRestView, GetEspeciesRestView, \
    GetCategoriasRestView, GetCoresRestView, GetRegioesRestView, GetUFsRestView, \
    GetCidadesRestView, SincronismoRestView, RecebeInfracoesRestView, \
    GetConfigSincRestView, GetLoginVerifyRestView, ImportaCor, ImportaCategoria, \
    ImportaEspecie, ImportaCidade, ImportaTipoVeiculo, ImportaModelo, \
    ImportaVeiculo, CriaSqliteView, CriaSqliteCanceladoView, StatusView, \
    CadastroDETView, ConsultaDETView, GeraDet, ConfigSincView, TemplateDET, ConsultaDispositivoAcessoView, \
    CadastroDispositivoAcessoView, RemoveDispositivoAcessoView

from detransapp.views.infracao import GetImageRestView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^media/(.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),
                       url(r'^static/(.*)$', 'django.views.static.serve',
                           {'document_root': settings.STATIC_ROOT}),
                       url(r'^$', views.index, name='index'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'login/login.html'},
                           name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name': 'logout/logout.html'}, name='logout'),

                       url(r'^relatorios/', views.relatorios, name='relatorios'),
                       url(r'^sobre/', views.about, name='sobre'),

                       url(r'^legislacao/$', CadastroLeisView.as_view(),
                           name='cad-legislacao'),
                       url(r'^legislacao/(?P<condutor_id>\d+)/$', CadastroLeisView.as_view(),
                           name='cad-legislacao'),
                       url(r'^legislacao/consulta/$', ConsultaLeisView.as_view(),
                           name='leis-consulta'),

                       url(r'^modelo/$', CadastroModeloView.as_view(), name='cad-modelo'),
                       url(r'^modelo/(?P<modelo_id>\d+)/$', CadastroModeloView.as_view(),
                           name='cad-modelo'),
                       url(r'^modelo/consulta/$', ConsultaModeloView.as_view(),
                           name='modelo-consulta'),

                       url(r'^tipo-veiculo/$', CadastroTipoView.as_view(),
                           name='cad-tipo-veiculo'),
                       url(r'^tipo-veiculo/(?P<tipo_id>\d+)/$', CadastroTipoView.as_view(),
                           name='cad-tipo-veiculo'),
                       url(r'^tipo-veiculo/consulta/$', ConsultaTipoView.as_view(),
                           name='tipo-veiculo-consulta'),

                       url(r'^tipo-infracao/$', CadastroTipoInfracaoView.as_view(),
                           name='cad-tipo-infracao'),
                       url(r'^tipo-infracao/(?P<tipo_infracao_id>[\w-]+)/$',
                           CadastroTipoInfracaoView.as_view(),
                           name='cad-tipo-infracao'),
                       url(r'^tipo_infracao/consulta/$', ConsultaTipoInfracaoView.as_view(),
                           name='tipo-infracao-consulta'),

                       url(r'^tipo-cancelamento/$', CadastroCancelamentoView.as_view(),
                           name='cad-tipo-cancelamento'),
                       url(r'^tipo-cancelamento/(?P<tipo_infracao_id>\d+)/$',
                           CadastroCancelamentoView.as_view(),
                           name='cad-tipo-cancelamento'),
                       url(r'^tipo-cancelamento/consulta/$',
                           ConsultaCancelamentoView.as_view(),
                           name='tipo-cancelamento-consulta'),

                       url(r'^tipo-infracao/carrega/$', CarregaTiposInfracao.as_view(),
                           name='carrega-tipo-infracao'),

                       url(r'^especie/$', CadastroEspecieView.as_view(), name='cad-especie'),
                       url(r'^especie/(?P<especie_id>\d+)/$', CadastroEspecieView.as_view(),
                           name='cad-especie'),
                       url(r'^especie/consulta/$', ConsultaEspecieView.as_view(),
                           name='especie-consulta'),

                       url(r'^agente/$', CadastroAgenteView.as_view(),
                           name='cad-agente'),
                       url(r'^agente/(?P<agente_id>\d+)/$', CadastroAgenteView.as_view(),
                           name='cad-agente'),
                       url(r'^agente/consulta/$', ConsultaAgenteView.as_view(),
                           name='agente-consulta'),
                       url(r'^agente/desbloqueio/$', DesbloqueioAgenteView.as_view(),
                           name='des-agente'),
                       url(r'^agente/desbloqueio/(?P<agente_id>\d+)/$',
                           DesbloqueioAgenteView.as_view(),
                           name='des-agente'),

                       url(r'^cor/$', CadastroCorView.as_view(), name='cad-cor'),
                       url(r'^cor/(?P<cor_id>\d+)/$', CadastroCorView.as_view(),
                           name='cad-cor'),
                       url(r'^cor/consulta/$', ConsultaCorView.as_view(),
                           name='cor-consulta'),

                       url(r'^categoria/$', CadastroCategoriaView.as_view(),
                           name='cad-categoria'),
                       url(r'^categoria/(?P<categoria_id>\d+)/$', CadastroCategoriaView.as_view(),
                           name='cad-categoria'),
                       url(r'^categoria/consulta/$', ConsultaCategoriaView.as_view(),
                           name='categoria-consulta'),

                       url(r'^dispositivo/$', CadastroDispositivoView.as_view(),
                           name='cad-dispositivo'),
                       url(r'^acesso/(?P<dispositivo_id>\d+)/$', CadastroDispositivoAcessoView.as_view(),
                           name='cad-acesso'),
                       url(r'^remove_acesso/(?P<dispositivo_id>\d+)/$', RemoveDispositivoAcessoView.as_view(),
                           name='remove-acesso'),
                       url(r'^dispositivo/(?P<dispositivo_id>\d+)/$',
                           CadastroDispositivoView.as_view(),
                           name='cad-dispositivo'),
                       url(r'^dispositivo/consulta/$', ConsultaDispositivoView.as_view(),
                           name='dispositivo-consulta'),
                       url(r'^dispositivo/acesso/$', ConsultaDispositivoAcessoView.as_view(),
                           name='dispositivo-acesso'),

                       url(r'^veiculo/$', CadastroVeiculoView.as_view(), name='cad-veiculo'),
                       url(r'^veiculo/(?P<veiculo_id>\d+)/$', CadastroVeiculoView.as_view(),
                           name='cad-veiculo'),
                       url(r'^veiculo/consulta/$', ConsultaVeiculoView.as_view(),
                           name='veiculo-consulta'),

                       url(r'^proprietario/$', CadastroProprietarioView.as_view(),
                           name='cad-proprietario'),
                       url(r'^proprietario/(?P<proprietario_id>\d+)/$',
                           CadastroProprietarioView.as_view(),
                           name='cad-proprietario'),
                       url(r'^proprietario/consulta/$', ConsultaProprietarioView.as_view(),
                           name='proprietario-consulta'),

                       url(r'^bloco/$', CadastroBlocoView.as_view(), name='cad-bloco'),
                       url(r'^bloco/(?P<bloco_id>\d+)/$', CadastroBlocoView.as_view(),
                           name='cad-bloco'),
                       url(r'^bloco/consulta/$', ConsultaBlocoView.as_view(),
                           name='bloco-consulta'),

                       url(r'^infracao/relatorio/$', RelatorioInfracaoView.as_view(),
                           name='relatorio-infracao'),
                       url(r'^infracao/relatorio/(?P<infracao_id>\d+)/$',
                           RelatorioInfracaoDetalhesView.as_view(), name='detalhes-infracao'),

                       url(r'^sistema/$', UploadDetransLogoView.as_view(),
                           name='upload-logo'),

                       url(r'^get-cidades/$', 'detransapp.views.cidade.get_cidades',
                           name='get-cidades'),
                       url(r'^downloadsqlite/$', DownloadDetransView.as_view(),
                           name='download_sqlite'),
                       url(r'^download-apk/$', UploadDetransApkView.as_view(),
                           name='upload_apk'),
                       url(r'^download-apk/(?P<down>\d+)/$', DownloadDetransApkView.as_view(),
                           name='download_apk'),

                       # REST
                       # <BLOCO>
                       url(r'^rest/det_autuador/$', GetAutuadorRestView.as_view(),
                           name='rest-det_autuador'),
                       url(r'^rest/bloco/$', GetBlocoRestView.as_view(),
                           name='rest-bloco'),
                       url(r'^rest/image/$', GetImageRestView.as_view(),
                           name='rest-image'),
                       url(r'^rest/agente/$', GetAgentesRestView.as_view(),
                           name='rest-agente'),
                       url(r'^rest/agente_login/$', GetControlLoginRestView.as_view(),
                           name='rest-agente-login'),
                       url(r'^rest/veiculo/$', GetVeiculosRestView.as_view(),
                           name='rest-veiculo'),
                       url(r'^rest/tipo-infracao/$', GetTiposInfracaoRestView.as_view(),
                           name='rest-tipo-infracao'),
                       url(r'^rest/tipo-veiculo/$', GetTiposVeiculoRestView.as_view(),
                           name='rest-tipo-veiculo'),
                       url(r'^rest/modelo/$', GetModelosRestView.as_view(),
                           name='rest-modelo'),
                       url(r'^rest/especie/$', GetEspeciesRestView.as_view(),
                           name='rest-especies'),
                       url(r'^rest/categoria/$', GetCategoriasRestView.as_view(),
                           name='rest-categorias'),
                       url(r'^rest/cor/$', GetCoresRestView.as_view(),
                           name='rest-cores'),
                       url(r'^rest/regiao/$', GetRegioesRestView.as_view(),
                           name='rest-regioes'),
                       url(r'^rest/uf/$', GetUFsRestView.as_view(),
                           name='rest-ufs'),
                       url(r'^rest/cidade/$', GetCidadesRestView.as_view(),
                           name='rest-cidades'),
                       url(r'^rest/sincronismo/$', SincronismoRestView.as_view(),
                           name='rest-sincronismo'),
                       url(r'^rest/infracoes/$', RecebeInfracoesRestView.as_view(),
                           name='rest-infracoes'),
                       url(r'^rest/config-sinc/$', GetConfigSincRestView.as_view(),
                           name='rest-config-sinc'),

                       # Carga inicial
                       url(r'^rest/agent_verify/$', GetLoginVerifyRestView.as_view(),
                           name='rest-login-verify'),
                       url(r'^carga-inicial/$', 'detransapp.views.carga_inicial.carga_cadasdro',
                           name='carga-inicial'),

                       url(r'^cadastra_inf/$', 'detransapp.views.cadastra_inf.cad',
                           name='cadastra-inf'),

                       url(r'^importa/cor/$', ImportaCor.as_view(),
                           name='importa-cor'),
                       url(r'^importa/categoria/$', ImportaCategoria.as_view(),
                           name='importa-categoria'),
                       url(r'^importa/especie/$', ImportaEspecie.as_view(),
                           name='importa-especie'),
                       url(r'^importa/cidade/$', ImportaCidade.as_view(),
                           name='importa-cidade'),
                       url(r'^importa/tipo-veiculo/$', ImportaTipoVeiculo.as_view(),
                           name='importa-tipo-veiculo'),
                       url(r'^importa/modelo/$', ImportaModelo.as_view(),
                           name='importa-modelo'),
                       url(r'^importa/veiculo/$', ImportaVeiculo.as_view(),
                           name='importa-veiculo'),

                       url(r'^cria-sqlite/$', CriaSqliteView.as_view(),
                           name='cria-sqlite'),
                       url(r'^cria-sqlite-cancelado/$', CriaSqliteCanceladoView.as_view(),
                           name='cria-sqlite-cancelado'),
                       url(r'^status-sqlite/$', StatusView.as_view(),
                           name='status-sqlite'),
                       url(r'^config/set/det$', CadastroDETView.as_view(),
                           name='cadastra-det'),
                       url(r'^config/get/det$', ConsultaDETView.as_view(),
                           name='consulta-det'),
                       url(r'^config/geradet/format/(?P<formato>\d+)/$', GeraDet.as_view(),
                           name='gera-det'),
                       url(r'^config/geradet/(?P<filtro>\d+)/(?P<formato>\d+)/$', GeraDet.as_view(),
                           name='gera-det'),
                       url(r'^configuracoes/$', ConfigSincView.as_view(),
                           name='config'),
                       url(r'^config/det$', TemplateDET.as_view(),
                           name='template-det'), ) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
