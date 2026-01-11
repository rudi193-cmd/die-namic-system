"""
Vision Board Categorizer
Uses existing analytics pipeline to categorize images for the vision board.

Usage:
    python categorize.py [folder_path] [--portable]
    
    --portable  Embed images as base64 (larger file, but works in browser)
    
Output:
    categories.json - Ready for vision board import
"""

import os
import sys
import subprocess
import json
import urllib.request
from pathlib import Path

import base64

# --- AUTO-INSTALLER ---
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import torch
    from torchvision import models, transforms
    from PIL import Image
except ImportError:
    print("Installing AI Vision libraries (one-time setup)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "--index-url", "https://download.pytorch.org/whl/cpu"])
    import torch
    from torchvision import models, transforms
    from PIL import Image

# --- SETTINGS ---
OUTPUT_FILE = 'categories.json'

# --- CATEGORY MAPPING ---
# Maps ImageNet labels to vision board categories
CATEGORY_MAP = {
    # Personal / Life
    'tabby': 'Personal', 'persian cat': 'Personal', 'siamese cat': 'Personal',
    'golden retriever': 'Personal', 'labrador': 'Personal', 'dog': 'Personal',
    'baby': 'Personal', 'diaper': 'Personal',
    
    # Nature / Travel
    'beach': 'Travel', 'seashore': 'Travel', 'lakeside': 'Travel',
    'mountain': 'Travel', 'volcano': 'Travel', 'valley': 'Travel',
    'coral reef': 'Travel', 'cliff': 'Travel',
    'palace': 'Travel', 'castle': 'Travel', 'monastery': 'Travel',
    
    # Home / Lifestyle
    'dining table': 'Home', 'desk': 'Home', 'bookcase': 'Home',
    'couch': 'Home', 'chair': 'Home', 'lamp': 'Home',
    'kitchen': 'Home', 'refrigerator': 'Home',
    'patio': 'Home', 'garden': 'Home',
    
    # Food
    'pizza': 'Food', 'burger': 'Food', 'sandwich': 'Food',
    'ice cream': 'Food', 'cake': 'Food', 'coffee': 'Food',
    'wine': 'Food', 'beer': 'Food',
    
    # Fitness / Health
    'dumbbell': 'Fitness', 'barbell': 'Fitness',
    'running shoe': 'Fitness', 'bicycle': 'Fitness',
    'yoga': 'Fitness', 'swimming': 'Fitness',
    
    # Career / Professional
    'laptop': 'Career', 'desktop computer': 'Career', 'monitor': 'Career',
    'keyboard': 'Career', 'mouse': 'Career',
    'suit': 'Career', 'tie': 'Career',
    'briefcase': 'Career', 'notebook': 'Career',
    
    # Finance / Wealth
    'sports car': 'Wealth', 'convertible': 'Wealth', 'limousine': 'Wealth',
    'yacht': 'Wealth', 'speedboat': 'Wealth',
    'mansion': 'Wealth',
    
    # Creative / Art
    'paintbrush': 'Creative', 'easel': 'Creative',
    'guitar': 'Creative', 'piano': 'Creative', 'violin': 'Creative',
    'camera': 'Creative', 'tripod': 'Creative',
    
    # Text / Documents (screenshots, memes, etc)
    'web site': 'Text',
    'book jacket': 'Text', 'comic book': 'Text',
    'envelope': 'Text', 'packet': 'Text',
}

# Default category for unrecognized items
DEFAULT_CATEGORY = 'Inspiration'

# --- SETUP THE BRAIN ---
print("Initializing Neural Network...")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

# Download ImageNet labels
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
try:
    with urllib.request.urlopen(LABELS_URL) as url:
        labels = json.loads(url.read().decode())
except Exception:
    print("Warning: Could not download labels.")
    labels = [str(i) for i in range(1000)]

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def generate_thumbnail(img_path, max_dim=200, quality=70):
    """Generate a small JPEG thumbnail as base64."""
    import io
    img = Image.open(img_path).convert('RGB')
    img.thumbnail((max_dim, max_dim))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def analyze_image(image_path):
    """Returns (top_label, confidence, category)"""
    try:
        input_image = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)

        with torch.no_grad():
            output = model(input_batch)
        
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_prob, top_catid = torch.topk(probabilities, 5)
        
        # Check top 5 predictions for category matches
        for i in range(5):
            label = labels[top_catid[i].item()].lower()
            confidence = top_prob[i].item()
            
            # Check for category match
            for key, category in CATEGORY_MAP.items():
                if key in label:
                    return label, confidence, category
        
        # No match found, use top prediction
        top_label = labels[top_catid[0].item()]
        return top_label, top_prob[0].item(), DEFAULT_CATEGORY

    except Exception as e:
        return "unknown", 0.0, DEFAULT_CATEGORY

def categorize_folder(folder_path, portable=False):
    """Categorize all images in a folder"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"ERROR: Folder not found: {folder_path}")
        return None
    
    # Find all images
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    images = [f for f in folder.iterdir() if f.suffix.lower() in extensions]
    
    print(f"Found {len(images)} images to categorize")
    
    results = {
        'source_folder': str(folder.absolute()),
        'categories': {},
        'images': []
    }
    
    for i, img_path in enumerate(images):
        if i % 10 == 0:
            print(f"  Processing {i+1}/{len(images)}...")
        
        label, confidence, category = analyze_image(str(img_path))
        
        # Get image data
        if portable:
            # Generate thumbnail (max 200px, ~5-15KB)
            thumb_data = generate_thumbnail(img_path)
            path_value = f"data:image/jpeg;base64,{thumb_data}"
        else:
            path_value = str(img_path.absolute())
        
        # Build image record
        record = {
            'filename': img_path.name,
            'path': path_value,
            'label': label,
            'confidence': round(confidence * 100, 1),
            'category': category
        }
        results['images'].append(record)
        
        # Track category counts
        if category not in results['categories']:
            results['categories'][category] = []
        results['categories'][category].append(img_path.name)
    
    return results

def main():
    # Parse args
    portable = '--portable' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    folder = args[0] if args else '.'
    
    print(f"\n=== Vision Board Categorizer ===")
    print(f"Scanning: {folder}")
    if portable:
        print("Mode: PORTABLE (embedding images as base64)")
    print()
    
    results = categorize_folder(folder, portable=portable)
    
    if results:
        # Save JSON
        output_path = Path(folder) / OUTPUT_FILE
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Summary
        print("\n" + "=" * 50)
        print("CATEGORIZATION COMPLETE")
        print("=" * 50)
        print(f"\nCategories found:")
        for cat, files in sorted(results['categories'].items()):
            print(f"  {cat}: {len(files)} images")
        print(f"\nOutput: {output_path}")
        print("\nNext: Import categories.json into Vision Board")

if __name__ == "__main__":
    main()
