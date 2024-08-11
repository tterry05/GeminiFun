import configparser
import google.generativeai as genai
import PIL.Image
import cv2

def draw_box_around_car(image_path, car_center_coordinates_str, box_size=100):
  """
  Draws a red box around the center of a car in an image.

  Args:
      image_path (str): Path to the image.
      car_center_x (int): X-coordinate of the car's center.
      car_center_y (int): Y-coordinate of the car's center.
      box_size (int, optional): Size of the box in pixels. Defaults to 100.

  Returns:
      numpy.ndarray: Image with the red box drawn around the car.
  """
  coordinates = car_center_coordinates_str[1:-1].split(",")  # Remove parentheses and split by comma
  car_center_x = int(coordinates[0])
  car_center_y = int(coordinates[1])

  # Load the image
  img = cv2.imread(image_path)

  # Calculate box coordinates
  top_left_x = car_center_x - box_size // 2
  top_left_y = car_center_y - box_size // 2
  bottom_right_x = car_center_x + box_size // 2
  bottom_right_y = car_center_y + box_size // 2

  # Draw the rectangle
  cv2.rectangle(img, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 0, 255), 2)  # (0, 0, 255) is red, 2 is thickness

  return img

config = configparser.ConfigParser()
config.read('config.ini')
google_key = config['GOOGLEAPI']['googleapi']

genai.configure(api_key=google_key)

model = genai.GenerativeModel('gemini-1.5-flash')
img = PIL.Image.open('car2.jpg')


prompt = ("You are responsible for identifying the exact center of this car. You need to determine how many"
          "pixels are in this image and return the pixel (x,y) coordinates of the center"
          "Your response is to be in this format (x,y) no other words except that")
response = model.generate_content([img, prompt])
print(">" + response.text)

image_with_box = draw_box_around_car('car2.jpg', response.text)

cv2.imshow("Image with Box", image_with_box)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the image with the box
cv2.imwrite("image_with_box.jpg", image_with_box)