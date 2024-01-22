import json
import matplotlib.pyplot as plt


def createFigure(rows=1, cols=1):
    '''
    Crea una figura con varias gráficas

    rows = numero de filas
    cols = numero de columnas
    '''
    fig, ax = plt.subplots(rows, cols)
    plt.show()
    return fig, ax


def plot_tga(data, fig, text='TGA', language='English', streak='--', color='Black') -> None:
    """
    Representa una grafica TGA

    data: Archivo con los datos TRATADOS del experimento
    text: Etiqueta que aparece en la leyenda
    language: Idioma de la gráfica (ejes)
    """
    with open('config//text.json', 'r') as config:
        # Carga el contenido del archivo JSON en una variable Python
        data_config = json.load(config)[language]

    with open('config//graph_settings.json', 'r') as settings:
        # Carga el contenido del archivo JSON en una variable Python
        graph_settings = json.load(settings)

    streak = graph_settings['Trazo'][streak]
    color = graph_settings['Color'][color]

    fig.plot(data['Ts'], data['% mass'], linestyle=streak, color=color, label=text)
    fig.set_xlabel(data_config['Temp'])
    fig.set_ylabel(data_config['% Mass'])
    fig.legend(loc='best')
    fig.set_xlim(data['Ts'].min(), data['Ts'].max())

def plot_dsc(data, fig, text='TGA', language='English', streak='--', color='Black') -> None:
    """
    Representa una grafica DSC

    data: Archivo con los datos TRATADOS del experimento
    text: Etiqueta que aparece en la leyenda
    language: Idioma de la gráfica (ejes)
    """
    with open('config//text.json', 'r') as config:
        # Carga el contenido del archivo JSON en una variable Python
        data_config = json.load(config)[language]

    with open('config//graph_settings.json', 'r') as settings:
        # Carga el contenido del archivo JSON en una variable Python
        graph_settings = json.load(settings)

    streak = graph_settings['Trazo'][streak]
    color = graph_settings['Color'][color]

    fig.plot(data['Ts'], data['% mass'], linestyle=streak, color=color, label=text)
    fig.set_xlabel(data_config['Temp'])
    fig.set_ylabel(data_config['HF'])
    fig.legend(loc='best')
    fig.set_xlim(data['Ts'].min(), data['Ts'].max())

def resize_figure(xmin, xmax, ymin, ymax) -> None:
    """
    Cambia el rango de los ejes x e y

    xmin = valor minimo eje x
    xmax = valor maximo eje x
    ymin = valor minimo eje y
    ymin = valor maximo eje y
    """
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
