# Quick Start Guide

This guide will help you set up and run both the Flask inference API and the React Native client.

## Prerequisites

### For Flask API:
- Python 3.8+
- pip

### For React Native Client:
- Node.js 14+
- npm or yarn
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac) or Android Emulator, or Expo Go app on physical device

## Step 1: Set Up Flask API

1. Navigate to the inference API directory:
```bash
cd inference-api
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the Flask server:
```bash
python run.py
```

The server will start on `http://localhost:5000`

5. Test the health endpoint:
```bash
curl http://localhost:5000/health
```

Expected response: `{"ok":true}`

6. (Optional) Test inference with an image:
```bash
# First, create a tests directory and add a sample image
mkdir -p tests
# Add a sample.jpg to tests/ directory, then:
curl -F frame=@tests/sample.jpg http://localhost:5000/infer
```

## Step 2: Set Up React Native Client

1. Navigate to the React Native client directory:
```bash
cd ../react-native-client
```

2. Install dependencies:
```bash
npm install
```

3. Start Expo development server:
```bash
npm start
# or
expo start
```

4. Run on your device:
   - **iOS**: Press `i` in terminal or scan QR with Camera app
   - **Android**: Press `a` in terminal or scan QR with Expo Go app
   - **Web**: Press `w` in terminal (limited functionality)

## Step 3: Connect Client to Server

### Option A: Same Machine (Localhost)

1. If running on iOS Simulator or Android Emulator on the same machine:
   - In the app settings, set Server URL to: `http://localhost:5000`
   - Or for Android emulator, use: `http://10.0.2.2:5000`

### Option B: Local Network (Physical Device)

1. **Find your computer's local IP address:**
   ```bash
   # Mac/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Windows
   ipconfig
   ```
   Look for an IP like `192.168.1.100`

2. **Update Flask server to listen on all interfaces** (already configured with `host='0.0.0.0'`)

3. **In the React Native app:**
   - Tap "Settings"
   - Set Server URL to: `http://YOUR_IP:5000` (e.g., `http://192.168.1.100:5000`)

4. **Make sure both devices are on the same Wi-Fi network**

5. **Test the connection:**
   - In the app, tap "Test" button
   - You should hear TTS and feel vibration (if enabled)
   - Check Flask server terminal for inference requests

## Step 4: Testing

### Test Flask API Independently

```bash
# Health check
curl http://localhost:5000/health

# Inference (requires an image file)
curl -F frame=@path/to/image.jpg http://localhost:5000/infer
```

### Test React Native App

1. **Test Mode**: Tap "Test" button - should trigger TTS and vibration
2. **Demo Mode**: Tap "Demo Mode" - simulates detections without backend
3. **Live Mode**: Make sure Flask server is running, point camera at objects

## Troubleshooting

### Flask API Issues

**Port already in use:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
```

**Module not found:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### React Native Client Issues

**Cannot connect to server:**
- Verify Flask server is running
- Check Server URL in app settings
- Ensure both devices are on same network
- Check firewall settings

**Camera not working:**
- Grant camera permissions in device settings
- Restart the app after granting permissions

**No detections:**
- Lower confidence threshold in settings
- Check Flask server logs for errors
- Try demo mode first to isolate the issue

## Using Docker (Optional)

### Build and Run Flask API with Docker

```bash
cd inference-api
docker build -t inference-api .
docker run -p 5000:5000 inference-api
```

## Next Steps

- Customize detection logic in `inference-api/app/routes.py`
- Adjust frame capture interval in `react-native-client/App.js`
- Modify TTS messages and thresholds in app settings
- Add more detection labels/types
- Integrate with a real ML model

## Architecture Overview

```
┌─────────────────┐         HTTP POST           ┌──────────────┐
│  React Native   │  ────────────────────────>  │  Flask API   │
│     Client      │  <────────────────────────  │  (Inference) │
│                 │      JSON Response          │              │
└─────────────────┘                             └──────────────┘
       │                                                │
       │ Camera (750ms)                                │ OpenCV
       │ TTS                                           │ Mock CNN
       │ Vibration                                     │ Detections
       │                                               │
```

## Support

For detailed documentation, see:
- Flask API: `inference-api/README.md`
- React Native Client: `react-native-client/README.md`


