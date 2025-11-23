---
title: "Computer Vision Detection App"
date: "2025-01-15"
summary: "Real-time object detection web app using Flask, OpenCV DNN, and HTML5 Canvas with TTS accessibility features"
tags: ["python", "flask", "opencv", "computer-vision", "html5", "accessibility"]
cover: "/images/projects/cv-detection-cover.jpg"
links:
  demo: "https://cv-app-demo.netlify.app"
  code: "https://github.com/yourusername/Portfolio/tree/main/cv-app"
published: true
---

Built a production-ready Flask web application that transforms any webcam feed into a real-time object detection studio. The system integrates MobileNet-SSD via OpenCV DNN for accurate detection, with a graceful fallback to mock mode when model files are absent—ensuring the app works out of the box for demos and testing. The frontend uses HTML5 Canvas for bounding box overlays and Web Speech API for accessibility, with smart debouncing to prevent TTS spam. The result is a polished, accessible tool that demonstrates how computer vision can enhance user experiences while maintaining developer-friendly deployment workflows.

**Key Features:**
- Real-time frame capture (1-second intervals) with OpenCV DNN integration
- Mock detection mode for testing without ML model dependencies
- Canvas-based visualization with labels and confidence scores
- Text-to-speech announcements with 3-second debouncing
- Docker support and Makefile-driven workflows
- Responsive UI with latency and FPS monitoring

**My Role:** Full-stack developer, UX designer

**Impact:** Delivered a complete, deployable system that works in both production (with models) and demo scenarios (mock mode), making it easy for teams to evaluate computer vision capabilities without infrastructure overhead.

