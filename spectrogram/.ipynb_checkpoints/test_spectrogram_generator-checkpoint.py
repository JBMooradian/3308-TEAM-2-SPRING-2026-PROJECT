import unittest
import os
import numpy as np
from spectrogram_generator import generate_mel_spectrogram

class TestSpectrogramGenerator(unittest.TestCase):
    
    def setUp(self):
            """Set up paths for testing using OS-agnostic joining."""
            # Path: 3308-TEAM-2-SPRING-2026-PROJECT/data/test/american_robin/american_robin_test.mp3
            self.test_file = os.path.join("..", "data", "test", "american_robin", "american_robin_test.mp3")
            self.expected_mels = 128

    def test_output_type(self):
        """Verify the generator returns a NumPy array."""
        if os.path.exists(self.test_file):
            result = generate_mel_spectrogram(self.test_file)
            self.assertIsInstance(result, np.ndarray, "Output should be a NumPy array.")
        else:
            self.skipTest(f"Missing {self.test_file}. Place a sample audio file in the folder to run.")

    def test_spectrogram_shape(self):
        """Verify the vertical resolution (Mels) is exactly 128 for Peyton's model."""
        if os.path.exists(self.test_file):
            result = generate_mel_spectrogram(self.test_file)
            # result.shape returns (rows, columns) -> (mels, time)
            self.assertEqual(result.shape[0], self.expected_mels, 
                             f"Spectrogram height must be {self.expected_mels}.")

    def test_file_not_found(self):
        """Ensure the code handles missing files gracefully."""
        with self.assertRaises(Exception):
            generate_mel_spectrogram("non_existent_bird_call.mp3")

if __name__ == "__main__":
    unittest.main()