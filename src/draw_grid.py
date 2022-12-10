from PIL import Image, ImageDraw

def draw_grid(n, values):
  # Create a new image with dimensions n x n
  img = Image.new("RGB", (n, n))

  # Create a drawing context for the image
  draw = ImageDraw.Draw(img)

  # Iterate over the values in the grid
  for i in range(n):
    for j in range(n):
      # Get the value at position (i, j)
      value = values[i][j]

      # Calculate the color for the square at position (i, j)
      color = (value, value, value)

      # Draw a square at position (i, j) with the calculated color
      draw.rectangle((i, j, i + 1, j + 1), fill=color)

  # Display the image
  img.show()

# Example usage
n = 5
values = [[0, 255, 0, 255, 0],
          [255, 0, 255, 0, 255],
          [0, 255, 0, 255, 0],
          [255, 0, 255, 0, 255],
          [0, 255, 0, 255, 0]]
draw_grid(n, values)
