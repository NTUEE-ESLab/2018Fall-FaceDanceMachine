import argparse
import cv2
from imutils import face_utils
import dlib
import matplotlib.pyplot as plt
import numpy as np
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import time

face_num=11

#=============================================
#----No.----|------facial expression------|
#    0          pessimistic

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument('--relax', default='/home/mtjade/eslab_final/face/relax.jpg', type=str, help='input gallery')
ap.add_argument('--input_img', default='/home/mtjade/eslab_final/face/pessimistic.jpg', type=str, help='input image')
args = vars(ap.parse_args())


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
fa = FaceAligner(predictor, desiredFaceWidth=256)


def Getlandmark(img):
	gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	# loop over the face detections
	# determine the facial landmarks for the face region, then
	# convert the facial landmark (x, y)-coordinates to a NumPy
	# array
	shape = predictor(gray, rects[0])
	shape = face_utils.shape_to_np(shape)
	faceAligned = fa.align(img, gray, rects[0])
	rects = detector(faceAligned, 0)
	shape=predictor(faceAligned,rects[0])
	shape = face_utils.shape_to_np(shape)
	tmp=np.zeros(faceAligned.shape)
	for (x,y) in shape:
		cv2.circle(tmp, (x, y), 2, (255, 255, 255), -1)
	'''
	plt.imshow(tmp)
	plt.show()
	'''

	# loop over the (x, y)-coordinates for the facial landmarks
	# and draw them on the image
	return shape

def Calsimilarity(gallery, img):
	print(gallery)
	print(img)
	landmark_num=gallery.shape[0]
	'''
	right=np.amax(gallery, axis=0)
	left=np.amin(gallery, axis=0)
	height=(right[1]-left[1]+1)
	width=(right[0]-left[0]+1)
	input_i=np.zeros((height,width))
	for (x, y) in gallery:
		new_y=y-left[1]
		new_x=x-left[0]
		input_i[new_y][new_x]=1
	plt.imshow(input_i,cmap="gray")
	plt.show()

	right=np.amax(img, axis=0)
	left=np.amin(img, axis=0)
	height=(right[1]-left[1]+1)
	width=(right[0]-left[0]+1)
	input_i=np.zeros((height,width))
	for (x, y) in img:
		new_y=y-left[1]
		new_x=x-left[0]
		input_i[new_y][new_x]=1
	plt.imshow(input_i,cmap="gray")
	plt.show()
	'''
	#vector
	vector_gallery=np.zeros((landmark_num,landmark_num,2))
	for i,(x1,y1) in enumerate(gallery):
		for y, (x2,y2) in enumerate(gallery):
			vector_gallery[i,y,0]=x2-x1
			vector_gallery[i,y,1]=y2-y1
	vector_ratio=1/np.amax(np.sqrt(np.sum(vector_gallery*vector_gallery,axis=2)))
	vector_gallery*=vector_ratio

	vector_img=np.zeros((landmark_num,landmark_num,2))
	for i,(x1,y1) in enumerate(img):
		for y, (x2,y2) in enumerate(img):
			vector_img[i,y,0]=x2-x1
			vector_img[i,y,1]=y2-y1
	vector_ratio=1/np.amax(np.sqrt(np.sum(vector_img*vector_img,axis=2)))
	vector_img*=vector_ratio

	result=vector_gallery-vector_img
	print(np.sum(np.sqrt(np.sum(result*result,axis=2))))
	print(np.sum(gallery))
	input("111")



	#scalar
	return 0
def Frown(landmark):
	result=False
	similarity=0
	diff_l=landmark[37:40,1]-landmark[19:22,1]
	diff_r=landmark[42:45,1]-landmark[22:25,1]
	eye_dis=landmark[42,0]-landmark[39,0]
	eyebrow_dis=landmark[22,0]-landmark[21,0]

	if np.argmin(diff_l)==2 and np.argmin(diff_r)==0 and np.argmax(diff_l)==0 and np.argmax(diff_r)==2 :
		if np.argmax(landmark[19:22,1])==2 and np.argmax(landmark[22:25,1])==0:
			if eyebrow_dis/eye_dis<0.5:
				result=True
				similarity=(1-eyebrow_dis/eye_dis)*1.5
	
	print("Frown:",similarity)
	return result,similarity

def RightEyeWink(landmark):
	result=False
	similarity=0
	l=np.sum(landmark[40:42,1])-np.sum(landmark[37:39,1])
	r=np.sum(landmark[46:48,1])-np.sum(landmark[43:45,1])
	diff=np.sum(landmark[22:27,1])-np.sum(landmark[17:22,1])
	slope_r=abs((landmark[24,1]-landmark[22,1])/(landmark[24,0]-landmark[22,0]))
	slope_l=abs((landmark[19,1]-landmark[21,1])/(landmark[19,0]-landmark[21,0]))
	if r<l and diff>0 and slope_l/slope_r>2:
		result=True
		similarity=1
	print("RightEyeWink:",similarity)
	return result,similarity


