from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import numpy as np
import os
import logging
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Detection model paths
MODEL_CONFIG = 'models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
MODEL_WEIGHTS = 'models/frozen_inference_graph.pb'
CLASSES_FILE = 'models/coco.names'

# COCO class names (first 20 for brevity, full list available)
COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
    'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
    'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

# Initialize detector
detector = None
mock_mode = True

def load_detector():
    """Load OpenCV DNN detector or set mock mode"""
    global detector, mock_mode
    
    if os.path.exists(MODEL_WEIGHTS) and os.path.exists(MODEL_CONFIG):
        try:
            detector = cv2.dnn.readNetFromTensorflow(MODEL_WEIGHTS, MODEL_CONFIG)
            mock_mode = False
            logger.info("OpenCV DNN model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load model: {e}. Using mock mode.")
            mock_mode = True
    else:
        logger.info("Model files not found. Using mock detection mode.")
        mock_mode = True

def mock_detect(frame):
    """Generate mock detections for demo"""
    height, width = frame.shape[:2]
    detections = []
    
    # Generate 1-2 random detections
    num_detections = np.random.randint(1, 3)
    
    common_classes = ['person', 'chair', 'cup', 'laptop', 'bottle', 'cell phone']
    
    for _ in range(num_detections):
        # Random bbox
        x = np.random.randint(0, width // 2)
        y = np.random.randint(0, height // 2)
        w = np.random.randint(50, min(200, width - x))
        h = np.random.randint(50, min(200, height - y))
        
        # Random class
        class_name = np.random.choice(common_classes)
        confidence = np.random.uniform(0.7, 0.95)
        
        detections.append({
            'label': class_name,
            'confidence': round(confidence, 2),
            'bbox': [int(x), int(y), int(w), int(h)]
        })
    
    return detections

def dnn_detect(frame):
    """Detect objects using OpenCV DNN"""
    height, width = frame.shape[:2]
    
    # Prepare input blob
    blob = cv2.dnn.blobFromImage(frame, 1.0/127.5, (300, 300), [127.5, 127.5, 127.5], swapRB=True, crop=False)
    detector.setInput(blob)
    
    # Run inference
    detections = detector.forward()
    
    results = []
    
    # Process detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.5:  # Confidence threshold
            class_id = int(detections[0, 0, i, 1])
            if class_id < len(COCO_CLASSES):
                # Get bbox coordinates
                x1 = int(detections[0, 0, i, 3] * width)
                y1 = int(detections[0, 0, i, 4] * height)
                x2 = int(detections[0, 0, i, 5] * width)
                y2 = int(detections[0, 0, i, 6] * height)
                
                results.append({
                    'label': COCO_CLASSES[class_id],
                    'confidence': round(float(confidence), 2),
                    'bbox': [x1, y1, x2 - x1, y2 - y1]
                })
    
    return results

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html', mock_mode=mock_mode)

@app.route('/detect', methods=['POST'])
def detect():
    """Process image and return detections"""
    try:
        if 'frame' not in request.files:
            return jsonify({'error': 'No frame provided'}), 400
        
        file = request.files['frame']
        if file.filename == '':
            return jsonify({'error': 'Empty file'}), 400
        
        # Read image
        nparr = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image'}), 400
        
        # Run detection
        start_time = datetime.now()
        
        if mock_mode:
            detections = mock_detect(frame)
        else:
            detections = dnn_detect(frame)
        
        latency_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return jsonify({
            'detections': detections,
            'latency_ms': latency_ms,
            'mock_mode': mock_mode
        }), 200
        
    except Exception as e:
        logger.error(f"Detection error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/mode', methods=['GET'])
def get_mode():
    """Get current detection mode"""
    return jsonify({'mock_mode': mock_mode}), 200

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# Initialize detector on startup
load_detector()

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)


