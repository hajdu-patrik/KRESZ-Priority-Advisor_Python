import os
import sys
from flask import Flask, render_template, request, Response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'template')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')

try:
    from business_logic import calculate_priority
except ImportError as e:
    print(f"ERROR: Failed to import the business_logic module: {e}")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# --- Site Identity ---
# Absolute base URL of the deployment, used for canonical links, social tags, robots and the sitemap.
SITE_URL = os.environ.get('SITE_URL', 'https://kresz-priority-advisor-system.vercel.app').rstrip('/')


@app.context_processor
def inject_site_urls():
    """Expose the site and the current canonical URL to every template."""
    return {'site_url': SITE_URL, 'canonical_url': SITE_URL + request.path}



# --- Web Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = None
    form_data = {
        'type_a': 'car', 'road_a': 'paved', 'sign_a': 'none',
        'type_b': 'car', 'road_b': 'paved', 'sign_b': 'none', 'dir_b': 'left'
    }

    if request.method == 'POST':
        data_a = {
            'type': request.form.get('type_a'),
            'road': request.form.get('road_a'),
            'sign': request.form.get('sign_a')
        }
        data_b = {
            'type': request.form.get('type_b'),
            'road': request.form.get('road_b'),
            'sign': request.form.get('sign_b'),
            'direction': request.form.get('dir_b')
        }
        
        form_data = {
            'type_a': data_a['type'], 'road_a': data_a['road'], 'sign_a': data_a['sign'],
            'type_b': data_b['type'], 'road_b': data_b['road'], 'sign_b': data_b['sign'], 'dir_b': data_b['direction']
        }

        result_text = calculate_priority(data_a, data_b)

    return render_template('index.html', result=result_text, form=form_data)

# --- 404 Error Handler ---
# --- Crawler Routes ---
@app.route('/robots.txt')
def robots_txt():
    # Everything is public; point crawlers at the sitemap.
    body = 'User-agent: *\nAllow: /\nSitemap: ' + SITE_URL + '/sitemap.xml\n'
    return Response(body, mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap_xml():
    urls = ''.join('  <url><loc>' + SITE_URL + path + '</loc></url>\n' for path in ['/'])
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n'
    return Response(body, mimetype='application/xml')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- Application Startpoint ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)