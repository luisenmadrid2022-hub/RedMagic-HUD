#!/bin/sh

# Gradle wrapper - descarga e instala Gradle automaticamente
GRADLE_VERSION="8.11.1"
GRADLE_DIR="$HOME/.gradle/wrapper/dists"
GRADLE_URL="https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip"

# Determinar directorio del proyecto
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
GRADLE_HOME="$PROJECT_DIR/.gradle"

# Descargar Gradle si no existe
if [ ! -f "$GRADLE_HOME/gradle-${GRADLE_VERSION}/bin/gradle" ]; then
    echo "Downloading Gradle ${GRADLE_VERSION}..."
    mkdir -p "$GRADLE_HOME"
    cd "$GRADLE_HOME"
    curl -sL "$GRADLE_URL" -o gradle.zip
    unzip -q gradle.zip
    rm gradle.zip
fi

export PATH="$GRADLE_HOME/gradle-${GRADLE_VERSION}/bin:$PATH"
exec gradle -p "$PROJECT_DIR" "$@"
