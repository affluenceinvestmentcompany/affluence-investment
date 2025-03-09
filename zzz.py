import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "dpkcmu4xp", 
    api_key = "119471239953182", 
    api_secret = "wDigTq27C7yRdsxSiEsJ3ywABIc",
    secure=True
)

# Upload an image
upload_result = cloudinary.uploader.upload("./staticfiles/images/logo.png", public_id="logo")
print(upload_result["secure_url"])

# Optimize delivery by resizing and applying auto-format and auto-quality
optimize_url, _ = cloudinary_url("logo", fetch_format="auto", quality="auto")
print(optimize_url)

# Transform the image: auto-crop to square aspect_ratio
auto_crop_url, _ = cloudinary_url("logo", width=500, height=500, crop="auto", gravity="auto")
print(auto_crop_url)