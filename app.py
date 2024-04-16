import cv2
import pytesseract
import re  

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\Tesseract.exe'
cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    custom_config = r'--oem 3 --psm 11 -l eng --dpi 300'

    text = pytesseract.image_to_string(binary, config=custom_config)
    print("Extracted Text:", text)
    cleaned_text = re.sub(r'\s+', '', text)

    
    h, w = gray.shape  
    boxes = pytesseract.image_to_boxes(binary)
    for b in boxes.splitlines():
        b = b.split()
        x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(binary, (x, h - y), (x2, h - y2), (0, 0, 255), 2)

    input_text = "IVECO"
    cleaned_input_text = re.sub(r'\s+', '', input_text)

    if cleaned_text.lower() == cleaned_input_text.lower():

        print("Texto correto")
    else:
        print("Texto incorreto")

    cv2.imshow('Camera Feed', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()