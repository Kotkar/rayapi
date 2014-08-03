from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RayApi.views.home', name='home'),
    # url(r'^RayApi/', include('RayApi.foo.urls')),
    url(r'^$', 'patient.views.home', name='home'),
#    url(r'^patients/$', include('RayApi.patient.urls')),
    url(r'^patients/$', 'patient.views.patient_list_view', name='patient_list'),
    url(r'^patients/sendmail/$', 'patient.views.send_emails', name='send-mails'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
