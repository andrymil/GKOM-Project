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

# GKOM - Billboarding (Etap 2)

## Zakres etapu 2

W tym etapie zrealizowano wymagania:

- **Wczytywanie skyboxa** (cubemap z 6 tekstur).
- **Obracanie płaskich obiektów** (billboardy testowe).

## Co zostało zrobione

- Dodano klasę `Skybox` w `src/skybox.py`:
  - ładowanie 6 tekstur cubemapy (`GL_TEXTURE_CUBE_MAP`),
  - utworzenie siatki sześcianu (36 wierzchołków),
  - render skyboxa z poprawną obsługą depth buffer (nie zasłania obiektów sceny).
- Dodano shadery skyboxa:
  - `shaders/skybox.vert`,
  - `shaders/skybox.frag`.
- Dodano model płaski `models/plane.obj`.
- Dodano testowe tekstury skyboxa `textures/skybox/*.ppm` (6 ścian).
- W `src/app.py`:
  - podpięto renderowanie skyboxa do pętli renderującej,
  - dodano dwa obracające się obiekty typu plane,
  - dodano klawisz **R** (pauza/wznowienie obrotu bez resetu pozycji).

## Jak sprawdzić funkcje z etapu 2

1. Uruchom program (`python main.py` lub `uv run main.py`).
2. Sprawdź, że kamera znajduje się wewnątrz sześcianu skyboxa (różne kolory ścian).
3. Poruszaj się kamerą – skybox powinien pozostać tłem niezależnie od ruchu.
4. Obserwuj dwa płaskie obiekty (plane) – powinny obracać się płynnie.
5. Wciśnij **R** – obrót powinien się zatrzymać, ponowne **R** wznawia animację od tego samego kąta.
