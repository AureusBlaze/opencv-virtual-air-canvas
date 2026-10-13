# 🎨 OpenCV Virtual Air Canvas: Real-Time Color & Gesture Tracking

An interactive Computer Vision application built with **OpenCV** and **NumPy** that turns your webcam into a virtual digital whiteboard. Draw, sketch, and take notes in mid-air using any colored physical object (pen cap, marker, or colored pointer) with zero touch hardware required.

---

## 📌 Features

- **Real-Time Mid-Air Drawing**: Track and render continuous freehand brush strokes directly over your webcam stream.
- **Exponential Moving Average (EMA) Jitter Filter**: Filters out sensor noise and natural hand tremors for smooth, fluid digital ink.
- **Live Color Calibrator Utility**: Built-in GUI tool with HSV trackbars to dial in color thresholds for any marker under any lighting condition.
- **On-Screen Heads-Up Display (HUD)**: Interactive controls and instructions rendered cleanly onto the video feed.
- **Fullscreen & Canvas Reset**: One-touch controls to toggle fullscreen presentation or clear the canvas.

---

## 🧠 Computer Vision Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌────────────────┐     ┌────────────────┐
│ Webcam Feed  │ ──► │ BGR ➔ HSV    │ ──► │ HSV Threshold  │ ──► │ Morphological  │
│ (Mirrored)   │     │ Conversion   │     │ (Color Mask)   │     │ Noise Cleaning │
└──────────────┘     └──────────────┘     └────────────────┘     └───────┬────────┘
                                                                         │
┌──────────────┐     ┌──────────────┐     ┌────────────────┐             │
│ On-Screen    │ ◄── │ Stroke       │ ◄── │ EMA Centroid   │ ◄───────────┘
│ Air Canvas   │     │ Buffer Deque │     │ Smoothing      │
└──────────────┘     └──────────────┘     └────────────────┘
```

1. **Camera Mirroring**: Mirrors incoming frames (`cv2.flip(frame, 1)`) to mirror natural human movement.
2. **HSV Color Segmentation**: Converts frames to Hue-Saturation-Value color space to isolate color frequency from room lighting changes.
3. **Morphological Noise Removal**: Applies erosion (`cv2.erode`, 6 passes) to discard stray pixels followed by dilation (`cv2.dilate`, 3 passes) to reinforce the object silhouette.
4. **Centroid Calculation via Moments**: Calculates spatial moments to extract the exact centroid of the tracked object:
   $$C_x = \frac{M_{10}}{M_{00}}, \quad C_y = \frac{M_{01}}{M_{00}}$$
5. **Jitter Reduction (Exponential Moving Average)**:
   $$S_t = \alpha \cdot X_t + (1 - \alpha) \cdot S_{t-1} \quad (\alpha = 0.2)$$
   Smooths out camera frame-to-frame variance for clean handwriting.
6. **Stroke Persistence**: Maintains point trajectories in a `collections.deque` buffer and renders contiguous antialiased lines.

---

## ⌨️ Controls

| Key | Action |
|:---:|:---|
| <kbd>C</kbd> | **Clear Canvas** — Wipes the board clean |
| <kbd>F</kbd> | **Toggle Fullscreen** — Switch between windowed and fullscreen presentation |
| <kbd>Q</kbd> | **Quit** — Release camera and close application |

---

## 📁 Repository Structure

```
opencv-virtual-air-canvas/
├── .gitignore               # Ignores Python caches and virtual environments
├── README.md                # System documentation & pipeline breakdown
├── requirements.txt         # Dependencies (opencv-python, numpy)
├── main.py                  # Primary interactive Air Canvas application
├── color_calibrator.py      # HSV trackbar utility to calibrate custom markers
└── legacy/                  # Early development prototypes & experiments
    ├── VAC.py
    └── Virtual-Air-Canvas.py
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AureusBlaze/opencv-virtual-air-canvas.git
cd opencv-virtual-air-canvas
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Air Canvas
```bash
python main.py
```

---

## 🎛️ Calibrating for Any Marker or Lighting

If you want to track a different object (e.g. green marker, red cap, orange ball), run the calibration tool:

```bash
python color_calibrator.py
```

1. Adjust the **Hue**, **Saturation**, and **Value** sliders until your pointer appears **pure WHITE** on the mask and the background is **BLACK**.
2. Press <kbd>Q</kbd>. The console will print your optimal numpy values:
   ```python
   blueLower = np.array([H_min, S_min, V_min])
   blueUpper = np.array([H_max, S_max, V_max])
   ```
3. Update the values in `main.py` lines 26–27.

---

## 🛠️ Tech Stack
- **Python 3.x**
- **OpenCV (`cv2`)** (Image processing, contour tracking & GUI widgets)
- **NumPy** (Matrix manipulations & HSV arrays)
