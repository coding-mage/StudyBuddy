def sm2(interval, ease, quality):
    if quality < 3:
        return 1, 2.5
    ease = max(1.3, ease + (0.1 - (5-quality)*(0.08+(5-quality)*0.02)))
    interval = int(interval * ease)
    return interval, ease
