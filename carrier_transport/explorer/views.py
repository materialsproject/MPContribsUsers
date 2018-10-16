"""This module provides the views for the carrier_transport explorer interface."""

import os
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from collections import OrderedDict
from mpcontribs.rest.views import get_endpoint
from mpcontribs.io.core.components import render_dataframe, render_plot
from mpcontribs.io.core.recdict import render_dict

def index(request):
    ctx = RequestContext(request)
    from webtzite.models import RegisteredUser
    if request.user.is_authenticated():
        user = RegisteredUser.objects.get(username=request.user.username)
        API_KEY = user.api_key
        ENDPOINT = request.build_absolute_uri(get_endpoint())
        from ..rest.rester import CarrierTransportRester
        with CarrierTransportRester(API_KEY, endpoint=ENDPOINT) as mpr:
            try:
                prov = mpr.get_provenance()
                ctx['title'] = prov.pop('title')
                ctx['provenance'] = render_dict(prov, webapp=True)
                df = mpr.get_contributions(limit=3)
                url = request.build_absolute_uri(request.path) + 'rest/table'
                ctx['table'] = render_dataframe(
                    df, url=url, total_records=mpr.count(), webapp=True
                )
            except Exception as ex:
                ctx.update({'alert': str(ex)})
    else:
        return redirect('{}?next={}'.format(reverse('cas_ng_login'), request.path))
    return render_to_response("carrier_transport_explorer_index.html", ctx)