import mediapipe as mp
import cv2


class HandDetector():
    def __init__(self,mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.complexity = 1

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        handNo = 0

        if self.results.multi_hand_landmarks:
            handNo = len(self.results.multi_hand_landmarks)
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img, handNo

    def findPosition(self, img, handNo = 0, draw = True):
        lmList = []

        if self.results.multi_hand_landmarks:          
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cx, cy = lm.x, lm.y

                lmList.append([id, cx, cy])

                if draw:
                    pass
                    #cv2.circle(img, (cx, cy), 3, (0,0,255), cv2.FILLED)

        return lmList


class PoseDetector():
    def __init__(self, staticMode = False, modelComplexity = 1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = staticMode
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode = self.mode,
                                     model_complexity = self.modelComplexity,
                                    min_detection_confidence = self.detectionCon,
                                    min_tracking_confidence = self.trackCon)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles


    def findBody(self, img, draw = True):

        img.flags.writeable = False      #こうするとパフォーマンスが向上するらしい
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(img)

        img.flags.writeable = True       #元に戻す
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.mp_drawing.draw_landmarks(
            img,
            self.result.pose_landmarks,
            self.mpPose.POSE_CONNECTIONS,
            landmark_drawing_spec = self.mp_drawing_styles.get_default_pose_landmarks_style())

        return img

    def findPosePosition(self, img):
        success = False
        landmarks = []
        height, width, channel = img.shape


        if self.result.pose_landmarks:
            success = True
            for id, lm in enumerate(self.result.pose_landmarks.landmark):
                cx, cy, cz = round(lm.x, 2), round(lm.y,2), round(lm.z,2)

                landmarks.append([id, cx, cy, cz])

        return success, landmarks
        