def MouthOpen(landmark):
	result=False
	similarity=0
	upperlip=landmark[62,1]-landmark[51,1]
	height=landmark[66,1]-landmark[62,1]
	if height>upperlip:
		result=True
		similarity=1
	print("MouthOpen:",similarity)
	return result,similarity

def MouthClosed(landmark):
	close=np.sum(landmark[65:68,1])-np.sum(landmark[61:64,1])
	height=landmark[62,1]-landmark[51,1]
	result=False
	if close<=height:
		similarity=1
		result=True
	else:
		similarity=0
	#print (close,height)
	print("MouthClosed:",similarity)
	return result,similarity

def MouthRight(landmark):
	middle_x=landmark[27,0]
	mouth_x=landmark[48:68,0]
	dis=mouth_x-middle_x
	result=False
	negative=[d for d in dis if d<0]
	if len(negative)<10:
		similarity=1-len(negative)/20*0.5
		result=True
	else:
		similarity=0
	print("MouthRight:", similarity)
	return result,similarity

def MouthLeft(landmark):
	middle_x=landmark[27,0]
	mouth_x=landmark[48:68,0]
	dis=mouth_x-middle_x
	result=False
	negative=[d for d in dis if d>0]
	if len(negative)<10:
		similarity=1-len(negative)/20*0.5
		result=True
	else:
		similarity=0
	print("MouthLeft:", similarity)
	return result,similarity

def Smile(landmark):
	result=False
	similarity=0
	h=np.mean(landmark[60:65,1])
	mouth=np.amax(landmark[48:68,1])-np.amin(landmark[48:68,1])
	if landmark[48,1]<h and landmark[54,1]<h:
		similarity=0.8+0.2*(h-(landmark[48,1]+landmark[54,1])/2)/mouth
		result=True
	print("Smile:",similarity)
	return result,similarity

def PointDown(landmark):
	result=False
	similarity=0
	h=(np.mean(landmark[64:68,1])+landmark[60,1])/2
	mouth=np.amax(landmark[48:68,1])-np.amin(landmark[48:68,1])
	if landmark[48,1]>h and landmark[54,1]>h:
		result=True
		similarity=0.8+0.2*((landmark[48,1]+landmark[54,1])/2-h)/mouth
	print("PointDown:",similarity)
	return result,similarity

def MouthOval(landmark):
	result=False
	similarity=0
	height=landmark[57,1]-landmark[51,1]
	width=landmark[54,0]-landmark[48,0]
	if abs(height/width)>1:
		result=True
		similarity=1
	
	print("MouthOval:",similarity)
	return result,similarity

def MouthCircle(landmark):
	result=False
	similarity=0
	height=landmark[57,1]-landmark[51,1]
	width=landmark[54,0]-landmark[48,0]
	if abs(height/width-1)<0.5:
		result=True
		similarity=1-abs(height/width-1)*0.5
	
	print("MouthCircle:",similarity)
	return result,similarity



def MouthWide(landmark):
	result=False
	similarity=0
	height=landmark[57,1]-landmark[51,1]
	width=landmark[54,0]-landmark[48,0]
	if width/height>1:
		result=True
		similarity=0.8+0.2*width/height*0.3
	
	print("WideMouth:",similarity)
	return result,similarity

def FaceLeft(landmark):
	result=False
	similarity=0
	L_len=landmark[27,0]-landmark[0,0]
	R_len=landmark[16,0]-landmark[28,0]
	if R_len/L_len>1.5:
		result=True
		similarity=1
	
	print("FaceLeft:",similarity)
	return result,similarity

def FaceRight(landmark):
	result=False
	similarity=0
	L_len=landmark[27,0]-landmark[0,0]
	R_len=landmark[16,0]-landmark[28,0]
	if L_len/R_len>1.5:
		result=True
		similarity=1	
	
	print("FaceRight:",similarity)
	return result,similarity
	



