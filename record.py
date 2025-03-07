from brainlabgp3 import BrAInLabGP3

if __name__ == "__main__":
    bl_gp3 = BrAInLabGP3() #connect to the stimulus machine, leave empty to connect to the local machine
    # bl_gp3.calibrate(show_calibration_result_time=2,calibration_result_log="calib.log") # run calibration from script or manually from Gazepoint Control
    bl_gp3.request_gaze_data_stream()
    while True:
        bl_gp3.send_gaze_to_lsl()