# See https://www.raspberrypi.org/documentation/usage/audio/#:~:text=documentation%20%3E%20usage%20%3E%20audio-,Playing%20audio%20on%20the%20Raspberry%20Pi,described%20in%20more%20detail%20here.&text=This%20will%20play%20the%20audio,connected%20via%20the%20headphone%20jack.

# omxplayer -o local example.mp3  # Forces to use local output jack

# Headless background version (letting output port be autodetected - hopefully headphone jack)
# Add '-o local' if needed
#omxplayer --no-keys example.mp3 &
while true; do
    omxplayer --no-keys mp3s/example.mp3
done

# A test tool
# speaker-test -t wav -c 2
