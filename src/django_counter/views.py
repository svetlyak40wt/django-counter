from django.http import HttpResponseRedirect, HttpResponse
import mimetypes, rfc822, os, stat
from pdb import set_trace
from django.shortcuts import get_object_or_404
from models import RedirCounter, Referer, ViewCounter

try:
    from PIL import Image
except ImportError:
    import Image

from StringIO import StringIO

_img  = Image.fromstring('RGB', (1,1), '000')
_ff = StringIO()
_img.save(_ff, format='GIF')
_ff.seek(0)

IMG_MIMETYPE = 'image/gif'
IMG_DATA = _ff.read()

def count(request, ctype_id, object_id):
    ctype_id = int(ctype_id)
    object_id = int(object_id)
    counter = ViewCounter.objects.increment(ctype_id, object_id)

    response = HttpResponse(IMG_DATA, mimetype=IMG_MIMETYPE)
    return response

# We may use
# update counter_downloadcounter as t1 set count = (select sum(t2.count) from counter_referer as t2 where t1.id = t2.counter_id);
# to calculate all total stats, if needed.
#
def redir(request, counter_id):
    referer = request.environ.get('HTTP_REFERER') or 'none'
    counter = get_object_or_404(RedirCounter, id = counter_id)
    ref = counter.referers.filter(url = referer)[:1]
    if not ref:
        ref = Referer(counter = counter, url = referer, count = 0)
    else:
        ref = ref[0]
    ref.count += 1
    ref.save()
    counter.count += 1
    counter.save()
    return HttpResponseRedirect(counter.url)
