#!/bin/sh
GRADLE_HOME=$(dirname "$0")
export GRADLE_HOME
exec "$GRADLE_HOME/gradlew" "$@"
