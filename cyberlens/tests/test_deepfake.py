from models.deepfake_detector import DeepfakeDetector


def test_video_is_marked_as_more_suspicious():
    result = DeepfakeDetector().predict("sample.mp4")
    assert result["label"] == "suspected-deepfake"