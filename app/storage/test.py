import file_storage as storage

import io
import os
import tempfile

# --- setup temp storage ---
tmpdir = tempfile.TemporaryDirectory()
storage.STORAGE_DIR = tmpdir.name

# --- fake video file ---
video_bytes = b"fake video data"
fake_file = io.BytesIO(video_bytes)

# --- call function ---
video_id = storage.store_video(fake_file, "test.mp4")

# --- assertions ---
assert isinstance(video_id, str), "video_id should be a string"
assert len(video_id) > 0, "video_id should not be empty"

stored_path = os.path.join(tmpdir.name, f"{video_id}.mp4")
assert os.path.exists(stored_path), "stored file does not exist"

with open(stored_path, "rb") as f:
    assert f.read() == video_bytes, "file content mismatch"

print("✅ store_video test passed")

# --- cleanup ---
tmpdir.cleanup()
