from flask import Flask, render_template, request, jsonify
import pandas as pd
import math
import os

app = Flask(__name__)

calorie_burn_rate = 0.002  # An arbitrary value representing the calorie burn rate per unit of movement

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_keypoints():
    global prev_keypoints
    data = request.json
    keypoints = data.get('keypoints', [])
    weight = data.get('weight', 70)  # get the user's weight from the request, default to 70kg if not provided
    
    # Calculate calories based on the movement
    if prev_keypoints:  # calculate the movement if we have previous keypoints to compare
        total_movement = sum(
            math.sqrt((x['x'] - prev_x['x']) ** 2 + (x['y'] - prev_x['y']) ** 2) 
            for x, prev_x in zip(keypoints, prev_keypoints)
        )
        calories_burned = total_movement * calorie_burn_rate * weight
    else:
        calories_burned = 0
    
    prev_keypoints = keypoints  # update the previous keypoints
    print(calories_burned)
    
    # Prepare the keypoints data
    data_df = pd.DataFrame(keypoints)
    pose_landmarks = [
        "Nose", "Left Eye Inner", "Left Eye", "Left Eye Outer", "Right Eye Inner",
        "Right Eye", "Right Eye Outer", "Left Ear", "Right Ear", "Mouth Left",
        "Mouth Right", "Left Shoulder", "Right Shoulder", "Left Elbow", "Right Elbow",
        "Left Wrist", "Right Wrist", "Left Pinky", "Right Pinky", "Left Index",
        "Right Index", "Left Thumb", "Right Thumb", "Left Hip", "Right Hip",
        "Left Knee", "Right Knee", "Left Ankle", "Right Ankle", "Left Heel",
        "Right Heel", "Left Foot Index", "Right Foot Index"
    ]
    data_df['Pose Landmark'] = pose_landmarks
    
    #print(data_df)
    return jsonify({"status": "success", "calories_burned": calories_burned})

prev_keypoints = None  # to store the previous frame's keypoints


if __name__ == '__main__':
    # Use the provided $PORT variable by Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

