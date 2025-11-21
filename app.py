from flask import Flask, request, render_template_string
import matplotlib
matplotlib.use('Agg')  # Important for server environments
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os

app = Flask(__name__)

def generate_image(name):
    try:
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
        
        # Define the heart function
        def heart(t):
            x = 16 * np.sin(t)**3
            y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
            return x, y

        # Generate the heart shape
        t = np.linspace(0, 2 * np.pi, 1000)
        x, y = heart(t)
        ax.fill(x, y, color='#ff4d4d', alpha=0.9)
        
        # Add the text inside the heart
        message = f'I Love You {name}'
        ax.text(0, -1, message, fontdict={
            'fontsize': 14, 
            'fontweight': 'bold', 
            'color': 'white',
            'fontfamily': 'cursive'
        }, ha='center')

        # Set the axis limits and remove borders
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Save the figure
        buf = io.BytesIO()
        plt.axis('off')
        plt.tight_layout()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, 
                    dpi=100, facecolor='#ffe6e6')
        buf.seek(0)
        plt.close(fig)

        # Convert to base64
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return img_base64
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip() or "My Love"
        img_base64 = generate_image(name)
        
        if img_base64:
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>For You, {{ name }}!</title>
                    <style>
                        body { background: #ffe6e6; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; font-family: Arial; }
                        .container { background: white; padding: 30px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(255,77,77,0.3); }
                        h1 { color: #ff4d4d; }
                        .btn { background: #ff4d4d; color: white; padding: 12px 30px; border: none; border-radius: 25px; text-decoration: none; display: inline-block; margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>For You, {{ name }}! 💖</h1>
                        <img src="data:image/png;base64,{{ img }}" alt="Heart">
                        <br>
                        <a href="/" class="btn">Create Another Heart</a>
                    </div>
                </body>
                </html>
            ''', name=name, img=img_base64)
        else:
            return "Error generating image", 500

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Create a Romantic Heart</title>
            <style>
                body { background: #ffe6e6; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; font-family: Arial; }
                .container { background: white; padding: 40px; border-radius: 20px; text-align: center; box-shadow: 0 15px 35px rgba(255,77,77,0.2); }
                h1 { color: #ff4d4d; }
                input { padding: 15px 20px; border: 2px solid #ffcccc; border-radius: 25px; margin: 20px 0; width: 100%; }
                button { background: #ff4d4d; color: white; padding: 15px 40px; border: none; border-radius: 25px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Create a Romantic Heart</h1>
                <form method="post">
                    <input type="text" name="name" placeholder="Enter your love's name" required>
                    <br>
                    <button type="submit">Create Heart 💝</button>
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
