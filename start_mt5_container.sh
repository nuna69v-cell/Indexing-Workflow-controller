#!/bin/bash
set -e

echo "Starting Xvfb on :99..."
Xvfb :99 -screen 0 1024x768x16 &
sleep 2

export DISPLAY=:99
export WINEPREFIX=/app/.wine

echo "Checking if wine is initialized..."
if [ ! -d "/app/.wine" ]; then
  echo "Setting up wine..."
  wineboot --init
  sleep 5
fi

echo "Checking if MT5 is installed..."
MT5_DIR="/app/.wine/drive_c/Program Files/MetaTrader 5"
if [ ! -d "$MT5_DIR" ]; then
  echo "MT5 is not installed, but terminal64.exe should be present in the container."
  # If we have a local installation in our home directory, let's copy it (mostly for testing setup)
  if [ -d "/home/jules/.wine/drive_c/Program Files/MetaTrader 5" ]; then
     echo "Copying MT5 from home directory for local development test..."
     mkdir -p "$MT5_DIR"
     cp -r "/home/jules/.wine/drive_c/Program Files/MetaTrader 5/"* "$MT5_DIR/"
  fi
fi


if [ -f "$MT5_DIR/terminal64.exe" ]; then
  echo "Running terminal64.exe..."
  # If common.ini doesn't exist in the target, copy from our initialized one
  if [ ! -f "$MT5_DIR/Config/common.ini" ] && [ -f "/home/jules/.wine/drive_c/Program Files/MetaTrader 5/Config/common.ini" ]; then
      mkdir -p "$MT5_DIR/Config"
      cp "/home/jules/.wine/drive_c/Program Files/MetaTrader 5/Config/common.ini" "$MT5_DIR/Config/common.ini"
  fi

  # Run MT5 in portable mode
  wine "$MT5_DIR/terminal64.exe" /portable &

  # Start the python API server
  if [ -f "scripts/genx_24_7_service.py" ]; then
     echo "Starting Python API Service..."
     python3 scripts/genx_24_7_service.py &
  fi

else
  echo "terminal64.exe not found. Setup failed."
fi

echo "running OS by 'Jules' program that allowe agent continuously running in Cloud and sandbox network"
echo "Keeping container alive..."
while true; do sleep 3600; done
