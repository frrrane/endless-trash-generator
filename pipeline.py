import time
import os
import uuid
from google import genai
from google.genai import types
from google.cloud import storage

# --- CONFIG ---
PROJECT_ID = 'my-veo-pipeline'
LOCATION = 'us-central1'
BUCKET_NAME = 'veo-output-123'
LOCAL_FILENAME = "output.mp4"

# Initialize Clients
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
storage_client = storage.Client(project=PROJECT_ID)

def run_video_pipeline(prompt):
    """
    Generates a video, saves it to GCS, and downloads a local copy.
    Returns: (gcs_uri, local_path)
    """
    # Create a unique ID for this specific generation
    unique_id = str(uuid.uuid4())[:8]
    blob_name = f"videos/gen_{unique_id}.mp4"
    gcs_uri = f"gs://{BUCKET_NAME}/{blob_name}"

    print(f"🚀 Starting Pipeline: {prompt}")
    print(f"🎬 Video ID: {unique_id}")
    
    # 1. Trigger Generation
    operation = client.models.generate_videos(
        model="veo-3.1-fast-generate-001",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            fps=24,
            aspect_ratio="16:9",
            output_gcs_uri=gcs_uri
        )
    )

    # 2. Polling for Completion
    while not operation.done:
        print("⏳ Rendering on Google Cloud...")
        time.sleep(20)
        operation = client.operations.get(operation)

    # 3. Handle Result
    if operation.result:
        print(f"✅ Generation complete! URI: {gcs_uri}")
        
        # Download logic with a smart retry
        try:
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(blob_name)
            
            # Wait a moment for GCS to index the new file
            time.sleep(5) 
            blob.download_to_filename(LOCAL_FILENAME)
            
            print(f"🎉 SUCCESS! Video saved locally as: {LOCAL_FILENAME}")
            return gcs_uri, LOCAL_FILENAME
        except Exception as e:
            print(f"⚠️ Video is in bucket, but local download failed: {e}")
            return gcs_uri, None
    else:
        print(f"❌ Generation failed: {operation.error}")
        return None, None

if __name__ == "__main__":
    my_prompt = "A high-speed FPV drone shot through a neon-lit canyon, 4k, hyper-realistic"
    
    # This is how you'll capture the values for your YouTube API later
    cloud_uri, local_file = run_video_pipeline(my_prompt)
    
    if cloud_uri:
        print(f"\n--- READY FOR YOUTUBE ---")
        print(f"Cloud Path: {cloud_uri}")
        print(f"Local Path: {local_file}")