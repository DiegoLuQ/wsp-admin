import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os 

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi import HTTPException
from html2image import Html2Image
from PIL import Image
from io import BytesIO

app = FastAPI()
os.environ['CHROME_EXECUTABLE'] = '/usr/bin/google-chrome-stable'

async def create_plotly_ejem():
    # Crear el DataFrame
    df = pd.DataFrame(dict(
        grupo = ["A", "B", "C", "D", "E"],
        valor = [14, 12, 8, 10, 16]
    ))

    # Crear el gráfico de barras con Plotly
    fig = go.Figure(data=go.Bar(x=df['grupo'], y=df['valor'], text=df['valor'], textposition='auto'))

    # Configurar el diseño del gráfico
    fig.update_layout(
        title='Ejemplo de Gráfico',
        xaxis_title='Grupo',
        yaxis_title='Valor',
        height=500,  # Altura del gráfico
        width=800    # Ancho del gráfico
    )

    # Guardar el gráfico como un archivo HTML
    fig.write_html("templates/plotly_example_report_5.html")

@app.get("/generate_image")
async def generate_image():
    await create_plotly_ejem()
    # Genera la imagen a partir del HTML
    # await generate_image_from_html('templates/plotly_ejem_report2.html', 'output3.png', width=1080, height=1080)
    await generate_image_from_html('templates/plotly_example_report_5.html', 'output5.jpeg', width=1080, height=1080)
    
    return {"message": "Imagen generada correctamente"}

@app.get("/")
async def home():
    
    return {"message": "Conectado"}
 
@app.get("/download_image")
async def download_image():
    try:
        return FileResponse("output5.png", media_type="image/png", filename="output5.png")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/view_image")
async def view_image():
    try:
        with open("output5.png", "rb", encoding='utf-8') as file:
            image_bytes = file.read()
        return {"image": image_bytes}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/image")
def get_image():
    # Load the image file
    image = Image.open("output5.jpeg")  # Replace with your image path

    # Convert the image to a byte buffer
    img_buffer = BytesIO()
    image.convert("RGB").save(img_buffer, format="JPEG")
    img_buffer.seek(0)

    # Return the image as a response
    return Response(content=img_buffer.read(), media_type="image/jpeg")

@app.get("/image/{image_path:path}")
def get_image_for_url(image_path: str):
    try:
        # Load the image file
        image = Image.open(image_path)  # Suponiendo que image_path es el nombre de la imagen

        # Convert the image to a byte buffer
        img_buffer = BytesIO()
        image.convert("RGB").save(img_buffer, format="JPEG")
        img_buffer.seek(0)

        # Return the image as a response
        return Response(content=img_buffer.read(), media_type="image/jpeg")
    except Exception as e:
        return Response(content="Error al cargar la imagen", status_code=500)


@app.get("/send_msg")
def send_msg():
    # Load the image file
    
    return {"Hello":"Nuevo Mensaje Para whatsapp"}

async def generate_image_from_html(html_file, output_file, width=None, height=None):
    """
    Genera una imagen a partir de un archivo HTML.

    Args:
        html_file (str): Ruta al archivo HTML.
        output_file (str): Ruta de salida para guardar la imagen.
        width (int, optional): Ancho de la imagen. Por defecto es None.
        height (int, optional): Alto de la imagen. Por defecto es None.
    """
    hti = Html2Image()
    with open(html_file, encoding='utf-8') as f:
        html_content = f.read()
    hti.screenshot(html_str=html_content, save_as=output_file, size=(width, height))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)