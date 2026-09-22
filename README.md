# ⚽ MatchLens AI – Football Match Analytics Using Computer Vision

> An AI-powered football video analytics system that uses Computer Vision, YOLO, OpenCV, object tracking, team classification, and tactical analysis to transform raw football match video into player-level and team-level insights.

---

## 📌 Project Overview

**MatchLens AI** is a computer-vision-based football analytics system designed to automatically analyze football match videos.

The system processes a match video and detects:

- ⚽ Football
- 👤 Players
- 🆔 Individual player IDs
- 🔵 Team 1 players
- 🟢 Team 2 players
- ⚪ Unknown/uncertain players
- 🏃 Player movement
- 📍 Player positions
- 📏 Distance travelled
- 💨 Player speed
- 🔥 Heatmaps
- 🧭 Player trajectories
- 🧠 Tactical positioning
- 🏟️ Team formations
- ⚽ Player-ball relationships
- 🎯 Passing candidates
- 📊 Possession estimation
- 📈 Match statistics
- 🤖 AI-based match insights

The final system generates an annotated dashboard-style football analytics video containing both the original match footage and analytical information.

---

# 🎯 Objectives

The main objectives of MatchLens AI are:

1. Automatically detect players and the football from match footage.
2. Track players across video frames using persistent IDs.
3. Identify players belonging to different teams.
4. Convert image coordinates into real-world football-pitch coordinates.
5. Calculate player movement and distance travelled.
6. Estimate player speed.
7. Generate player and team heatmaps.
8. Visualize player trajectories.
9. Analyze player positioning and tactical shape.
10. Estimate player-ball relationships and possession.
11. Generate automated match statistics and AI-based insights.
12. Present the analysis directly inside an output video dashboard.

---

# 🧠 System Architecture

