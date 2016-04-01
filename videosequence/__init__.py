from __future__ import division
import collections
import contextlib
import logging
import os

import gi
import PIL.Image as Image

gi.require_version('Gst', '1.0')
gi.require_version('GstApp', '1.0')
from gi.repository import Gst, GstApp

# Initialise GStreamer
Gst.init()

LOG = logging.getLogger()
STATE_CHANGE_TIMEOUT = 5 * Gst.SECOND

class VideoSequence(collections.Sequence):
    """
    A sequence of video frames.

    """
    def __init__(self, path):
        abs_uri = "file://" + os.path.abspath(path)
        LOG.info("Opening file at %s", abs_uri)

        pipeline = Gst.ElementFactory.make("playbin", "playbin")
        self.pipeline = pipeline
        pipeline.set_property("uri", abs_uri)
        pipeline.set_property(
            "audio-sink", Gst.ElementFactory.make("fakesink", "fakeaudio"))

        videocaps = Gst.Caps.new_empty_simple("video/x-raw")
        videocaps.set_value("format", "RGB")
        appsink = GstApp.AppSink()
        self.appsink = appsink
        appsink.set_property("caps", videocaps)
        pipeline.set_property("video-sink", appsink)

        ret = pipeline.set_state(Gst.State.PAUSED)
        if ret == Gst.StateChangeReturn.ASYNC:
            ret, state, _ = pipeline.get_state(STATE_CHANGE_TIMEOUT)
        if ret == Gst.StateChangeReturn.FAILURE:
            raise IOError("Failed to open video")
        elif ret == Gst.StateChangeReturn.NO_PREROLL:
            raise IOError("Live sources not supported")
        assert state == Gst.State.PAUSED

        sample = appsink.pull_preroll()
        if sample is None:
            raise IOError("No data in video")

        self.caps = sample.get_caps()
        ok, num, denom = self.caps.get_structure(0).get_fraction("framerate")
        if not ok:
            raise IOError("Could not determine frame rate for seeking")
        self.ns_per_frame = (denom * Gst.SECOND) / num

        self.width = self.caps.get_structure(0).get_value("width")
        self.height = self.caps.get_structure(0).get_value("height")

        ok, duration = pipeline.query_duration(Gst.Format.TIME)
        if not ok:
            raise IOError("Could not determine duration of video")

        self.duration = int(duration / self.ns_per_frame)

    def close(self):
        self.pipeline.set_state(Gst.State.NULL)

    def _get_frame(self, index):
        flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE | Gst.SeekFlags.SKIP
        ok = self.pipeline.seek_simple(
            Gst.Format.TIME, flags, index * self.ns_per_frame)
        if not ok:
            raise RuntimeError("Unable to seek")

        sample = self.appsink.pull_preroll()
        if sample is None:
            LOG.warn("Seek failed, returning empty frame based on initial frame size")
            return Image.new("RGB", (self.width, self.height))
        return _sample_to_image(sample)

    def _get_slice(self, slc):
        for idx in range(*slc.indices(self.duration)):
            yield self._get_frame(idx)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._get_slice(key)
        key = int(key)
        if key < 0:
            key += self.duration
        if key < 0 or key >= self.duration:
            raise IndexError("Invalid frame index: {}".format(key))
        return self._get_frame(key)

    def __len__(self):
        return self.duration

def _sample_to_image(sample):
    caps = sample.get_caps()
    format_ = caps.get_structure(0).get_string("format")
    if format_ != "RGB":
        raise ValueError("Need RGB frame sample to convert to image")

    buf = sample.get_buffer()
    data = buf.extract_dup(0, buf.get_size())
    w = caps.get_structure(0).get_value("width")
    h = caps.get_structure(0).get_value("height")
    return Image.frombytes("RGB", (w, h), data)
