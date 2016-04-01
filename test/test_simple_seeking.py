from __future__ import print_function

from contextlib import closing
from PIL import ImageChops, ImageStat
from videosequence import VideoSequence

def assert_images_not_equal(im1, im2):
    diff = ImageChops.difference(im1, im2)
    for min_, max_ in ImageStat.Stat(diff).extrema:
        if max_ > 0:
            return
    assert False

def assert_images_equal(im1, im2):
    diff = ImageChops.difference(im1, im2)
    for min_, max_ in ImageStat.Stat(diff).extrema:
        if max_ != 0:
            assert False

def test_duration(news_video, ice_video):
    with closing(VideoSequence(news_video)) as s:
        assert len(s) == 288
    with closing(VideoSequence(ice_video)) as s:
        assert len(s) == 468

def test_size(news_video):
    with closing(VideoSequence(news_video)) as s:
        assert s.width == 352
        assert s.height == 288

def test_initial_and_final_frame(news_video, ice_video):
    with closing(VideoSequence(news_video)) as s:
        start = s[0]
        end = s[-1]
    assert_images_not_equal(start, end)
    with closing(VideoSequence(ice_video)) as s:
        start = s[0]
        end = s[-1]
    assert_images_not_equal(start, end)

def test_first_few_frames_differ(news_video):
    with closing(VideoSequence(news_video)) as s:
        last_mean = 0.0
        for idx in range(5):
            print("Frame", idx)
            mean = ImageStat.Stat(s[idx]).mean[0]
            assert mean != last_mean
            assert mean > 0
            last_mean = mean

def test_slice_news(news_video):
    with closing(VideoSequence(news_video)) as s:
        frames = [s[idx] for idx in range(5, 10)]
        for f1, f2 in zip(frames, s[5:10]):
            assert_images_equal(f1, f2)

def test_slice_ice(ice_video):
    with closing(VideoSequence(ice_video)) as s:
        frames = [s[idx] for idx in range(5, 10)]
        for f1, f2 in zip(frames, s[5:10]):
            assert_images_equal(f1, f2)

def __xtest_iteration(news_video, ice_video):
    with closing(VideoSequence(news_video)) as s:
        n = 0
        for _ in s:
            n += 1
        assert n == len(s)
    with closing(VideoSequence(ice_video)) as s:
        n = 0
        for _ in s:
            n += 1
        assert n == len(s)