```text
                    ┌─────────────────────┐
                    │   Football Video    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   YOLO Detection    │
                    │ Players + Ball      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   ByteTrack         │
                    │ Player Tracking     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Persistent Player   │
                    │ IDs                 │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Team Classification │
                    │ KMeans + HSV        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │ Pitch Calibration│          │ Player Analytics│
       │ + Homography     │          │ Speed/Distance │
       └────────┬────────┘          └────────┬────────┘
                │                            │
                └──────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Tactical Analytics  │
                    │ Position / Heatmap  │
                    │ Formation / Shape   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Level 3 Analytics   │
                    │ Ball / Possession   │
                    │ Passing / Movement  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Level 4 Analytics   │
                    │ Events / AI Insights│
                    │ Reports / Stability │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Final Dashboard     │
                    │ Analytics Video     │
                    └─────────────────────┘
🛠️ Technologies Used
Technology	Purpose
Python	Main programming language
OpenCV	Computer vision and video processing
YOLOv8	Object detection
ByteTrack	Multi-object tracking
NumPy	Numerical computation
Pandas	Data processing and CSV analytics
Scikit-learn	KMeans team classification
Matplotlib	Heatmaps and analytical plots
PyYAML	Configuration management
Streamlit	Optional interactive interface
📂 Project Structure
MatchLens_AI/
│
├── input.mp4
│
├── config.yaml
├── requirements.txt
├── README.md
├── run.py
├── app.py
│
├── matchlens/
│   ├── __init__.py
│   ├── config.py
│   ├── homography.py
│   ├── pipeline.py
│   ├── tactical.py
│   ├── team_classifier.py
│   └── analytics.py
│
├── tools/
│   │
│   ├── extract_frame.py
│   ├── calibrate.py
│   │
│   ├── analytics.py
│   ├── heatmap.py
│   ├── team_heatmap.py
│   ├── player_distance.py
│   ├── speed_analysis.py
│   │
│   ├── analytics_video.py
│   ├── match_stats_video.py
│   ├── trajectory_video.py
│   │
│   ├── ball_tracking_improved.py
│   ├── player_ball_relationship.py
│   ├── possession.py
│   ├── passing_analysis.py
│   ├── formations.py
│   ├── tactical_shape.py
│   ├── player_positioning.py
│   ├── advanced_movement.py
│   │
│   ├── camera_motion_compensation.py
│   ├── dynamic_calibration.py
│   ├── event_detection.py
│   ├── automated_report.py
│   ├── ai_insights.py
│   ├── robust_realtime_video.py
│   │
│   ├── final_matchlens_video.py
│   ├── run_level3.py
│   └── run_level4.py
│
└── outputs/
    ├── tracks.csv
    ├── tracks_with_speed.csv
    ├── player_analytics.csv
    ├── player_heatmap.png
    ├── team1_heatmap.png
    ├── team2_heatmap.png
    ├── player_distance.png
    ├── player_speed.png
    ├── stabilized.mp4
    ├── match_report.json
    ├── ai_insights.json
    └── MatchLens_AI_Final.mp4
🚀 Installation
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/MatchLens_AI.git

Move into the project:

cd MatchLens_AI
2. Create Virtual Environment
Windows
python -m venv .venv

Activate:

.\.venv\Scripts\Activate.ps1

If PowerShell blocks activation:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then:

.\.venv\Scripts\Activate.ps1
3. Install Dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

If Matplotlib is not installed:

python -m pip install matplotlib
🎥 Input Video

Place your football video inside the project directory:

MatchLens_AI/
└── input.mp4

The system supports football match footage suitable for player detection and pitch analysis.

▶️ Running the Project
Level 1 – Basic Football Detection & Tracking

Run:

python run.py --source input.mp4 --output outputs\matchlens.mp4

This performs:

Player detection
Ball detection
Player tracking
Player IDs
Team classification
Pitch coordinate transformation
Tactical visualization
CSV generation

Main output:

outputs/matchlens.mp4
outputs/tracks.csv
🗺️ Pitch Calibration

MatchLens AI uses homography to transform image coordinates into football-pitch coordinates.

The default pitch dimensions are:

Length = 105 meters
Width  = 68 meters

Example:

pitch:
  length_m: 105.0
  width_m: 68.0

  image_points:
    - [4, 59]
    - [351, 60]
    - [348, 472]
    - [7, 469]

The four image points represent the four corners of the visible pitch region.

📍 Homography

The system converts image coordinates:

Pixel Coordinate
      ↓
Homography Transformation
      ↓
Real Pitch Coordinate
      ↓
X = meters
Y = meters

This allows player movement to be analyzed in real-world pitch coordinates instead of raw pixels.

Example:

Player Position:

Image:
x = 150 pixels
y = 250 pixels

Converted:

Pitch:
x = 42.5 meters
y = 35.2 meters
📊 Tracking CSV

The tracking pipeline generates:

outputs/tracks.csv

Example structure:

frame
track_id
class
team
x1
y1
x2
y2
pitch_x_m
pitch_y_m

Example:

frame  track_id  class   team  pitch_x_m  pitch_y_m
0      1         player  1     16.18      41.40
0      2         player  1     39.99      30.57
0      3         player  2     82.90      37.87
🏃 Level 2 – Player Analytics

Level 2 converts player tracking data into movement statistics.

Run:

python -m tools.analytics

Outputs:

outputs/tracks_with_speed.csv
outputs/player_analytics.csv
📏 Distance Calculation

Player distance is calculated from consecutive pitch positions.

Distance =
√((x₂-x₁)² + (y₂-y₁)²)

The distances are accumulated for each player.

Example:

Player ID 12
Distance = 6.84 km
💨 Speed Analysis

Speed is calculated using:

Speed = Distance / Time

and converted to:

km/h

The analytics system generates:

Average speed
Maximum speed
Total distance
Frames tracked
🔥 Player Heatmap

Run:

python tools\heatmap.py

Output:

outputs/player_heatmap.png

The heatmap represents areas where players spent more time during the analyzed footage.

🔵🟢 Team Heatmaps

Run:

python tools\team_heatmap.py

Outputs:

outputs/team1_heatmap.png
outputs/team2_heatmap.png

The two team heatmaps help visualize differences in spatial occupation.

Note: Team numbers are classifier labels. Team 1 and Team 2 may swap between different videos.

📊 Player Distance Chart

Run:

python tools\player_distance.py

Output:

outputs/player_distance.png

This displays players according to their calculated movement distance.

💨 Player Speed Chart

Run:

python tools\speed_analysis.py

Output:

outputs/player_speed.png

The chart compares:

Maximum speed
Average speed
🎬 Analytics Video

Instead of analyzing only CSV files and charts, MatchLens AI can display analytics directly on the video.

Run:

python tools\analytics_video.py

Output:

outputs/matchlens_analytics.mp4

The video can display:

Player Bounding Box
Player ID
Team
Speed
Tactical Pitch
Frame Number
📊 Live Match Statistics Video

Run:

python tools\match_stats_video.py

The output displays:

Players Detected
Team 1 Count
Team 2 Count
Unknown Count
Average Speed
Maximum Speed
Frame Number

Output:

outputs/matchlens_stats.mp4
🧭 Player Trajectory Analysis

MatchLens AI tracks player movement over time.

Run:

python -m tools.trajectory_video

Output:

outputs/matchlens_trajectory.mp4

The video displays:

Player ID
Team
Bounding Box
Speed
Movement Trajectory

Example:

       Player 12
           ↓
     ──────────────
    /              \
   /                \
  ●────●────●────●
🧠 Level 3 – Advanced Football Analytics

Level 3 extends the system from basic player statistics to football-specific tactical analysis.

Run:

python tools/run_level3.py

Or run individual modules:

python tools/ball_tracking_improved.py
python tools/player_ball_relationship.py
python tools/possession.py
python tools/passing_analysis.py
python tools/formations.py
python tools/tactical_shape.py
python tools/player_positioning.py
python tools/advanced_movement.py
⚽ Ball Tracking

The system attempts to detect and track the football using the object detector.

The ball information can be used for:

Player-ball distance
Possession estimation
Passing analysis
Ball movement
Tactical analysis
👤⚽ Player-Ball Relationship

The system calculates the relationship between players and the detected ball.

Concept:

Player Position
       +
Ball Position
       ↓
Euclidean Distance
       ↓
Nearest Player

This provides the basis for possession estimation and ball-related analysis.

🏆 Possession Estimation

Possession is estimated using player-ball proximity.

Concept:

Ball
 ↓
Nearest Player
 ↓
Player Team
 ↓
Estimated Team Possession

The output is an analytical estimate and should not be treated as official match statistics.

🎯 Passing Analysis

Passing candidates can be identified using:

Player positions
Ball movement
Distance between players
Temporal movement
Team association

The system can generate candidate passing events for further analysis.

🧩 Formation Analysis

Player pitch coordinates are used to estimate team formation.

Example:

           ST

      LW         RW

        CM   CM

   LB    CB   CB    RB

            GK

The actual formation depends on detected player positions.

🧠 Tactical Shape Analysis

Tactical shape analysis examines how players are distributed across the pitch.

Possible measurements include:

Team width
Team length
Player spacing
Average team position
Defensive shape
Attacking shape
Compactness
Spatial distribution
📍 Player Positioning

The system analyzes player locations using the calibrated pitch coordinates.

Example:

105m
┌─────────────────────────────────────┐
│                                     │
│        ●       ●                    │
│                                     │
│              ●                      │
│                                     │
│    ●                    ●           │
│                                     │
│                 ⚽                   │
│                                     │
└─────────────────────────────────────┘
              68m
🏃 Advanced Movement Analytics

Advanced movement analysis can use:

Distance
Speed
Acceleration
Position changes
Movement direction
Player trajectories
Spatial occupation

These metrics can be used to study player movement patterns.

🤖 Level 4 – Professional Analytics

Level 4 introduces additional processing for more advanced football analysis.

Run:

python tools/run_level4.py

Major components include:

Camera Motion Compensation
Dynamic Pitch Calibration
Event Detection
Automated Match Report
AI Insights
Robust Real-Time Video Analytics
🎥 Camera Motion Compensation

Football cameras can move, zoom and pan.

Camera motion compensation attempts to reduce the effect of camera movement so that player movement can be analyzed more consistently.

Pipeline:

Original Video
      ↓
Camera Motion Estimation
      ↓
Motion Compensation
      ↓
Stabilized Video

Output:

outputs/stabilized.mp4
🏟️ Dynamic Pitch Calibration

Instead of relying only on manually entered pitch points, Level 4 includes dynamic calibration functionality intended to detect pitch information from video frames.

This can help reduce the dependency on fixed camera coordinates.

🚨 Event Detection

The system can analyze tracking information for possible football events.

Potential event categories include:

Movement Events
Speed Events
Ball Events
Player-Ball Events
Team Movement Events

These should be treated as computer-vision-derived candidate events rather than official event data.

📝 Automated Match Report

MatchLens AI can generate structured match information.

Example:

{
    "players_detected": 22,
    "team_1_players": 11,
    "team_2_players": 11,
    "average_speed": 12.4,
    "maximum_speed": 28.7
}

Output:

outputs/match_report.json
🤖 AI-Based Insights

The system generates analytical insights from available tracking and match statistics.

Example insight categories:

Player Movement
Team Distribution
Speed
Spatial Occupation
Tactical Shape
Possession Estimate

Output:

outputs/ai_insights.json
📺 Final MatchLens AI Dashboard

The final project combines the available analytics into one dashboard-style video.

Run:

python tools/final_matchlens_video.py

Output:

outputs/MatchLens_AI_Final.mp4
🎨 Final Video Features

The final dashboard can display:

👤 Player Detection
┌───────────────┐
│ ID 12         │
│ TEAM 1        │
│ 14.2 km/h     │
└───────────────┘
🔵 Team 1

Blue bounding boxes and trajectories.

🟢 Team 2

Green bounding boxes and trajectories.

⚪ Unknown

Gray bounding boxes for uncertain classification.

🟡 Ball

Yellow representation for the detected ball.

🆔 Player IDs

Every tracked player receives a tracking ID.

💨 Speed

Individual player speed can be displayed alongside the player ID.

🧭 Trajectories

Player movement trails are drawn across the video.

🗺️ Tactical Pitch

A 105 × 68 meter tactical pitch displays player positions.

📊 Match Statistics

The dashboard can show:

Players Detected
Team 1
Team 2
Unknown
Average Speed
Maximum Speed
Team Spread
Top Distance Players
📁 Main Output Files

After processing, the outputs folder can contain:

File	Description
tracks.csv	Raw player and ball tracking data
tracks_with_speed.csv	Tracking data with speed
player_analytics.csv	Player-level statistics
player_heatmap.png	Overall heatmap
team1_heatmap.png	Team 1 heatmap
team2_heatmap.png	Team 2 heatmap
player_distance.png	Distance chart
player_speed.png	Speed chart
matchlens_analytics.mp4	Analytics video
matchlens_stats.mp4	Statistics overlay video
matchlens_trajectory.mp4	Trajectory video
stabilized.mp4	Stabilized video
match_report.json	Automated report
ai_insights.json	AI-derived insights
MatchLens_AI_Final.mp4	Final dashboard video
🔄 Complete Processing Pipeline
INPUT FOOTBALL VIDEO
        │
        ▼
YOLO OBJECT DETECTION
        │
        ├──────────────► Players
        │
        └──────────────► Ball
        │
        ▼
BYTETRACK
        │
        ▼
PLAYER IDs
        │
        ▼
TEAM CLASSIFICATION
        │
        ▼
PITCH CALIBRATION
        │
        ▼
HOMOGRAPHY
        │
        ▼
REAL-WORLD COORDINATES
        │
        ├──────────────► Distance
        │
        ├──────────────► Speed
        │
        ├──────────────► Heatmap
        │
        ├──────────────► Trajectory
        │
        ├──────────────► Positioning
        │
        └──────────────► Tactical Shape
        │
        ▼
BALL ANALYSIS
        │
        ├──────────────► Player-Ball Relationship
        ├──────────────► Possession Estimate
        └──────────────► Passing Candidates
        │
        ▼
ADVANCED ANALYTICS
        │
        ├──────────────► Camera Compensation
        ├──────────────► Event Detection
        ├──────────────► Match Report
        └──────────────► AI Insights
        │
        ▼
FINAL DASHBOARD VIDEO
📈 Analytics Levels
Level	Main Features
Level 1	Detection, tracking, IDs, team classification, pitch calibration
Level 2	Speed, distance, heatmaps, trajectories, statistics
Level 3	Ball, possession, passing, formations, tactical shape
Level 4	Camera compensation, dynamic calibration, events, reports, AI insights
🎓 Skills Demonstrated

This project demonstrates practical knowledge of:

Computer Vision
Object Detection
Object Tracking
Image Processing
Homography
Perspective Transformation
Video Processing
Machine Learning
YOLO
KMeans Clustering
Feature Extraction
Classification
Python
OpenCV
NumPy
Pandas
Scikit-learn
Matplotlib
YAML
JSON
Data Analytics
Speed Calculation
Distance Calculation
Spatial Analysis
Heatmaps
Trajectory Analysis
Statistical Summaries
AI / Sports Analytics
Player Tracking
Team Analysis
Ball Analysis
Tactical Analysis
Formation Analysis
Possession Estimation
Event Detection
Automated Insights
⚠️ Limitations

MatchLens AI is a computer-vision research/prototype system.

Current limitations may include:

Player occlusion
Similar jersey colors
Lighting variations
Camera movement
Fast player movement
Small or blurred football
Ball detection failures
Player ID switches
Incorrect team classification
Short-lived tracking IDs
Perspective errors
Inaccurate speed estimates when tracking is unstable
Approximate possession estimation
Approximate passing/event detection

Therefore, generated statistics should be considered computer-vision estimates, not official match statistics.

🔬 Future Improvements

Future development can include:

Custom-trained football player detector
Custom football/ball detector
Jersey-number recognition
Better player re-identification
DeepSORT / advanced tracking
Camera calibration using pitch keypoints
Automatic pitch-line detection
Camera-motion compensation
Accurate ball tracking
Pass detection
Shot detection
Goal detection
Offside analysis
Pressing analysis
Defensive-line analysis
Expected Goals (xG)
Expected Assists (xA)
Player workload analysis
Real-time camera processing
Web-based analytics dashboard
Database integration
Cloud deployment
💻 Example Commands
Basic Pipeline
python run.py --source input.mp4 --output outputs\matchlens.mp4
Player Analytics
python -m tools.analytics
Heatmap
python tools\heatmap.py
Team Heatmap
python tools\team_heatmap.py
Distance Analysis
python tools\player_distance.py
Speed Analysis
python tools\speed_analysis.py
Trajectory Video
python -m tools.trajectory_video
Level 3
python tools\run_level3.py
Level 4
python tools\run_level4.py
Final Dashboard
python tools\final_matchlens_video.py
🧪 Example Final Output

The final MatchLens AI video combines:

┌─────────────────────────────────────────────────────────────┐
│                    MATCHLENS AI                             │
├─────────────────────────────────────┬───────────────────────┤
│                                     │ MATCH STATISTICS      │
│                                     │                       │
│       FOOTBALL MATCH VIDEO          │ Team 1: 11            │
│                                     │ Team 2: 11            │
│     🔵 Player ID 12                 │ Avg Speed: XX km/h    │
│          ─────────────               │ Max Speed: XX km/h    │
│                 🟡                  │                       │
│          🟢 Player ID 8             │ TOP DISTANCE          │
│                                     │ ID 12                 │
│                                     │ ID 8                  │
├─────────────────────────────────────┴───────────────────────┤
│                    TACTICAL PITCH                           │
│                                                             │
│       🔵       🔵                 🟢       🟢                │
│                                                             │
│             🔵          🟡          🟢                       │
│                                                             │
│       🔵                         🟢                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
🏆 Project Highlights
✅ AI-based football video analysis
✅ YOLO object detection
✅ Multi-player tracking
✅ Persistent player IDs
✅ Team classification
✅ Pitch calibration
✅ Homography transformation
✅ Real-world player coordinates
✅ Player speed estimation
✅ Distance calculation
✅ Heatmap generation
✅ Trajectory visualization
✅ Ball tracking
✅ Player-ball relationship
✅ Possession estimation
✅ Passing analysis
✅ Formation analysis
✅ Tactical shape analysis
✅ Camera motion compensation
✅ Event detection
✅ Automated reports
✅ AI-based insights
✅ Final dashboard-style analytics video
👨‍💻 Author

Naveen Kumar S

B.E. Mechanical Engineering
Knowledge Institute of Technology, Salem

Areas of Interest
Automation & Robotics
Computer Vision
Artificial Intelligence
Machine Vision
Industrial Automation
Robotics
Data Analytics
📜 Project Purpose

MatchLens AI was developed as a practical application of Computer Vision, Artificial Intelligence, Object Tracking, and Data Analytics to the field of football analytics.

The project demonstrates how raw video can be converted into structured player tracking data and then transformed into meaningful visual and tactical information.

⭐ If You Like This Project

If this project is useful or interesting, consider giving the repository a ⭐ star.

Contributions, suggestions, and improvements are welcome.

📌 Disclaimer

MatchLens AI is an experimental computer-vision analytics project. Its outputs depend on video quality, camera angle, detection accuracy, tracking stability, calibration quality, and team-classification performance. Analytical values such as speed, possession, passing candidates, and tactical events should not be considered official match statistics without independent validation.


### Suggested GitHub repository tagline

> **AI-powered football match analytics using YOLO, OpenCV, player tracking, team classification, tactical analysis, and automated video insights.**

### Suggested GitHub topics

```text
football
football-analytics
computer-vision
opencv
yolo
yolov8
object-detection
object-tracking
bytetrack
sports-analytics
python
machine-learning
artificial-intelligence
player-tracking
tactical-analysis
