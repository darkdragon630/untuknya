from flask import Flask, request, render_template_string
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

def generate_image(name):
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Define the heart function
    def heart(t):
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        return x, y

    # Generate the heart shape
    t = np.linspace(0, 2 * np.pi, 1000)
    x, y = heart(t)
    ax.fill(x, y, color='red')  # Fill the heart shape with color

    # Add the text inside the heart
    message = f'I Love You {name}'
    ax.text(0, -5, message, fontdict={'fontsize': 12, 'fontweight': 'bold', 'color': 'lightgreen'}, ha='center')

    # Set the axis limits
    ax.set_xlim(-20, 20)
    ax.set_ylim(-40, 20)

    # Remove the axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Hide the frame
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.axis('off')  # Turn off the axis
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)  # Save with tight layout
    buf.seek(0)

    # Convert to base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        img_base64 = generate_image(name)
        return render_template_string('''
            <html>
            <head>
                <style>
                    body {
                        background-color: #ffe6e6;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-family: Arial, sans-serif;
                        margin: 0;
                    }
                    .heart-container {
                        text-align: center;
                    }
                    img {
                        margin-bottom: 30px; /* Menambahkan jarak antara gambar dan teks */
                    }
                    audio {
                        position: fixed;
                        bottom: 10px;
                        left: 10px;
                    }
                </style>
            </head>
            <body>
                <div class="heart-container">
                    <h1>Your Romantic Heart</h1>
                    <img src="data:image/png;base64,{{ img }}" alt="Heart">
                    <!-- Menghapus teks di bawah gambar -->
                </div>
                <audio autoplay loop>
                    <source src="https://www.bensound.com/bensound-music/bensound-love.mp3" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </body>
            </html>
        ''', img=img_base64)

    return render_template_string('''
        <html>
        <head>
            <style>
                body {
                    background-color: #ffe6e6;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: Arial, sans-serif;
                    margin: 0;
                }
                .form-container {
                    background: white;
                    padding: 20px 40px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    margin-bottom: 20px;
                }
                .form-container h1 {
                    color: #ff6666;
                    margin-bottom: 20px;
                }
                .form-container input[type="text"] {
                    width: 80%;
                    padding: 10px;
                    margin-bottom: 20px;
                    border: 1px solid #ff6666;
                    border-radius: 5px;
                }
                .form-container button {
                    background-color: #ff6666;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .form-container button:hover {
                    background-color: #ff4d4d;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h1>Enter Your Love's Name</h1>
                <form method="post">
                    <input type="text" id="name" name="name" placeholder="Name" required>
                    <br>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
