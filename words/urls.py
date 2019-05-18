"""words URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from V import show,handleForm,others

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', show.homepage),
    url(r'^login/', handleForm.login),
    url(r'^regist/', handleForm.regist),
    url(r'^logout/', handleForm.logout),
    url(r'^record/', show.record),
    url(r'^exam/', show.exam),
    url(r'^getword/', show.getword),
    url(r'^calculate/', show.calculate),
    url(r'^print/', others.printout),
    url(r'^printer/', others.printer),
    url(r'^bugs/', others.bugs),
    url(r'^about/', others.about),
    url(r'^trans/', others.trans),
]
