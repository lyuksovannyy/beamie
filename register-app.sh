#!/usr/bin/env bash
set -e

# Detect if the binary beamie is placed in a /bin directory
BINARY_PATH=""
for path in "/usr/local/bin/beamie" "/usr/bin/beamie" "/bin/beamie"; do
  if [ -f "$path" ]; then
    BINARY_PATH="$path"
    break
  fi
done

echo "Found beamie binary at: $BINARY_PATH"

# Setup the icon path
ICON_SRC="$(dirname "$0")/logo.png"
if [ ! -f "$ICON_SRC" ]; then
  ICON_SRC="/home/lebron/PyCharmProjects/beamie/logo.png"
fi

ICON_DST=""
if [ -w "/usr/share/pixmaps" ]; then
  ICON_DST="/usr/share/pixmaps/beamie.png"
  cp "$ICON_SRC" "$ICON_DST"
  echo "Installed system-wide icon to: $ICON_DST"
else
  mkdir -p "$HOME/.local/share/icons"
  ICON_DST="$HOME/.local/share/icons/beamie.png"
  cp "$ICON_SRC" "$ICON_DST"
  echo "Installed user-space icon to: $ICON_DST"
fi

# Define Desktop Entry target
DESKTOP_DIR="$HOME/.local/share/applications"
if [ "$EUID" -eq 0 ] && [ -w "/usr/share/applications" ]; then
  DESKTOP_DIR="/usr/share/applications"
fi

mkdir -p "$DESKTOP_DIR"
DESKTOP_FILE="$DESKTOP_DIR/beamie.desktop"

# Create Desktop entry file
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Type=Application
Name=Beamie
Comment=PipeWire Desktop Router and Media Streamer
Exec=$BINARY_PATH
Icon=$ICON_DST
Terminal=false
Categories=Utility;AudioVideo;Audio;
EOF

chmod +x "$DESKTOP_FILE"
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo "Success! Registered Beamie as a desktop application."
echo "Entry file created at: $DESKTOP_FILE"
echo "Launch target: $BINARY_PATH"
