# Untitled - By: RIKIKEN - 火 10月 24 2017

import sensor, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames()

#led = pyb.LED(1)
#led.on()

thresholds = (120, 255)
color = [0, 255]

count = 1
while count <= 100:
    img = sensor.snapshot()
    blobs = img.find_blobs([thresholds],invert=True,pixels_threshold=10)
    count += 1
    if len(blobs) == 2:
        preblobs = blobs

while(True):
    img = sensor.snapshot()
    blobs = img.find_blobs([thresholds],invert=True,pixels_threshold=10)

    if len(blobs) == 2:
        distTwoTimepoints = [math.sqrt((blobs[0].cx() - preblobs[0].cx())**2 + (blobs[0].cy() - preblobs[0].cy())**2), math.sqrt((blobs[1].cx() - preblobs[1].cx())**2 + (blobs[1].cy() - preblobs[1].cy())**2), \
        math.sqrt((blobs[0].cx() - preblobs[1].cx())**2 + (blobs[0].cy() - preblobs[1].cy())**2)]    #[dist between Myself (blob[0]), dist between Myself (blob[1]), dist between blob[0] and 1]

        if distTwoTimepoints[0] > distTwoTimepoints[2] - 2:
            blobs = blobs[::-1]

        i = 0
        for blob in blobs:
            img.draw_cross(blob.cx(),blob.cy(),color=color[i])
            i = i + 1
        dist = math.sqrt((blobs[0].cx() - blobs[1].cx())**2 + (blobs[0].cy() - blobs[1].cy())**2)
        #print(dist)

        preblobs = blobs

    else:
        print('nothing')
