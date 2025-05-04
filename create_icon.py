from PIL import Image
import os

def create_icon():
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Open the PNG image
    img = Image.open('assets/player.png')
    
    # Convert to RGBA if not already
    img = img.convert('RGBA')
    
    # Create icon sizes
    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    icon_images = []
    
    # Resize image for each size
    for size in sizes:
        resized_img = img.resize(size, Image.Resampling.LANCZOS)
        icon_images.append(resized_img)
    
    # Save as ICO
    icon_images[0].save('assets/icon.ico', format='ICO', sizes=[(x.width, x.height) for x in icon_images], append_images=icon_images[1:])

if __name__ == '__main__':
    create_icon() 