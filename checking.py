from vosk import Model

try:
    model_path = r"E:\FUN_projects\assistant\vosk_model\vosk-model-small-en-us-0.15"
    model = Model(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
