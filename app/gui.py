import tkinter as tk
from tkinter import ttk
from app.template_matcher import TemplateMatcher

class GUI:
    def __init__(self, root):
        self.root = root
        self.matcher = TemplateMatcher()

        # GUI Elements
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.start_button = ttk.Button(root, text="Start", command=self.start_template_matching)
        self.start_button.pack()

        self.select_roi_button = ttk.Button(root, text="Select ROI", command=self.select_roi)
        self.select_roi_button.pack()

        self.threshold_label = ttk.Label(root, text="Threshold:")
        self.threshold_label.pack()
        self.threshold_scale = ttk.Scale(root, from_=0, to=100, command=self.set_threshold)
        self.threshold_scale.pack()

        self.fps_label = ttk.Label(root, text="Live FPS:")
        self.fps_label.pack()
        self.fps_scale = ttk.Scale(root, from_=1, to=30, command=self.set_live_fps)
        self.fps_scale.pack()

    def start_template_matching(self):
        self.matcher.start()

    def select_roi(self):
        self.matcher.select_roi()

    def set_threshold(self, value):
        self.matcher.set_threshold(float(value))

    def set_live_fps(self, value):
        self.matcher.set_live_fps(int(value))
