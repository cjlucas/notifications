#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, Thomas Jost <thomas.jost@gmail.com>
# 
# Permission  to use,  copy, modify,  and/or  distribute this  software for  any
# purpose  with  or without  fee  is hereby  granted,  provided  that the  above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS"  AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO  THIS SOFTWARE INCLUDING  ALL IMPLIED WARRANTIES  OF MERCHANTABILITY
# AND FITNESS. IN  NO EVENT SHALL THE AUTHOR BE LIABLE  FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR  CONSEQUENTIAL DAMAGES OR  ANY DAMAGES WHATSOEVER  RESULTING FROM
# LOSS OF USE, DATA OR PROFITS,  WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER  TORTIOUS ACTION,  ARISING  OUT OF  OR  IN CONNECTION  WITH  THE USE  OR
# PERFORMANCE OF THIS SOFTWARE.

"""Client for the iOS "Notifications" (aka "Push 4.0") app.

ttp://www.appnotifications.com/

This  module helps  scripts to  use  the HTTP  REST API  of the  `Notifications'
application, which is  available for the iPhone and the  iPod Touch. It supports
finding  the  user's credentials  token,  and  then  sending notification  in  a
synchronous or asynchronous way. This modules provides three functions:

get_credentials() -- Get the user's credentials token
send() -- Send a notification, waiting for it to be sent.
send_async() -- Send a  notification, returning immediately, without waiting for
the message to be sent.

"""

__author__ = "Thomas Jost <thomas.jost@gmail.com>, Chris Lucas <cjlucas07@gmail.com>"
__version__ = "0.3"

import sys
import threading
import xml.dom.minidom

_py3 = sys.version_info > (3,)

if _py3:
	from urllib.request import urlopen
	from urllib.parse import urlencode
else:
	from urllib import urlencode, urlopen
	
CREDENTIALS_URL = "https://www.appnotifications.com/user_session.xml"
SEND_URL = "https://www.appnotifications.com/account/notifications.xml"

def get_credentials(email, password):
    """Get the user's credentials token."""
    
    # Create data to POST
    data = {
        'user_session[email]': email,
        'user_session[password]': password
    }
    data = urlencode(data).encode('utf-8')

    # Send them
    u = urlopen(CREDENTIALS_URL, data)
    success = (u.getcode() == 200)
    if not success:
        return(False)

    # Parse the XML response
    response = u.read()
    u.close()
    doc = xml.dom.minidom.parseString(response)
    token = doc.getElementsByTagName("single-access-token")
    if len(token) == 0:
        return(False)
    return(token[0].firstChild.data)


def send(credentials, message, title=None, subtitle=None, long_message=None,
         long_message_preview=None, icon_url=None, message_level=0, silent=False,
         action_loc_key=None, run_command=None, sound=1, debug=False):
    """Send a notification, waiting for the message to be sent.

    The first two arguments (credentials  and message) are mandatory, all of the
    others are optional. They are  the same as the various identifiers described
    in    the   documentation    of    the   Notifications    HTTP   REST    API
    (http://developer.appnotifications.com/p/user_notifications.html).

    When  `debug` is  set  to `True`,  the XML  result  of the  HTTP request  is
    displayed on `sys.stderr`.

    This  function  returns  a  boolean  indicating  if  the  message  was  sent
    successfuly.

    """
    # Create data to POST
    data = {}

    if credentials is None or credentials == "":
        raise ValueError("Invalid user credentials")
    if message is None or message == "":
        raise ValueError("Invalid message")
    
    data['user_credentials'] = credentials
    data['notification[message]'] = message

    for key in ("title", "subtitle", "long_message", "long_message_preview",
                "icon_url", "message_level", "action_loc_key", "run_command"):
        value = locals()[key]
        if value is not None:
            data['notification[{0}]'.format(key)] = value

    if silent:
        data['notification[silent]'] = 1
    else:
        data['notification[silent]'] = 0
        if not 1 <= sound <= 7:
            raise ValueError("sound must be an integer between 1 and 7")
        data['notification[sound]'] = "{0}.caf".format(sound)

    # Encode the data, trying to deal with Unicode
    for k in data:
        if type(data[k]) is str:
            data[k] = data[k].encode('utf-8')
    
    data = urlencode(data).encode('utf-8')

    # Send the notification
    u = urlopen(SEND_URL, data)
    success = (u.getcode() == 200)
    if debug:
        sys.stderr.write(u.read().decode('utf-8'))
    u.close()

    return(success)


def send_async(*args, **kwargs):
    """Send  a  notification, returning  immediately,  without  waiting for  the
    message to be sent.

    This function does return the ID of the thread that does the HTTP request.
    
    """
    thr = threading.Thread(target=send, args=args, kwargs=kwargs)
    thr.daemon = True
    thr.start()
    return(thr)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        sys.stderr.write("Syntax: {0} credentials message".format(sys.argv[0]))
    else:
        send(sys.argv[1], sys.argv[2], debug=True)
