import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify
from shop.models import Product, Category
from django.core.files.base import ContentFile

from PIL import Image
import io

def crop_to_square(img):
    w, h = img.size
    min_side = min(w, h)
    left = (w - min_side) // 2
    top = (h - min_side) // 2
    right = left + min_side
    bottom = top + min_side
    return img.crop((left, top, right, bottom))


# img = Image.open(...)
# resized = img.resize((512, 512), Image.LANCZOS)

# Convert back to bytes
# buffer = io.BytesIO()
# resized.save(buffer, format="JPEG")  # or "PNG", "WEBP", etc.
# buffer.seek(0)  # rewind to start!
# img = Image.open("input.jpg")
# square = crop_to_square(img)
# resized = square.resize((512, 512), Image.LANCZOS)
# resized.save("output.jpg")


class Command(BaseCommand):

    help = "Load product images from a folder"

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str)

    def handle(self, *args, **kwargs):

        folder = kwargs["folder"]

        category = Category.objects.first()

        count = 0
        product = Product.objects.all()

        for file_name in os.listdir(folder):

            if file_name.endswith((".jpg", ".jpeg", ".png")):

                path = os.path.join(folder, file_name)

                name = os.path.splitext(file_name)[0]

                
                print(f'yess {file_name}')

                with Image.open(path) as f:
                    square = crop_to_square(f)
                    resized = square.resize((300, 300), Image.LANCZOS)

                    #reading back to bytes to save in an image field
                    buffer = io.BytesIO()
                    resized.save(buffer, format="PNG")  # or "PNG", "WEBP", etc.
                    buffer.seek(0)

                    product[count].image.save(file_name, ContentFile(buffer.read()), save=True)
                    count +=1


                # with open(path, "rb") as f:
                #     square = crop_to_square(f)
                #     resized = square.resize((300, 300), Image.LANCZOS)

                #     product = Product.objects.create(
                #         category=category,
                #         name=name,
                #         slug=slugify(name),
                #         price=12.50,
                #         available=True
                #     )
                

                    # product[count].image.save(file_name, File(resized), save=True)
                    # count +=1

                self.stdout.write(self.style.SUCCESS(
                        f"Finished Succesfully {name}"
                    ))