from flask import Flask, request, render_template_string
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
                        position: relative;
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
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                    }
                    
                    .heart-image {
                        max-width: 100%;
                        height: auto;
                        border-radius: 10px;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
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
                        transition: all 0.3s ease;
                        text-decoration: none;
                        display: inline-block;
                    }
                    
                    .back-button:hover {
                        background: #ff3333;
                        transform: translateY(-2px);
                        box-shadow: 0 5px 15px rgba(255, 77, 77, 0.4);
                    }
                    
                    .audio-controls {
                        position: fixed;
                        bottom: 20px;
                        left: 20px;
                        background: rgba(255, 255, 255, 0.9);
                        padding: 10px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    
                    .audio-controls button {
                        background: #ff4d4d;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 5px;
                        cursor: pointer;
                        margin: 0 5px;
                    }
                    
                    @media (max-width: 768px) {
                        .heart-container {
                            padding: 20px;
                        }
                        
                        .heart-container h1 {
                            font-size: 1.5em;
                        }
                        
                        .audio-controls {
                            position: relative;
                            bottom: auto;
                            left: auto;
                            margin-top: 20px;
                        }
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
                
                <div class="audio-controls">
                    <audio id="loveSong" loop>
                        <source src="https://www.bensound.com/bensound-music/bensound-love.mp3" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                    <button onclick="document.getElementById('loveSong').play()">Play Music</button>
                    <button onclick="document.getElementById('loveSong').pause()">Pause Music</button>
                </div>

                <script>
                    // Auto-play music with user interaction
                    document.addEventListener('click', function() {
                        const audio = document.getElementById('loveSong');
                        if (audio.paused) {
                            audio.play().catch(e => console.log('Auto-play prevented:', e));
                        }
                    }, { once: true });
                </script>
            </body>
            </html>
        ''', name=name, img=img_base64)

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
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    font-family: 'Arial', sans-serif;
                    padding: 20px;
                }
                
                .form-container {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(255, 77, 77, 0.2);
                    text-align: center;
                    max-width: 500px;
                    width: 90%;
                }
                
                .form-container h1 {
                    color: #ff4d4d;
                    margin-bottom: 30px;
                    font-size: 2.2em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }
                
                .form-container p {
                    color: #666;
                    margin-bottom: 25px;
                    font-size: 1.1em;
                    line-height: 1.5;
                }
                
                .input-group {
                    margin-bottom: 25px;
                }
                
                .form-container input[type="text"] {
                    width: 100%;
                    padding: 15px 20px;
                    border: 2px solid #ffcccc;
                    border-radius: 25px;
                    font-size: 1em;
                    transition: all 0.3s ease;
                    outline: none;
                }
                
                .form-container input[type="text"]:focus {
                    border-color: #ff4d4d;
                    box-shadow: 0 0 10px rgba(255, 77, 77, 0.3);
                }
                
                .form-container input[type="text"]::placeholder {
                    color: #ffb3b3;
                }
                
                .form-container button {
                    background: linear-gradient(135deg, #ff4d4d, #ff3333);
                    color: white;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 1.1em;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    box-shadow: 0 5px 15px rgba(255, 77, 77, 0.4);
                }
                
                .form-container button:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 8px 25px rgba(255, 77, 77, 0.6);
                }
                
                .heart-emoji {
                    font-size: 3em;
                    margin-bottom: 20px;
                    animation: pulse 1.5s ease-in-out infinite alternate;
                }
                
                @keyframes pulse {
                    from { transform: scale(1); }
                    to { transform: scale(1.1); }
                }
                
                @media (max-width: 480px) {
                    .form-container {
                        padding: 30px 20px;
                    }
                    
                    .form-container h1 {
                        font-size: 1.8em;
                    }
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <div class="heart-emoji">💖</div>
                <h1>Create a Romantic Heart</h1>
                <p>Enter your loved one's name to create a beautiful personalized heart</p>
                <form method="post">
                    <div class="input-group">
                        <input type="text" id="name" name="name" placeholder="Enter name here..." required maxlength="50">
                    </div>
                    <button type="submit">Create Heart 💝</button>
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
