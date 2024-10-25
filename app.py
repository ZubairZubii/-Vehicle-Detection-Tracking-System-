# # import os
# # import threading
# # from flask import Flask, request, render_template, send_from_directory, jsonify
# # import cv2
# # import numpy as np
# # from ultralytics import YOLO
# # import ffmpegcv

# # app = Flask(__name__)

# # UPLOAD_FOLDER = 'uploads'
# # OUTPUT_FOLDER = 'outputs'
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# # # Global variables to control the margin and stopping the processing
# # margin = 50
# # stop_processing = False

# # class MainClass:
# #     def __init__(self):
# #         self.vehicle_thread = None
# #         self.registered_plates = []
# #         self.coco_model = YOLO(r"C:\Users\INTEL\Downloads\yolov8n-seg.pt", verbose=False)
# #         self.vehicles = [1, 2, 3, 5, 7]

# #     def VehicleDetectionv1(self, frame):
# #         vehicles_detected = self.coco_model(frame)
# #         return vehicles_detected

# #     def run_mode(self, source, output):
# #         global margin, stop_processing
# #         cap = ffmpegcv.VideoCapture(source)
# #         vehicle_count = 0

# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# #         out = cv2.VideoWriter(output, fourcc, 20.0, (int(cap.width), int(cap.height)))

# #         save_path = os.path.join(app.config['OUTPUT_FOLDER'])
# #         os.makedirs(save_path, exist_ok=True)

# #         while True:
# #             if stop_processing:
# #                 break

# #             ret, frame = cap.read()
# #             if not ret:
# #                 break

# #             frame = frame.copy()  # Make the frame writable

# #             height, width, _ = frame.shape
# #             y_upper = int(height * 0.5)  # Defining the area for detection
# #             x_left = margin
# #             x_right = width - margin

# #             frame_cropped = frame[:, margin:width - margin]
# #             detected_vehicles = self.VehicleDetectionv1(frame_cropped)

# #             for det in detected_vehicles:
# #                 if det.masks is not None:
# #                     v_masks = det.masks.data.cpu().numpy()  # Get masks
# #                     v_boxes = det.boxes.xyxy.cpu().numpy()  # Get bounding boxes
# #                     v_clss = det.boxes.cls.cpu().numpy()  # Get class ids

# #                     for mask, box, v_cls in zip(v_masks, v_boxes, v_clss):
# #                         if v_cls in self.vehicles:
# #                             bbox_bottom_y = int(box[3])  # Bottom y-coordinate of the bounding box
# #                             bbox_left_x = int(box[0]) + margin  # Left x-coordinate of the bounding box
# #                             bbox_right_x = int(box[2]) + margin  # Right x-coordinate of the bounding box
# #                             bbox_top_y = int(box[1])  # Top y-coordinate of the bounding box

# #                             # Only process vehicles within the defined boundaries
# #                             if bbox_bottom_y >= y_upper and x_left <= bbox_left_x <= x_right:
# #                                 mask_resized = cv2.resize(mask, (frame_cropped.shape[1], frame_cropped.shape[0]))

# #                                 vehicle_img = np.zeros_like(frame)
# #                                 vehicle_cropped = np.zeros_like(frame_cropped)
# #                                 for c in range(3):
# #                                     vehicle_cropped[:, :, c] = np.where(mask_resized > 0.5, frame_cropped[:, :, c], 0)

# #                                 try:
# #                                     vehicle_img[:, margin:width - margin] = vehicle_cropped
# #                                     vehicle_count += 1
# #                                     # Crop the vehicle image to the bounding box
# #                                     cropped_vehicle = vehicle_img[bbox_top_y:bbox_bottom_y, bbox_left_x:bbox_right_x]
# #                                     cv2.imwrite(os.path.join(save_path, f"vehicle_{vehicle_count}.jpg"), cropped_vehicle)
# #                                 except ValueError as e:
# #                                     print(f"Error cropping and saving vehicle image: {e}")

# #             # Draw the boundary lines
# #             cv2.line(frame, (0, y_upper), (width, y_upper), (0, 255, 0), 2)
# #             cv2.line(frame, (x_left, y_upper), (x_left, height), (0, 255, 0), 2)
# #             cv2.line(frame, (x_right, y_upper), (x_right, height), (0, 255, 0), 2)
# #             cv2.putText(frame, f'Vehicle Count: {vehicle_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
# #             out.write(frame)

# #         cap.release()
# #         out.release()

# # main_instance = MainClass()

# # @app.route('/')
# # def index():
# #     return render_template('upload.html')

# # @app.route('/upload', methods=['POST'])
# # def upload_file():
# #     if 'file' not in request.files:
# #         return 'No file part'
# #     file = request.files['file']
# #     if file.filename == '':
# #         return 'No selected file'
# #     if file:
# #         filename = file.filename
# #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #         file.save(file_path)
# #         return jsonify({"file_path": file_path})

# # @app.route('/process', methods=['POST'])
# # def process_file():
# #     global margin, stop_processing
# #     stop_processing = False
# #     file_path = request.form['file_path']
# #     margin = int(request.form['margin'])
# #     output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'processed_' + os.path.basename(file_path))
    
