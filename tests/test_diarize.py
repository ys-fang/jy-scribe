import numpy as np
from unittest.mock import patch, MagicMock
from jy_scribe.diarize import diarize_segments


def test_diarize_returns_labels_per_segment():
    segments = [
        {"start": 0.0, "end": 3.0, "text": "Hello"},
        {"start": 3.5, "end": 6.0, "text": "Hi"},
        {"start": 6.5, "end": 9.0, "text": "Bye"},
    ]

    fake_embeddings = np.random.rand(3, 256).astype(np.float32)

    with patch("jy_scribe.diarize.VoiceEncoder") as MockEncoder, \
         patch("jy_scribe.diarize.SpectralClusterer") as MockClusterer, \
         patch("jy_scribe.diarize.load_audio_segment") as mock_load:

        mock_encoder = MagicMock()
        MockEncoder.return_value = mock_encoder
        mock_encoder.embed_utterance.side_effect = [
            fake_embeddings[i] for i in range(3)
        ]

        mock_load.return_value = np.zeros(16000, dtype=np.float32)

        mock_clusterer = MagicMock()
        MockClusterer.return_value = mock_clusterer
        mock_clusterer.predict.return_value = np.array([0, 1, 0])

        labels = diarize_segments("test.wav", segments)

        assert len(labels) == 3
        assert labels[0] == 0
        assert labels[1] == 1
        assert labels[2] == 0


def test_diarize_with_num_speakers():
    segments = [{"start": 0.0, "end": 2.0, "text": "A"}]

    with patch("jy_scribe.diarize.VoiceEncoder") as MockEncoder, \
         patch("jy_scribe.diarize.SpectralClusterer") as MockClusterer, \
         patch("jy_scribe.diarize.load_audio_segment") as mock_load:

        mock_encoder = MagicMock()
        MockEncoder.return_value = mock_encoder
        mock_encoder.embed_utterance.return_value = np.zeros(256)

        mock_load.return_value = np.zeros(16000, dtype=np.float32)

        mock_clusterer = MagicMock()
        MockClusterer.return_value = mock_clusterer
        mock_clusterer.predict.return_value = np.array([0])

        diarize_segments("test.wav", segments, num_speakers=3)

        init_kwargs = MockClusterer.call_args[1]
        assert init_kwargs["min_clusters"] == 3
        assert init_kwargs["max_clusters"] == 3
