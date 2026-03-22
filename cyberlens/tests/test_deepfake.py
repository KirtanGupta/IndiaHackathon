from backend.risk_scorer import score_deepfake


def test_video_review_scores_higher_than_audio():
    audio = score_deepfake("audio")
    video = score_deepfake("video")
    assert video["score"] > audio["score"]