# GKOM – Billboarding

Program renderuje scenę 3D z billboardami drzew lub chmur, skyboxem oraz modelem 3D oświetlonym cieniowaniem Phonga.

## Wymagania

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) lub pip

## Instalacja

```bash
uv sync
```

lub

```bash
pip install -r requirements.txt
```

## Uruchomienie

```bash
python main.py trees    # scena z drzewami (billboardy axial)
python main.py clouds   # scena z chmurami (billboardy world-oriented)
```

Domyślnie bez podania argumentu uruchamia się scena `trees`.

## Sterowanie

| Klawisz             | Akcja                                      |
| ------------------- | ------------------------------------------ |
| W / S / A / D       | Poruszanie się po scenie                   |
| Spacja / Lewy Shift | Lot w górę / w dół                         |
| Mysz                | Obrót kamery                               |
| R                   | Zamrożenie / wznowienie obrotu billboardów |
| ESC                 | Wyjście                                    |

## Struktura projektu

```
src/
├── app.py        # Główna klasa aplikacji – pętla renderująca, obsługa scen i billboardów
├── camera.py     # Kamera FPS z obsługą klawiatury i myszy
├── model.py      # Wczytywanie i renderowanie modeli w formacie .obj
├── shader.py     # Kompilacja i obsługa programów shaderów GLSL
├── skybox.py     # Cubemapa skyboxa – ładowanie tekstur i renderowanie sześcianu
├── texture.py    # Ładowanie tekstur 2D z plików PPM
├── material.py   # Parametry materiału Phonga (ambient, specular, shininess)
├── utils.py      # Wspólny parser plików PPM
└── window.py     # Inicjalizacja okna GLFW i kontekstu OpenGL
shaders/
├── basic.vert / basic.frag       # Shader obiektów sceny z cieniowaniem Phonga
└── skybox.vert / skybox.frag     # Shader skyboxa
```

## Zrealizowane funkcjonalności

- Cieniowanie Phonga (ambient, diffuse, specular) z konfigurowalnymi parametrami materiału
- Kamera perspektywiczna typu FPS ze swobodnym poruszaniem się po scenie
- Wczytywanie modeli w formacie `.obj`
- Billboardy w dwóch wariantach: **axial** (drzewa) i **world-oriented** (chmury)
- Skybox z cubemapą złożoną z 6 tekstur
- Obsługa tekstur w formacie PPM
