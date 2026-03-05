from flask import Flask, request, render_template_string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os

app = Flask(__name__)

def generate_image(name):
    fig, ax = plt.subplots(figsize=(8,8), dpi=100)

    def heart(t):
        x = 16*np.sin(t)**3
        y = 13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)
        return x,y

    t = np.linspace(0,2*np.pi,1000)
    x,y = heart(t)

    ax.fill(x,y,color='#ff4d4d',alpha=0.9)

    ax.text(0,-1,f'I Love You {name}',
        fontsize=14,
        fontweight='bold',
        color='white',
        ha='center')

    ax.set_xlim(-20,20)
    ax.set_ylim(-20,20)
    ax.axis('off')

    buf = io.BytesIO()
    fig.savefig(buf,format='png',bbox_inches='tight',pad_inches=0)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.getvalue()).decode()
    plt.close(fig)

    return img_base64


@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        name = request.form.get('name',"My Love")
        img = generate_image(name)

        return f"""
        <h1>For You {name} ❤️</h1>
        <img src='data:image/png;base64,{img}'>
        <br><br>
        <a href="/">Create Again</a>
        """

    return """
    <h1>Create Romantic Heart</h1>
    <form method="post">
    <input name="name">
    <button>Create</button>
    </form>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
