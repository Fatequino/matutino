import os

from mediapipe.calculators.core import constant_side_packet_calculator_pb2
from mediapipe.python.solution_base import SolutionBase


UPPER_BODY_ONLY=True
SMOOTH_LANDMARKS=True
STATIC_IMAGE_MODE=False

TEXT_GRAPH_PATH = "fatequino_vision_holistic_cpu.pbtxt"

class CustomHolistic(SolutionBase):
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):

        #Packets parameters 
        side_inputs={
            'upper_body_only': UPPER_BODY_ONLY,
            'smooth_landmarks': SMOOTH_LANDMARKS and not STATIC_IMAGE_MODE,
        }

        #Outputs
        outputs=[
            'face_roi_from_pose', 'left_hand_landmarks', 'right_hand_landmarks', 'pose_landmarks'
        ]

        calculator_params={
            'poselandmarkcpu__ConstantSidePacketCalculator.packet': [
                constant_side_packet_calculator_pb2
                .ConstantSidePacketCalculatorOptions.ConstantSidePacket(
                    bool_value=not STATIC_IMAGE_MODE)
            ],
            'poselandmarkcpu__posedetectioncpu__TensorsToDetectionsCalculator.min_score_thresh':
                min_detection_confidence,
            'poselandmarkcpu__poselandmarkbyroicpu__ThresholdingCalculator.threshold':
                min_tracking_confidence,
        }

        root_path = os.path.dirname(os.path.abspath(__file__))
        text_graph_path = os.path.join(root_path, TEXT_GRAPH_PATH)
        text_config = self.read_graph_file(text_graph_path)
        
        
        super().__init__(
            graph_config=text_config,
            side_inputs = side_inputs,
            calculator_params = calculator_params,
            outputs = outputs
        )

    def process(self, image):
        results = super().process(input_data={'image': image})
        # if results.pose_landmarks:
        #     for landmark in results.pose_landmarks.landmark:
        #         landmark.ClearField('presence')
        return results

    def read_graph_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path + " not exists" )
        with open(file_path, "r") as f:
            return f.read()