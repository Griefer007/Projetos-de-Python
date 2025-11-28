from flask import Flask, send_from_directory, redirect, url_for

app = Flask(__name__)
import random, os
facts_list = [
    "Honey never spoils.",
    "Bananas are berries, but strawberries aren't.",
    "A group of flamingos is called a 'flamboyance'.",
    "Octopuses have three hearts.",
    "Wombat poop is cube-shaped.",
    "There are more stars in the universe than grains of sand on Earth.",
    "A day on Venus is longer than a year on Venus.",
    "The Eiffel Tower can be 15 cm taller during the summer.",
    "Sharks have been around longer than trees."]
@app.route("/")
def home():
    return (
        '<h1>bem vindo ao site MUITO LEGAL!!!!!</h1>'
        '<h2><a href="/fact">FATOS.INTERESSANTES!!!!!!</a></h2>'
        '<h2><a href="/about">SOBRE..ESTESITE!!!!!!</a></h2>'
        '<h2><a href="/fruit">VER FRUTA (imagem low-quality)</a></h2>'
        '<h2><a href="/ncs">ABRIR UMA MÚSICA NCS ALEATÓRIA</a></h2>'
    )
@app.route("/fact")
def fact():
    return f'<h1>{random.choice(facts_list)}</h1>' '<h2>você pode refrescar a página para receber um novo fato!' '<h3><a href="/">HOME.HOME</a></h3>'
@app.route("/about")
def about():
    return '<h1>Sobre este site</h1>' '<h2>EU FIZ ESSE SITE, SSSSSSSSIIIIIIIIIIIIIIIIIIIIIMMMMMMMMMMMMMMM!!!!!!</h2>' '<h3><a href="/">HOME.HOME</a></h3>'

# Directory where generated images live
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'Images')

# list of generated low-quality image filenames (created by generate_low_quality_fruits.py)
fruit_files = [
    'apple_low.jpg',
    'cantaloupe_low.jpg',
    'banana_low.jpg',
    'pear_low.jpg',
    'orange_low.jpg',
]

# Small curated list of NCS links (can be extended)
ncs_list = [
    'https://www.youtube.com/watch?v=2lYR1kMcUe4',
    'https://www.youtube.com/watch?v=3JWTaaS7LdU',
    'https://www.youtube.com/watch?v=7wtfhZwyrcc',
    'https://www.youtube.com/watch?v=Uj1ykZWtPYI'
]


@app.route('/images/<path:filename>')
def images(filename):
    # Serve images from the Images directory
    return send_from_directory(IMAGES_DIR, filename)


@app.route('/fruit')
def fruit():
    # pick a random generated fruit image (falls back if file missing)
    fname = random.choice(fruit_files)
    image_url = url_for('images', filename=fname)
    return (
        f'<h1>Fruta aleatória</h1>'
        f'<img src="{image_url}" alt="fruit" style="width:420px;height:420px;image-rendering:pixelated;display:block;margin:12px 0;"/>'
        f'<p><a href="/ncs">Ouvir uma faixa NCS aleatória</a></p>'
        f'<p><a href="/">Voltar</a></p>'
    )


@app.route('/ncs')
def ncs():
    # Redirect to a random NCS YouTube link
    return redirect(random.choice(ncs_list))


def youtube_embed_url(watch_url, autoplay=1):
    # extract video id from common watch URL formats and return embed URL
    # examples: https://www.youtube.com/watch?v=VIDEOID or https://youtu.be/VIDEOID
    vid = None
    if 'v=' in watch_url:
        # split on v=
        parts = watch_url.split('v=')
        vid = parts[1].split('&')[0]
    elif 'youtu.be/' in watch_url:
        vid = watch_url.split('youtu.be/')[1].split('?')[0]
    if not vid:
        return watch_url
    return f'https://www.youtube.com/embed/{vid}?autoplay={1 if autoplay else 0}&rel=0&modestbranding=1'


@app.route('/ncsfruit')
@app.route('/NCSFRUIT')
def ncsfruit():
    # Serve a dedicated page showing a random fruit image and an embedded NCS player
    fname = random.choice(fruit_files)
    watch = random.choice(ncs_list)
    embed = youtube_embed_url(watch, autoplay=1)
    image_url = url_for('images', filename=fname)
    # Inline minimal JS to fallback to drawing a pixel fruit if image missing
    html_template = """<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>NCS + Fruit</title>
    <style>
        body{font-family:Segoe UI,Arial;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
        .card{background:#1b1b1b;padding:18px;border-radius:8px;max-width:900px;width:100%;display:flex;gap:18px;align-items:center}
        img{width:420px;height:420px;image-rendering:pixelated;border-radius:6px;background:#222}
        .right{flex:1;color:#eee}
    </style>
</head>
<body>
    <div class="card">
        <img id="fruitImg" src="__IMAGE__" alt="fruit" onerror="fallbackDraw()"/>
        <div class="right">
            <h2>Now playing (NCS)</h2>
            <div id="playerWrap"><iframe id="player" width="420" height="236" src="__EMBED__" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
            <p><button id="playBtn">Play (if autoplay blocked)</button></p>
            <p><a href="/">Voltar</a></p>
        </div>
    </div>

    <script>
    function fallbackDraw(){
        try{
            const px=64; const canvas=document.createElement('canvas'); canvas.width=px; canvas.height=px;
            const ctx=canvas.getContext('2d'); ctx.fillStyle='#fff'; ctx.fillRect(0,0,px,px);
            // simple circle fruit
            ctx.fillStyle='#d11b2b'; ctx.beginPath(); ctx.arc(px/2,px/2,px*0.32,0,Math.PI*2); ctx.fill();
            const img=document.getElementById('fruitImg'); img.src=canvas.toDataURL('image/jpeg',0.18);
        }catch(e){console.warn(e);}
    }
    document.getElementById('playBtn').addEventListener('click',function(){
        var iframe=document.getElementById('player');
        // reload iframe with autoplay parameter to encourage playback after user gesture
        var src=iframe.src; if(src.indexOf('autoplay=1')===-1){ src=src+ (src.indexOf('?')===-1?'?':'&') + 'autoplay=1';} iframe.src=src;
    });
    </script>
</body>
</html>
"""
    html = html_template.replace('__IMAGE__', image_url).replace('__EMBED__', embed)
    return html


if __name__ == '__main__':
    app.run(debug=True)