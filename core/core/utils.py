def get_test_image_url(image):
    return f'http://testserver{image.url}' if image else None
