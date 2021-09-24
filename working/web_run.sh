gnome-terminal -- python3 send_test.py
sleep 0.5
xdotool key Super_L+Left

sleep 1
gnome-terminal -- python3 recieve_test.py
sleep 0.5
xdotool key Super_L+Right
sleep 0.5
xdotool key Alt_L+Tab
