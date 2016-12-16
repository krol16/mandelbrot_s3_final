from django.shortcuts import render
from pylab import *
import datetime
import boto
import boto.s3.connection

# Create your views here.

def index(request):
	return render(request, 'mandelapp/index.html')
	
def generate(request):
	breite = int(request.GET.get('breite',''))
	hohe = int(request.GET.get('hohe',''))
	iterationen = int(request.GET.get('iterationen',''))

        access_key = 'AKIAIRBBN7ZV7UPV7F6A'
        secret_key = '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'
	conn = boto.connect_s3(
                aws_access_key_id = access_key,
                aws_secret_access_key = secret_key,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
        bucket = conn.create_bucket('superbuckets3')
	path = createMandelBrot(breite, hohe, iterationen, bucket)
	
	return render(request, 'mandelapp/index.html', {'code':5, 'path': path, 'brots': get_brots(bucket)})

def get_brots(bucket):
        return bucket.list()

def createMandelBrot(breite, hohe, iter, bucket):
	path = "mandelbrot.png"
	schluessel = bucket.new_key('mandelbrot.png')

	iterations = iter
	density = 1000
	x_min, x_max = -2, 1
	y_min, y_max = -1.5, 1.5
	x, y = meshgrid(linspace(x_min, x_max, density),
	linspace(y_min, y_max, density))
	c = x + 1j*y
	z = c.copy()
	m = zeros((density, density))
	for n in xrange(iterations):
		print "Completed %d %%" % (100 * float(n)/iterations)
		indices = (abs(z) <= 10)
		z[indices] = z[indices]**2 + c[indices]
		m[indices] = n
	imshow(log(m), cmap=cm.hot, extent=(x_min, x_max, y_min, y_max))
	path = "/home/ubuntu/mandelbrot/mandelbrot_s3_final/assets/"+path
        savefig(path)
	title('Mandelbrot Set')
	xlabel('Re(z)')
	ylabel('Im(z)')

	schluessel.set_contents_from_filename(path)
        schluessel.set_canned_acl('public-read')
        link = schluessel.generate_url(expires_in=10, query_auth=False, force_http=True)
        return link
