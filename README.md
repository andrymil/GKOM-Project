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
- **Billboarding w 2 wersjach**:
  - axial (scena `trees`),
  - world-oriented (scena `clouds`).
- **Przełączanie scen argumentem konsoli**.
- **Zatrzymanie obrotu billboardów klawiszem `R`**.

## Co zostało zrobione

- Dodano klasę `Skybox` w `src/skybox.py`:
  - ładowanie 6 tekstur cubemapy (`GL_TEXTURE_CUBE_MAP`),
  - utworzenie siatki sześcianu (36 wierzchołków),
  - render skyboxa z poprawną obsługą depth buffer (nie zasłania obiektów sceny).
- Dodano shadery skyboxa:
  - `shaders/skybox.vert`,
  - `shaders/skybox.frag`.
- Dodano tekstury obiektów:
  - `textures/tree.ppm`,
  - `textures/cloud.ppm`.
- Dodano model billboardu `models/billboard.obj`.
- Dodano proste krajobrazowe tekstury skyboxa `textures/skybox/*.ppm` (6 ścian: niebo, las, ziemia).
- W `src/app.py`:
  - podpięto renderowanie skyboxa do pętli renderującej,
  - dodano obliczanie macierzy billboardów:
    - `_axial_billboard_matrix(...)`,
    - `_world_oriented_billboard_matrix(...)`,
  - dodano dwie sceny billboardowe (`trees`, `clouds`),
  - dodano pauzę/wznowienie obrotu billboardów względem kamery (`R`).
- W `main.py`:
  - dodano wybór sceny z argumentu konsoli:
    - `python main.py trees`,
    - `python main.py clouds`.

## Jak sprawdzić funkcje z etapu 2

1. Uruchom scenę z billboardami axial: `python main.py trees`.
2. Uruchom scenę z billboardami world-oriented: `python main.py clouds`.
3. W obu scenach sprawdź, że skybox poprawnie otacza kamerę.
4. W scenie `trees` billboardy obracają się tylko wokół osi pionowej (Y).
5. W scenie `clouds` billboardy pełniej orientują się względem kamery.
6. Wciśnij `R` i porusz kamerą: billboardy powinny być chwilowo "zamrożone".
