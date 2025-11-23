# Computer Vision Detection App

A Flask-based web application for real-time object detection using OpenCV DNN with webcam preview, canvas overlay, and text-to-speech support.

## Features

- **Real-time Webcam Detection**: Capture frames from webcam and detect objects every 1 second
- **OpenCV DNN Support**: Uses MobileNet-SSD model for accurate detection (fallback to mock mode)
- **Canvas Overlay**: Draws bounding boxes and labels on detected objects
- **Text-to-Speech**: Optional TTS announcements with 3-second debouncing
- **Mock Mode**: Works without model files using simulated detections
- **Demo Images**: Load sample images for testing
- **Modern UI**: Clean, responsive interface with real-time stats

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use make
make install
```

### Run

```bash
# Start server
python app.py

# Or use make
make run
```

Open browser to `http://localhost:5000`

### Demo Mode

```bash
# Start and open browser automatically
make demo
```

The app will work in mock mode if model files are not present.

## Model Setup (Optional)

To use real OpenCV DNN detection:

1. Download MobileNet-SSD model files:
   - `frozen_inference_graph.pb` (model weights)
   - `ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt` (model config)

2. Place files in `models/` directory:
   ```
   models/
   ├── frozen_inference_graph.pb
   └── ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt
   ```

3. Model download sources:
   - OpenCV extra testdata repository
   - TensorFlow Object Detection API
   - Or use the `make download-model` command (provides instructions)

## Usage

1. **Start Camera**: Click "Start Camera" and allow browser permissions
2. **Toggle TTS**: Enable "Speak Detections" to hear detected objects
3. **Load Demo**: Click "Load Demo Image" to test with a sample image
4. **View Detections**: See bounding boxes on canvas and list below

### Mock Mode

When model files are not available, the app automatically switches to mock mode:
- Generates 1-2 random detections per frame
- Simulates common objects (person, chair, cup, laptop, etc.)
- Useful for testing UI and functionality without model setup

## Project Structure

```
cv-app/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Frontend HTML/JS
├── static/               # Static assets (images, videos)
│   ├── demo1.jpg
│   ├── demo2.jpg
│   └── demo_video.mp4
├── models/               # Model files (optional)
├── uploads/             # Temporary uploads
├── requirements.txt     # Dependencies
├── Makefile             # Commands
├── Dockerfile           # Container config
└── README.md            # This file
```

## Docker

### Build

```bash
docker build -t cv-app .
```

### Run

```bash
# With camera access (Linux)
docker run -p 5000:5000 --device=/dev/video0 cv-app

# Or use make
make docker-build
make docker-run
```

## API Endpoints

- `GET /` - Main page with webcam interface
- `POST /detect` - Process image frame, returns detections
- `GET /mode` - Get current detection mode (mock/DNN)
- `GET /static/<filename>` - Serve static files

## Detection Response

```json
{
  "detections": [
    {
      "label": "person",
      "confidence": 0.87,
      "bbox": [100, 150, 200, 300]
    }
  ],
  "latency_ms": 45,
  "mock_mode": false
}
```

## Browser Compatibility

- **Chrome/Edge**: Full support (webcam, TTS, canvas)
- **Firefox**: Full support
- **Safari**: Limited (may need HTTPS for webcam)

## Development

### Testing Mock Mode

The app automatically uses mock mode when model files are missing. This allows testing:
- UI components
- Canvas drawing
- TTS functionality
- API responses

### Adding Demo Images

Place images in `static/` directory:
```bash
# Create sample images
mkdir -p static
# Add your demo images (demo1.jpg, demo2.jpg, etc.)
```

## Troubleshooting

### Camera Not Working
- Ensure browser has camera permissions
- Try HTTPS (required on some browsers)
- Check browser console for errors

### Model Not Loading
- Verify model files are in `models/` directory
- Check file permissions
- App will fallback to mock mode automatically

### TTS Not Speaking
- Check browser TTS support (`speechSynthesis`)
- Ensure detections are being found
- TTS is debounced (3 seconds between same detection)

## License

MIT


