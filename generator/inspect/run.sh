#!/bin/bash
# Helper used by lgen.py to ask the real Logisim for component port positions.
# Build once:  javac -cp $LOGISIM_JAR Inspect.java
DIR="$(cd "$(dirname "$0")" && pwd)"
exec java -Djava.awt.headless=true -cp "$LOGISIM_JAR:$DIR" Inspect "$@"
