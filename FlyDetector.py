# Untitled - By: RIKIKEN - 火 10月 24 2017

THRESHOLD = (120, 255) # Grayscale threshold for dark things...
#thresholds =  (110, 255)
BINARY_VISIBLE = True # Does binary first so you can see what the linear regression
                      # is being run on... might lower FPS though.

import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

color = [0, 255]
lines = [0, 0]

windowSize = [10,10,20,20]

count = 1
while count <= 50:
    img = sensor.snapshot()
    img.binary([THRESHOLD])
    blobs = img.find_blobs([THRESHOLD],invert=True,pixels_threshold=10)
    count += 1
    if len(blobs) == 2:
        preblobs = blobs

while(True):
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([THRESHOLD],invert=True,pixels_threshold=10)

    if len(blobs) == 2:
        distTwoTimepoints = [math.sqrt((blobs[0].cx() - preblobs[0].cx())**2 + (blobs[0].cy() - preblobs[0].cy())**2), math.sqrt((blobs[1].cx() - preblobs[1].cx())**2 + (blobs[1].cy() - preblobs[1].cy())**2), \
        math.sqrt((blobs[0].cx() - preblobs[1].cx())**2 + (blobs[0].cy() - preblobs[1].cy())**2)]    #[dist between Myself (blob[0]), dist between Myself (blob[1]), dist between blob[0] and 1]

        if distTwoTimepoints[0] > distTwoTimepoints[2] - 2:
            blobs = blobs[::-1]

        i = 0
        for blob in blobs:
            img.draw_cross(blob.cx(),blob.cy(),color=color[i])
            lines[i] = img.get_regression([THRESHOLD],roi=[blob.cx()-windowSize[0],blob.cy()-windowSize[1],windowSize[2],windowSize[3]], invert = True)
            img.draw_line(lines[i].line(), color=color[i])
            i += 1

        dist = math.sqrt((blobs[0].cx() - blobs[1].cx())**2 + (blobs[0].cy() - blobs[1].cy())**2)
        #print(dist)

        preblobs = blobs

    else:
        print('nothing')

    print("FPS %f" % (clock.fps()))
