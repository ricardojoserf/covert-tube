#!/bin/bash
pyinstaller --onefile main.py
rm *png *avi Pipfile /tmp/*png /tmp/*mp4 /tmp/*txt
rm -rf __pycache__
cp dist/main c2ctube
rm -rf dist build
rm main.spec
