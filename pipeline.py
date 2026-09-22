from pathlib import Path
import csv
import cv2
import numpy as np
from ultralytics import YOLO

from .config import Config
from .homography import PitchMapper
from .team_classifier import TeamClassifier
from .tactical import render_tactical

class MatchLensPipeline:
    def __init__(self, config_path):
        self.cfg = Config.from_yaml(config_path)

        self.model = YOLO(self.cfg.model)

        self.mapper = PitchMapper(
            self.cfg.image_points,
            self.cfg.pitch_length,
            self.cfg.pitch_width,
        )

        self.team_classifier = TeamClassifier()

    def _device(self):
        if self.cfg.device == "auto":
            return 0 if self._has_cuda() else "cpu"
        return self.cfg.device

    @staticmethod
    def _has_cuda():
        try:
            import torch
            return bool(torch.cuda.is_available())
        except Exception:
            return False

    @staticmethod
    def _make_writer(path, fps, width, height):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        return cv2.VideoWriter(path, fourcc, fps, (width, height))

    def run(self, source, output):
        cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video: {source}")

        fps = cap.get(cv2.CAP_PROP_FPS) or self.cfg.fps
        frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out_w = frame_w + self.cfg.tactical_width
        out_h = max(frame_h, self.cfg.tactical_height)

        writer = self._make_writer(
            output, fps, out_w, out_h
        )

        csv_path = str(Path(output).with_name("tracks.csv"))

        csv_file = open(
            csv_path, "w", newline="", encoding="utf-8"
        )

        csv_writer = csv.writer(csv_file)

        csv_writer.writerow([
            "frame",
            "track_id",
            "class",
            "team",
            "x1",
            "y1",
            "x2",
            "y2",
            "pitch_x_m",
            "pitch_y_m",
        ])

        frame_no = 0
        team_fitted = False

        while True:
            ok, frame = cap.read()

            if not ok:
                break

            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                conf=self.cfg.confidence,
                iou=self.cfg.iou,
                imgsz=self.cfg.imgsz,
                device=self._device(),
                verbose=False,
            )

            result = results[0]

            player_boxes = []
            detections = []

            if result.boxes is not None and len(result.boxes) > 0:
                xyxy = result.boxes.xyxy.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy().astype(int)
                confs = result.boxes.conf.cpu().numpy()

                if result.boxes.id is not None:
                    ids = result.boxes.id.cpu().numpy().astype(int)
                else:
                    ids = np.full(len(xyxy), -1)

                for box, cls_id, score, track_id in zip(
                    xyxy, classes, confs, ids
                ):
                    if score < self.cfg.confidence:
                        continue

                    # COCO:
                    # 0 = person
                    # 32 = sports ball
                    if cls_id == 0:
                        player_boxes.append(box.tolist())

                        detections.append(
                            (
                                box,
                                "player",
                                int(track_id),
                                float(score),
                            )
                        )

                    elif cls_id == 32:
                        detections.append(
                            (
                                box,
                                "ball",
                                int(track_id),
                                float(score),
                            )
                        )

            # Once enough players are visible, learn the two visual groups.
            if not team_fitted and len(player_boxes) >= 4:
                team_fitted = self.team_classifier.fit(
                    frame, player_boxes
                )

            tactical_tracks = []

            for box, kind, track_id, score in detections:
                x1, y1, x2, y2 = box

                if kind == "player":
                    team = (
                        self.team_classifier.predict(frame, box)
                        if team_fitted
                        else None
                    )

                    # Player's foot/contact point with the ground.
                    foot_x = (x1 + x2) / 2.0
                    foot_y = y2

                    pitch_x, pitch_y = (
                        self.mapper.image_to_pitch(
                            foot_x, foot_y
                        )
                    )

                    # Reject clearly impossible projections.
                    if not (
                        -20 <= pitch_x <= self.cfg.pitch_length + 20
                        and
                        -20 <= pitch_y <= self.cfg.pitch_width + 20
                    ):
                        pitch_x = None
                        pitch_y = None

                    csv_writer.writerow([
                        frame_no,
                        track_id,
                        kind,
                        team,
                        round(float(x1), 1),
                        round(float(y1), 1),
                        round(float(x2), 1),
                        round(float(y2), 1),
                        None if pitch_x is None else round(pitch_x, 2),
                        None if pitch_y is None else round(pitch_y, 2),
                    ])

                    tactical_tracks.append({
                        "track_id": track_id,
                        "team": team,
                        "pitch_x": pitch_x,
                        "pitch_y": pitch_y,
                    })

                    cv2.rectangle(
                        frame,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        (255, 255, 255),
                        2,
                    )

                    label = f"ID {track_id} T{team or '?'}"

                    cv2.putText(
                        frame,
                        label,
                        (int(x1), max(20, int(y1)-8)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 255, 255),
                        2,
                    )

                else:
                    # Ball detection.
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)

                    radius = max(
                        3,
                        int(max(x2-x1, y2-y1) / 2)
                    )

                    cv2.circle(
                        frame,
                        (cx, cy),
                        radius,
                        (255, 255, 255),
                        2,
                    )

                    cv2.putText(
                        frame,
                        f"BALL {track_id}",
                        (cx+5, cy-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2,
                    )

            tactical = render_tactical(
                tactical_tracks,
                self.cfg.tactical_width,
                out_h,
                self.cfg.pitch_length,
                self.cfg.pitch_width,
            )

            canvas = np.zeros(
                (out_h, out_w, 3),
                dtype=np.uint8
            )

            canvas[
                :frame_h,
                :frame_w
            ] = frame

            canvas[
                :tactical.shape[0],
                frame_w:frame_w+tactical.shape[1]
            ] = tactical

            cv2.putText(
                canvas,
                "MATCHLENS AI - TACTICAL VIEW",
                (frame_w+20, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2,
            )

            writer.write(canvas)

            frame_no += 1

            if frame_no % 100 == 0:
                print(f"Processed {frame_no} frames")

        cap.release()
        writer.release()
        csv_file.close()

        print(f"Saved video: {output}")
        print(f"Saved tracks: {csv_path}")
