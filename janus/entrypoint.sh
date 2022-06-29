#!/bin/bash

#nohup ffmpeg -f v4l2 -thread_queue_size 8192 -input_format yuyv422 -video_size 1280x720 -framerate 10 -i /dev/video0 -c:v h264 -profile:v baseline -b:v 1M -bf 0 -flags:v +global_header -bsf:v "dump_extra=freq=keyframe" -max_delay 0 -an -bufsize 1M -vsync 1 -g 10 -f rtp rtp://0.0.0.0:8004/ > /dev/null 2>&1 &
/opt/janus/bin/janus