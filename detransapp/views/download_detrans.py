# coding: utf-8
"""Faz o download de apk"""
import os
import os.path
import mimetypes
# Uplouad
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.models.config_sinc import ConfigSinc
from detransapp.forms.up_apk import UploadApkForm


class DownloadDetransView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)
    # @method_decorator(login_required)
    # @method_decorator(validar_imei())
    # @method_decorator(registro_log_sinc(0))

    def get(self, request):
        filename = 'detrans.sqlite.gz'
        db_path = "%s/%s" % (settings.MEDIA_ROOT, filename)

        response = StreamingHttpResponse(FileWrapper(open(db_path)),
                                         content_type=mimetypes.guess_type(db_path)[0])

        response['Content-Type'] = 'application/x-gzip'
        response['Content-Length'] = os.path.getsize(db_path)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        return response


class UploadDetransApkView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)
    template = 'upload/apk.html'
    def get(self, request):
        cf = ConfigSinc.objects.filter()
        cf = cf[len(cf)-1]

        down = '0'
        form = UploadApkForm()
        if cf.caminho_apk != '':
            down = '1'
        return render(request, self.template, {'form': form, 'down': down},)

    def post(self, request):
        try:
            sistema = ConfigSinc.objects.filter()[0]
        except Exception:
            return HttpResponseRedirect('/download-apk/')
        form = UploadApkForm(request.POST or None, request.FILES or None, instance=sistema)
        if 'caminho_apk' in request.FILES and str(request.FILES['caminho_apk'])[-4:] == '.apk':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
            else:
                form = UploadApkForm()
                return render(request, self.template, {'form': form})
        else:
            form = UploadApkForm()
            return render(request, self.template, {'form': form, 'erro': 'erro_arquivo'})


def handle_uploaded_file(f):

    name = 'media/' + str(f.name)
    destination = open(name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


class DownloadDetransApkView(View):
    permission_classes = (IsAuthenticated, AllowAny)
    # Download

    def get(self, request, down=None):
        cf = ConfigSinc.objects.filter()
        cf = cf[len(cf)-1]
        if down == '1':
            filename = str(cf.caminho_apk)
            db_path = "%s/%s" % (settings.MEDIA_ROOT, filename)
            if filename == '' or os.path.exists(db_path) is False:
                form = UploadApkForm()
                return render(request, 'upload/apk.html', {'form': form, 'erro': 'erro_servidor'})
            else:

                response = StreamingHttpResponse(FileWrapper(open(db_path)),
                                                 content_type=mimetypes.guess_type(db_path)[0])

                response['Content-Type'] = 'application/vnd.android.package-archive'
                response['Content-Length'] = os.path.getsize(db_path)
                response['Content-Disposition'] = "attachment; filename=%s" % filename

                return response
        else:
            pass
