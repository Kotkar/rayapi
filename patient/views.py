from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, RequestContext
from django.template import Context
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail


import json
import os
# Create your views here.

JSON_MAILFILE_PATH = os.path.join(settings.TEMPLATE_DIRS[0],
                         'patient_mails_list.json')
JSON_PATIENT_FILE_PATH = os.path.join(settings.TEMPLATE_DIRS[0],
                         'patient_list.json')

def get_json(file):
    """return data loading from json file.
    
    """
    try:
        return json.load(open(file))
    except:
        return {}

def update_mails_tojson(mails):
    """return update json file with mail sent to list of patients selected.
    
    """    
    with open(JSON_MAILFILE_PATH, 'w') as mails_to_json:
        mails_to_json.write(mails)

def patient_list_view(request):
    """Used to represent All Patients list from json file.
    
    """
    data = get_json(JSON_PATIENT_FILE_PATH)
    return render_to_response('patient_list.html', data, 
                              context_instance=RequestContext(request))

def send_mail_to_patients(email):
    """Send a mass mail to patients selected from patients list.
    
    @email: It contains selected patients email list, subject and message details.
    Used send_mass_mail from django mail modules.
    Raise an exception when any of the email required paramters are absent.  
    """
    subject = email.get('subject') or None
    message = email.get('message') or None
    from_email = settings.EMAIL_HOST_USER
    email_list = [p['email'] for p in email.get('patients', None) or None]
    email_list = filter(lambda x: x, email_list)
    if None in [message, subject, email_list]:
        raise Exception('''Error in Content of Message Either 
        in Message, SUbject or Emails''')
    msg_tuples = list()
    for email in email_list:
        msg_tuples.append((subject, message, from_email, [email]), )
    msg_tuples = tuple(msg_tuples)
    send_mass_mail(msg_tuples, fail_silently=False)

def home(request):
    """render home page, onload patient_list get called using
    XMLHttpRequest script.

    """
    return render_to_response('base.html', 
                              context_instance=RequestContext(request))

def send_emails(request):
    """Send Emails and save patients details in Json file. 
    
    This view gets patients json file to list out details of which patients
    has been selected. 
    Count sent mails and saved the current mail details.
    Handle Exception while sending and saving mail details.
    Display proper messages inform status of action using DJango message framework. 
    """
    if request.method == 'POST':
        try:
            ids = request.POST.getlist('id', None) or None
            if ids:
                data = get_json(JSON_PATIENT_FILE_PATH)
                email_patients = [p for p in data['items'] if p['id'] in ids]
                msg, sub = request.POST.get('msg'), request.POST.get('subject')
                email = {"patients": email_patients, "message": msg, 
                         "subject": sub}
#                Mass Mailing Functionality
                send_mail_to_patients(email)

#                Saving Sent Messages.
                json_mail = json.dumps(email)
                json_mails_list = get_json(JSON_MAILFILE_PATH)
                try:
                    json_mails_list[len(json_mails_list)] = json_mail
                    json_mails = json.dumps(json_mails_list)
                    update_mails_tojson(json_mails)
                    messages.info(request, "Email Sent Successfully!!")
                except Exception as ex:
                    print ex
                    messages.error(request, "Error while saving mails")
        except Exception as ex:
            messages.error(request, """Error Sending Mails
             mails - {}""".format(ex.message))

#    return render_to_response('patient_list.html', data, 
#                              context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('home'))


