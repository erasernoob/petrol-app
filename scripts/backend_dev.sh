#!/bin/bash
cd src/api

source venv/Scripts/activate

uvicorn backend_main:app --reload
