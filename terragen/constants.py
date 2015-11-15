from PIL import ImageColor

def hsl2rgb(c):
    return ImageColor.getrgb(c)

# http://jsfiddle.net/m4s3mq55/2/
TERRAIN = [
    (-100, hsl2rgb('hsl(195, 80%, 15%)')),
    (-90, hsl2rgb('hsl(195, 80%, 17%)')),
    (-80, hsl2rgb('hsl(195, 80%, 20%)')),
    (-70, hsl2rgb('hsl(195, 80%, 22%)')),
    (-60, hsl2rgb('hsl(195, 80%, 25%)')),
    (-50, hsl2rgb('hsl(195, 80%, 28%)')),
    (-40, hsl2rgb('hsl(195, 80%, 30%)')),
    (-30, hsl2rgb('hsl(195, 80%, 32%)')),
    (-20, hsl2rgb('hsl(195, 80%, 35%)')),
    (-10, hsl2rgb('hsl(195, 80%, 40%)')),
    (0, hsl2rgb('hsl(36,    22%, 40%)')),
    (10, hsl2rgb('hsl(35,   24%, 42%)')),
    (20, hsl2rgb('hsl(34,   26%, 45%)')),
    (30, hsl2rgb('hsl(33,   28%, 50%)')),
    (40, hsl2rgb('hsl(32,   30%, 55%)')),
    (50, hsl2rgb('hsl(32,   35%, 60%)')),
    (60, hsl2rgb('hsl(32,   38%, 65%)')),
    (70, hsl2rgb('hsl(32,   40%, 70%)')),
    (80, hsl2rgb('hsl(32,   45%, 75%)')),
    (90, hsl2rgb('hsl(32,   50%, 80%)')),
    (100, hsl2rgb('hsl(32,  55%, 85%)'))
]
