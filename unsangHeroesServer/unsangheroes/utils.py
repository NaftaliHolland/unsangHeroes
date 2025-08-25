from cloudinary.utils import cloudinary_url

def get_cloudinary_url(image, width=None, height=None, crop='fill'):
    if not image:
        return None
    url, _ = cloudinary_url(
        image.image,
        width=width, height=height, crop=crop, qualit='auto', fetch_format='auto'
    )
    return url

