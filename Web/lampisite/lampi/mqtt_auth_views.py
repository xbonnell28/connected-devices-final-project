from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from paho.mqtt.client import topic_matches_sub


ACL_SUB = "1"  # READ
ACL_PUB = "2"  # WRITE


def unpack_POST_data(req):
    post_data = req.POST

    username = post_data.get("username", "")
    password = post_data.get("password", "")
    topic = post_data.get("topic", "")
    acc = post_data.get("acc", "")
    clientid = post_data.get("clientid", "")

    print("U: '{}' P: '{}' T: '{}' A: '{}' C: '{}'".format(username,
                                                           password,
                                                           topic,
                                                           acc,
                                                           clientid))

    return username, password, topic, acc, clientid


def get_user_from_session_key(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        return None
    uid = session.get_decoded().get('_auth_user_id')
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist:
        return None


@csrf_exempt
def auth(req):
    if req.method == 'POST':
        if req.META['REMOTE_ADDR'] == '127.0.0.1':
            username, password, topic, acc, clientid = unpack_POST_data(req)
            # need to handle
            #   django users - with username and password (mqtt-daemon)
            #   django users - with websockets
            #      username: device_id
            #      password: django session_key
            #   LAMPI devices - brokers authenticated with Certificates
            #      mosquitto handles SSL/TLS auth directly, so this
            #      auth function never is invoked
            #
            return HttpResponse(None, content_type='application/json')

    return HttpResponseForbidden(None, content_type='application/json')


@csrf_exempt
def superuser(req):
    # do not allow any superusers
    return HttpResponseForbidden(None, content_type='application/json')


@csrf_exempt
def acl(req):
    if req.method == 'POST':
        if req.META['REMOTE_ADDR'] == '127.0.0.1':
            username, password, topic, acc, clientid = unpack_POST_data(req)
            # need to handle
            #   django users
            #   django superusers
            #   websockets users
            #   LAMPI devices - broker bridges
            return HttpResponse(None, content_type='application/json')

    return HttpResponseForbidden(None, content_type='application/json')
