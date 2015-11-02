#!/bin/bash
find . -prune -o -name "*.pyc" -print -o -name "__pycache__" -print | xargs rm -rf