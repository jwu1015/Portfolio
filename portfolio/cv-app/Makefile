.PHONY: run lint demo install clean docker-build docker-run download-model

run:
	python app.py

lint:
	flake8 app.py || true
	pylint app.py || true

demo:
	@echo "Starting server in demo mode..."
	@python app.py &
	@sleep 2
	@echo "Opening browser..."
	@open http://localhost:5000 || xdg-open http://localhost:5000 || start http://localhost:5000

install:
	pip install -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf uploads/*

docker-build:
	docker build -t cv-app .

docker-run:
	docker run -p 5000:5000 --device=/dev/video0 cv-app

download-model:
	@echo "Downloading MobileNet-SSD model..."
	@mkdir -p models
	@echo "Please download the model from:"
	@echo "https://github.com/opencv/opencv_extra/raw/master/testdata/dnn/frozen_inference_graph.pb"
	@echo "https://github.com/opencv/opencv_extra/raw/master/testdata/dnn/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
	@echo "Or use the TensorFlow Object Detection API to export a model"


