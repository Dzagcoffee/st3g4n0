# st3g4n0 — стеганография в изображениях и аудио

Здесь показаны классические и современные методы сокрытия информации в данных: изображениях и аудиофайлах.

---

## Структура проекта

```
input_data/         # Исходные данные
├── big_secret.txt  # Крупное текстовое сообщение
├── small_secret.txt # Короткое сообщение для тестов
├── img.png         # Оригинальное цветное изображение
├── gs_img.png      # Ч/б изображение (градации серого)
├── KINO.wav        # Оригинальный аудиофайл
├── KINO_FULL.wav   # Длинная версия аудиофайла
│
output_data/        # Результаты работы алгоритмов
└── gan_out.png     # Пример результата GAN-встраивания
│
src/                # Исходный код методов
├── st3g4n0_lsb_img.py   # LSB-встраивание в изображение
├── st3g4n0_lsb_snd.py   # LSB-встраивание в аудио
├── st3g4n0_dct_img.py   # Частотный метод (DCT) для изображений
├── st3g4n0_gan_img.py   # Нейросетевой (GAN) метод
└── compare.py           # Побайтовое сравнение и тепловая карта различий
```

---

## Подготовка к запуску

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Методы

| Файл | Метод | Описание |
|------|--------|-----------|
| `st3g4n0_lsb_img.py` | **LSB Matching** | Пространственное внедрение в младшие биты пикселей |
| `st3g4n0_dct_img.py` | **DCT-встраивание** | Изменение среднечастотных коэффициентов блоков 8×8 |
| `st3g4n0_lsb_snd.py` | **LSB Audio** | Встраивание в звуковые сэмплы WAV |
| `st3g4n0_gan_img.py` | **GAN-based Steganography** | Встраивание сообщения с помощью генеративной модели |
| `compare.py` | **Diff-анализ** | Визуализация различий и тепловая карта изменений |

---

## Примеры использования

### Встраивание текста в изображение (LSB)
Встраивание:
```bash
python src/st3g4n0_lsb_img.py encode -i input_data/img.png -o output_data/lsb_img/after.png -m input_data/small_secret.txt
```

Извлечение:
```bash
python src/st3g4n0_lsb_img.py decode -i output_data/lsb_img/after.png -o output_data/resuls_lsb_img_big_secret.txt
```

Для примера.
1. Картинка ДО:
<p align="center"> <img width="800" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/lsb_img/before.png"/> </p>

2. Картинка ПОСЛЕ:
<p align="center"> <img width="800" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/lsb_img/after.png"/> </p>

3. Встроенное и декодированные сообщение: (файл resuls_lsb_img_big_secret.txt)
4. Отличия картинок (тепловая карта):
<p align="center"> <img width="800" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/lsb_img/diff_heatmap.png"/> </p>

---

### Скрытие данных через DCT
Встраивание:
```bash
python src/st3g4n0_lsb_img.py encode -i input_data/img.png -o output_data/dct_gs_img/after.png -m input_data/big_secret.txt
```

Извлечение:
```bash
python src/st3g4n0_lsb_img.py decode -i output_data/dct_gs_img/after.png -o output_data/resuls_dct_img_big_secret.txt
```

Для примера.
1. Картинка ДО:
<p align="center"> <img width="800" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/dct_gs_img/before.png"/> </p>

2. Картинка ПОСЛЕ:
<p align="center"> <img width="800" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/dct_gs_img/after.png"/> </p>

3. Встроенное и декодированные сообщение: (файл resuls_lsb_img_big_secret.txt)
4. Отличия картинок (тепловая карта):
   <p align="center"> <img width="800" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/dct_gs_img/diff_heatmap.png"/> </p>
5. Отличия в выходах ДКП:
   - До:
     <p align="center"> <img width="520" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/dct_gs_img/stego_dct_before.png"/> </p>
   - После:
     <p align="center"> <img width="520" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/dct_gs_img/stego_dct_after.png"/> </p>
   - Отличия:
     <p align="center"> <img width="520" src="https://github.com/Dzagcoffee/st3g4n0/blob/main/output_data/dct_gs_img/stego_dct_diff.png"/> </p>
  
---

### Встраивание в аудио
Встраивание:
```bash
python src/st3g4n0_lsb_snd.py encode -i input_data/KINO.wav -o output_data/lsb_snd/after.png -m input_data/small_secret.txt
```

Извлечение:
```bash
python src/st3g4n0_lsb_img.py decode -i output_data/lsb_snd/after.png -o output_data/resuls_lsb_snd_small_secret.txt
```

---

### Встраивание c помощью GAN (энкодинг + декодинг одновременно)
```bash
python src/st3g4n0_gan_img.py
```

---

### Анализ изменений
```bash
python src/compare.py
```

Покажет:
- процент изменённых пикселей и бит;
- карту различий;
- тепловую карту активности изменений.