# #     # Run the processing in a separate thread
# #     processing_thread = threading.Thread(target=main_instance.run_mode, args=(file_path, output_path))
# #     processing_thread.start()

# #     return f"File processed and saved as: {output_path}"

# # @app.route('/update_margin', methods=['POST'])
# # def update_margin():
# #     global margin
# #     margin = int(request.form['margin'])
# #     return 'Margin updated'

# # @app.route('/stop', methods=['POST'])
# # def stop_processing():
# #     global stop_processing
# #     stop_processing = True
# #     return 'Processing stopped'

# # @app.route('/uploads/<filename>')
# # def uploaded_file(filename):
# #     return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

# # if __name__ == '__main__':
# #     app.run(debug=True)
















import os
import threading
from flask import Flask, request, render_template, send_from_directory, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import ffmpegcv

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Global variables to control the margin, y_upper factor, and stopping the processing
margin = 50
y_upper_factor = 0.5
stop_processing = False

class MainClass:
    def __init__(self):
        self.vehicle_thread = None
        self.registered_plates = []
        self.coco_model = YOLO(r"C:\Users\INTEL\Downloads\yolov8n-seg.pt", verbose=False)
        self.vehicles = [1, 2, 3, 5, 7]

    def VehicleDetectionv1(self, frame):
        vehicles_detected = self.coco_model(frame)
        return vehicles_detected

    def run_mode(self, source, output):
        global margin, y_upper_factor, stop_processing
        cap = ffmpegcv.VideoCapture(source)
        vehicle_count = 0

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output, fourcc, 20.0, (int(cap.width), int(cap.height)))

        save_path = os.path.join(app.config['OUTPUT_FOLDER'])
        os.makedirs(save_path, exist_ok=True)

        while True:
            if stop_processing:
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame = frame.copy()  # Make the frame writable

            height, width, _ = frame.shape
            y_upper = int(height * y_upper_factor)  # Defining the area for detection
            x_left = margin
            x_right = width - margin

            frame_cropped = frame[:, margin:width - margin]
            detected_vehicles = self.VehicleDetectionv1(frame_cropped)

            for det in detected_vehicles:
                if det.masks is not None:
                    v_masks = det.masks.data.cpu().numpy()  # Get masks
                    v_boxes = det.boxes.xyxy.cpu().numpy()  # Get bounding boxes
                    v_clss = det.boxes.cls.cpu().numpy()  # Get class ids

                    for mask, box, v_cls in zip(v_masks, v_boxes, v_clss):
                        if v_cls in self.vehicles:
                            bbox_bottom_y = int(box[3])  # Bottom y-coordinate of the bounding box
                            bbox_left_x = int(box[0]) + margin  # Left x-coordinate of the bounding box
                            bbox_right_x = int(box[2]) + margin  # Right x-coordinate of the bounding box
                            bbox_top_y = int(box[1])  # Top y-coordinate of the bounding box

                            # Only process vehicles within the defined boundaries
                            if bbox_bottom_y >= y_upper and x_left <= bbox_left_x <= x_right:
                                mask_resized = cv2.resize(mask, (frame_cropped.shape[1], frame_cropped.shape[0]))

                                vehicle_img = np.zeros_like(frame)
                                vehicle_cropped = np.zeros_like(frame_cropped)
                                for c in range(3):
                                    vehicle_cropped[:, :, c] = np.where(mask_resized > 0.5, frame_cropped[:, :, c], 0)

                                try:
                                    vehicle_img[:, margin:width - margin] = vehicle_cropped
                                    vehicle_count += 1
                                    # Crop the vehicle image to the bounding box
                                    cropped_vehicle = vehicle_img[bbox_top_y:bbox_bottom_y, bbox_left_x:bbox_right_x]
                                    cv2.imwrite(os.path.join(save_path, f"vehicle_{vehicle_count}.jpg"), cropped_vehicle)
                                except ValueError as e:
                                    print(f"Error cropping and saving vehicle image: {e}")

            # Draw the boundary lines
            cv2.line(frame, (0, y_upper), (width, y_upper), (0, 255, 0), 2)
            cv2.line(frame, (x_left, y_upper), (x_left, height), (0, 255, 0), 2)
            cv2.line(frame, (x_right, y_upper), (x_right, height), (0, 255, 0), 2)
            cv2.putText(frame, f'Vehicle Count: {vehicle_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            out.write(frame)

        cap.release()
        out.release()

main_instance = MainClass()

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"file_path": file_path})

@app.route('/process', methods=['POST'])
def process_file():
    global margin, y_upper_factor, stop_processing
    stop_processing = False
    file_path = request.form['file_path']
    margin = int(request.form['margin'])
    y_upper_factor = float(request.form['y_upper_factor'])
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'processed_' + os.path.basename(file_path))
    
    # Run the processing in a separate thread
    processing_thread = threading.Thread(target=main_instance.run_mode, args=(file_path, output_path))
    processing_thread.start()

    return f"File processed and saved as: {output_path}"

@app.route('/update_margin', methods=['POST'])
def update_margin():
    global margin
    margin = int(request.form['margin'])
    return 'Margin updated'

@app.route('/stop', methods=['POST'])
def stop_processing():
    global stop_processing
    stop_processing = True
    return 'Processing stopped'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)


