# # coding: utf-8
# from django.shortcuts import render, redirect
# from django.views.generic.base import View
#
# from detransapp.forms.infrator import FormInfrator
#
#
# class CadastroCondutorView(View):
#     template = 'condutor/salvar.html'
#
#     def get(self, request, condutor_id=None):
#
#         if condutor_id:
#             condutor = Condutor.objects.get(pk=condutor_id)
#             form = FormInfrator(instance=condutor)
#         else:
#             form = FormInfrator()
#
#         return render(request, self.template, {'form': form})
#
#     def post(self, request, condutor_id=None):
#
#         if condutor_id:
#             condutor = Condutor.objects.get(pk=condutor_id)
#             form = FormInfrator(instance=condutor, data=request.POST)
#         else:
#
#             form = FormInfrator(request.POST)
#
#         if form.is_valid():
#             form.save()
#
#             return redirect('/')
#
#         return render(request, self.template, {'form': form})
#
#
# class ConsultaCondutorView(View):
#     template_name = 'condutor/consulta.html'
#
#     def __page(self, request):
#         procurar = ''
#
#         if request.method == 'POST':
#
#             if 'procurar' in request.POST:
#                 procurar = request.POST['procurar']
#
#         else:
#
#             if 'procurar' in request.GET:
#                 procurar = request.GET['procurar']
#
#         try:
#             page = int(request.GET.get('page', 1))
#         except Exception:
#             page = 1
#
#         condutores_page = Condutor.objects.get_page(page, procurar)
#
#         return render(request, self.template_name, {'condutores': condutores_page, 'procurar': procurar})
#
#     def get(self, request):
#
#         return self.__page(request)
#
#     def post(self, request):
#
#         return self.__page(request)
