import os

def doesPostExist(id):
    if os.path.exists(f"results/{id}.mp4") or os.path.exists(f"images/{id}.png"):
        return True
    return False