import subprocess, sys
steps=['tools.ball_tracking_improved','tools.player_ball_relationship','tools.possession','tools.passing_analysis','tools.formations','tools.tactical_shape','tools.player_positioning','tools.advanced_movement']
for mod in steps:
    print(f'\n=== {mod} ==='); subprocess.run([sys.executable,'-m',mod],check=False)
