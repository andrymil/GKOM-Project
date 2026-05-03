# GKOM - Billboarding (Etap 1)

## Zrealizowane funkcjonalności

- Inicjalizacja i obsługa okna za pomocą GLFW.
- Własny parser plików `.obj` (wczytywanie wierzchołków i wektorów normalnych).
- Pełne cieniowanie Phonga (Ambient, Diffuse, Specular) realizowane w shaderach.
- Kamera typu "Fly/FPS" pozwalająca na swobodne poruszanie się po scenie.
- Niezależne transformacje obiektów na scenie (translacja, rotacja, skalowanie).

## Instalacja

Aby pobrać niezbędne biblioteki należy wykonać poniższą komendę:

`pip install -r requirements.txt`

Można również skorzystać z uv (`pip install uv`):

`uv sync`

## Uruchomienie i sterowanie

Aby uruchomić program, należy wykonać główny plik z poziomu konsoli:
`python main.py`

lub za pomocą uv:
`uv run main.py`

**Sterowanie:**

- **W / S / A / D** - Poruszanie się (Przód / Tył / Lewo / Prawo)
- **Spacja** - Lot w górę
- **Lewy Shift** - Lot w dół
- **Mysz** - Rozglądanie się (obrót kamery)
- **ESC** - Wyjście z programu
