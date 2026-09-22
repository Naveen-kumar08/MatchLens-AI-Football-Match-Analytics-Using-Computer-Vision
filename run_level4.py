import subprocess, sys
steps=['tools.camera_motion_compensation','tools.dynamic_calibration','tools.event_detection','tools.automated_report','tools.ai_insights','tools.robust_realtime_video']
for mod in steps:
    print(f'\n=== {mod} ==='); subprocess.run([sys.executable,'-m',mod],check=False)
