#!/bin/bash

tmate -S /tmp/tmate.sock new-session -d
tmate -S /tmp/tmate.sock wait tmate-ready

echo "SSH connection available:"
tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'

# giữ container chạy
tail -f /dev/null