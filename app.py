from flask import Flask, request, render_template_string
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

def generate_image(name):
    # Create a figure and axis with better resolution
    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    
    # Define the heart function
    def heart(t):
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        return x, y

    # Generate the heart shape
    t = np.linspace(0, 2 * np.pi, 1000)
    x, y = heart(t)
    
    # Fill the heart shape with gradient color
    ax.fill(x, y, color='#ff4d4d', alpha=0.9)
    
    # Add the text inside the heart with better styling
    message = f'I Love You {name}'
    ax.text(0, -1, message, fontdict={
        'fontsize': 14, 
        'fontweight': 'bold', 
        'color': 'white',
        'fontfamily': 'cursive'
    }, ha='center')

    # Set the axis limits
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)

    # Remove the axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Hide the frame
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Save the figure to a buffer with optimized settings
    buf = io.BytesIO()
    plt.axis('off')
    plt.tight_layout()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, 
                dpi=100, transparent=False, facecolor='#ffe6e6')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free memory

    # Convert to base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            name = "My Love"
        
        try:
            img_base64 = generate_image(name)
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Romantic Heart for {{ name }}</title>
                    <style>
                        * {
                            margin: 0;
                            padding: 0;
                            box-sizing: border-box;
                        }
                        
                        body {
                            background: linear-gradient(135deg, #ffe6e6, #ffb3b3);
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                            font-family: 'Arial', sans-serif;
                            padding: 20px;
                        }
                        
                        .heart-container {
                            text-align: center;
                            background: white;
                            padding: 30px;
                            border-radius: 20px;
                            box-shadow: 0 10px 30px rgba(255, 77, 77, 0.3);
                            margin: 20px;
                            max-width: 90%;
                        }
                        
                        .heart-container h1 {
                            color: #ff4d4d;
                            margin-bottom: 20px;
                            font-size: 2em;
                        }
                        
                        .heart-image {
                            max-width: 100%;
                            height: auto;
                            border-radius: 10px;
                        }
                        
                        .back-button {
                            background: #ff4d4d;
                            color: white;
                            padding: 12px 30px;
                            border: none;
                            border-radius: 25px;
                            cursor: pointer;
                            font-size: 1em;
                            margin-top: 20px;
                            text-decoration: none;
                            display: inline-block;
                        }
                    </style>
                </head>
                <body>
                    <div class="heart-container">
                        <h1>For You, {{ name }}! 💖</h1>
                        <img src="data:image/png;base64,{{ img }}" alt="Heart for {{ name }}" class="heart-image">
                        <br>
                        <a href="/" class="back-button">Create Another Heart</a>
                    </div>
                </body>
                </html>
            ''', name=name, img=img_base64)
        except Exception as e:
            return f"Error generating image: {str(e)}", 500

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Create a Romantic Heart</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    background: linear-gradient(135deg, #ffe6e6, #ffb3b3);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    font-family: 'Arial', sans-serif;
                }
                
                .form-container {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(255, 77, 77, 0.2);
                    text-align: center;
                }
                
                .form-container h1 {
                    color: #ff4d4d;
                    margin-bottom: 30px;
                }
                
                input[type="text"] {
                    width: 100%;
                    padding: 15px 20px;
                    border: 2px solid #ffcccc;
                    border-radius: 25px;
                    font-size: 1em;
                    margin-bottom: 20px;
                }
                
                button {
                    background: #ff4d4d;
                    color: white;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 1.1em;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
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
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

