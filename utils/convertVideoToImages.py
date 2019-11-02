import cv2

VIDEO_PATH = "D:\\code_collection\\RetailAnalytics\\videos\\cam4-2.mkv"
SAVE_PATH = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\"

videoReader = cv2.VideoCapture(VIDEO_PATH)

imageIndex = 0
while videoReader.isOpened():
    _, frame = videoReader.read()
    if frame is None:
        print ('\nEnd of Video')
        break
    filepath = SAVE_PATH + 'frame{:04d}'.format(imageIndex) + '.jpg'
    cv2.imwrite(filepath, frame)
    imageIndex += 1
    if(imageIndex % 100 == 0):
        print("Processing " + str(imageIndex) + "th file")