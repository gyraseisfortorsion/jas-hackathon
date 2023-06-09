import numpy as np
from facenet_pytorch import MTCNN
import cv2
import time
import torch
from model import GenderAge
from model_em import EmotionsModel

device = 'cuda' if torch.cuda.is_available() else 'cpu'

mtcnn = MTCNN(image_size=160, margin=14, min_face_size=40,device=device, post_process=False)
model = torch.load('best.pt').to(device)
model_em = EmotionsModel().to(device)
model_em.load_state_dict(torch.load('model66.pt'))


cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

prev_frame_time = 0
next_frame_time = 0

Genders = {0: 'male', 1: 'female'}
Moods = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

def transform(im):
	im = cv2.resize(im, (48,48))
	im = torch.tensor(im/255.)
	im = im.permute(2,0,1)
	return im.float().to(device).unsqueeze(0)


while cap.isOpened():
	ret, frame = cap.read()
	if not ret:
		break
	frame_BGR=frame.copy()
	model.eval()
	model_em.eval()
	frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	boxes, probs = mtcnn.detect(frame, landmarks=False)
	
	if (probs.all() != None and probs.all() > 0.8):
		for x1,y1,x2,y2 in boxes:
			x1,x2,y1,y2 = int(x1),int(x2),int(y1),int(y2)
			face = frame_BGR[y1:y2,x1:x2]
			face_cp = face
			if face.shape[0]==0 or face.shape[1]==0:
				continue
			face = np.transpose(cv2.resize(face, (128,128)), (2,0,1))
			face = np.expand_dims(face, 0).astype(np.float32)/255.
			predictions = model(torch.tensor(face).to(device)).detach().cpu().numpy()
			gender = int(np.argmax(predictions[0, :2]))
			age = int(predictions[0, 2])
			emotion = torch.argmax(model_em(transform(face_cp))).cpu().numpy().item()

			cv2.putText(frame, 'Gender: {}, Age: {}, Mood: {}'.format(['Male', 'Female'][gender], age, Moods[emotion]), (x1,y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255))
	frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

	next_frame_time = time.time()
	try:
		fps = str(round(1/(next_frame_time-prev_frame_time),2))
	except ZeroDivisionError:
		fps = ""
	prev_frame_time = next_frame_time

	cv2.putText(frame, fps, (7,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 1, cv2.LINE_AA)
	cv2.imshow("Face Recognition", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