#compare ordered face
def face_dance(face_mission, target, landmark_relax):	
	landmark_target=Getlandmark(target)
	result=-1
	similarity=0
	for mission in face_mission:
		if mission==0:
			print("==========pessimistic==========")
			#pessimistic
			mouth_left, left_score=MouthLeft(landmark_target)
			mouth_closed, closed_score=MouthClosed(landmark_target)
			smile, smile_score=Smile(landmark_target)
			if mouth_left and mouth_closed and not smile:
				similarity=(left_score*0.5+closed_score*0.5)
				print(similarity)
				#break
		elif mission==1:
			print("==========surprised==========")
			#surprised
			mouth_open, open_score=MouthOpen(landmark_target)
			frown,frown_score=Frown(landmark_target)
			mouth_O,O_score=MouthCircle(landmark_target)
			mouth_oval,oval_score=MouthOval(landmark_target)
			mouth_left, left_score=MouthLeft(landmark_target)
			#Reye_open, Reye_score=RightEyeOpen(landmark_target,landmark_relax)
			#Leye_open, Leye_score=LeftEyeOpen(landmark_target)
			if mouth_open and not frown and not mouth_left:
				if mouth_O or mouth_oval:
					similarity=open_score*0.3+(max(oval_score,O_score))*0.7
					print(similarity)
				#break
		elif mission==2:
			print("==========wink==========")
			#wink
			Reye_wink, Reye_score=RightEyeWink(landmark_target)
			smile, smile_score=Smile(landmark_target)
			if Reye_wink and smile:
				similarity=smile_score*0.8+Reye_score*0.2
				print(similarity)
				#break
		elif mission==3:
			print("==========sadness==========")
			#sadness
			#Reye_open, Reye_score=RightEyeOpen(landmark_target, landmark_relax)
			#Leye_open, Leye_score=LeftEyeOpen(landmark_target)
			pointDown, pointDown_score=PointDown(landmark_target)
			if pointDown :
				similarity=pointDown_score
				print(similarity)
				#break
		elif mission==4:
			print("==========grin==========")
			#grin
			smile, smile_score=Smile(landmark_target)
			mouth_open, open_score=MouthOpen(landmark_target)
			if mouth_open and smile:
				similarity=smile_score*0.7+mouth_open*0.3
				print(similarity)
				#break

		elif mission==5:
			#angry
			print("==========angry==========")
			frown,frown_score=Frown(landmark_target)
			mouth_open, open_score=MouthOpen(landmark_target)
			w_mouth, mouth_score=MouthWide(landmark_target)
			if frown and mouth_open and w_mouth:
				similarity=frown_score*0.6+mouth_score*0.4
				print(similarity)
				#break
		elif mission==6:
			#LeftO
			print("==========LeftO==========")
			frown,frown_score=Frown(landmark_target)
			mouth_left, left_score=MouthLeft(landmark_target)
			mouth_O,O_score=MouthCircle(landmark_target)
			face_left, face_score=FaceLeft(landmark_target)

			if not frown and mouth_left and mouth_O and face_left:
				similarity=left_score*0.5+O_score*0.5
				print(similarity)
				#break
		elif mission==7:
			#RightO
			print("==========RightO==========")
			frown,frown_score=Frown(landmark_target)
			mouth_Right, Right_score=MouthRight(landmark_target)
			mouth_O,O_score=MouthCircle(landmark_target)
			face_Right, face_score=FaceRight(landmark_target)

			if not frown and mouth_Right and mouth_O and face_Right:
				similarity=Right_score*0.5+O_score*0.5
				print(similarity)
				#break
		elif mission==8:
			#toothache
			print("==========toothache==========")
			Reye_wink, Reye_score=RightEyeWink(landmark_target)
			mouth_open, open_score=MouthOpen(landmark_target)
			mouth_left, left_score=MouthLeft(landmark_target)

			if Reye_wink and mouth_left and mouth_open:
				similarity=left_score*0.8+Reye_score*0.2
				print(similarity)
				#break
		elif mission==9:
			#calm
			print("==========calm==========")
			mouth_closed, closed_score=MouthClosed(landmark_target)
			smile, smile_score=Smile(landmark_target)
			pointDown, pointDown_score=PointDown(landmark_target)
			frown,frown_score=Frown(landmark_target)
			if mouth_closed and not smile and not pointDown and not frown:
				similarity=1
				print(similarity)
				#break
		elif mission==10:
			break
		elif mission==11:
			break
	return result, round(100*similarity)




def main():

	face_relax=cv2.imread(args["relax"])
	landmark_relax=Getlandmark(face_relax)
	face_mission=[0,1,2,3,4,5,6,7,8,9]
	target=cv2.imread(args["input_img"])
	face_dance(face_mission, target, landmark_relax)
	
	'''     
	mouth=Calsimilarity(landmark_gallery[48:68,:], landmark_target[48:68,:])
	left_eyes=Calsimilarity(landmark_gallery[36:42,:], landmark_target[36:42,:])
	right_eyes=Calsimilarity(landmark_gallery[42:48,:], landmark_target[42:48,:])
	left_eyebrows=Calsimilarity(landmark_gallery[16:22,:], landmark_target[16:22,:])
	right_eyebrows=Calsimilarity(landmark_gallery[22:27,:], landmark_target[22:27,:])
	'''






if __name__ == '__main__':
    main()