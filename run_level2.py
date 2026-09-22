import subprocess, sys
steps=['tools.analytics','tools.heatmap','tools.team_heatmap','tools.player_distance','tools.speed_analysis']
for mod in steps:
    print(f'\n=== {mod} ==='); subprocess.run([sys.executable,'-m',mod],check=False)
print('\nVideo overlays: python -m tools.trajectory_video')
print('               python -m tools.match_stats_video')
