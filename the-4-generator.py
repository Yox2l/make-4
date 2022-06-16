import cairo
import math
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import img_to_array, load_img
import pytesseract


SIZE = 4
PIXEL_SIZE = 28
def draw_vector(context, vector):
    x1, y1, x2, y2 = vector
    context.set_line_width(0.05)
    context.move_to(x1/100, y1/100)
    context.line_to(x2/100, y2/100)
    context.stroke()    

def draw(name, vectors):
    with cairo.SVGSurface(f"{name}.svg", PIXEL_SIZE, PIXEL_SIZE) as surface:
        context = cairo.Context(surface)
        context.set_source_rgb(1, 1, 1)
        context.paint()
        context.set_source_rgb(0, 0, 0)
        context.scale(PIXEL_SIZE, PIXEL_SIZE)
        i = 0
        while i < len(vectors):
            draw_vector(context, vectors[i:i+SIZE])
            i += SIZE
        surface.write_to_png(f"{name}.png")

def mutate(vector, prev_score):
    chance_of_change = max(0.1, math.sqrt(1 - prev_score)/2)
    value_of_change = int(max(12 * (1-prev_score) ** 1.3, 2))
    new_vec = []
    for v in vector:
        new_value = v 
        if np.random.rand() < chance_of_change:
            new_value += np.random.randint(-value_of_change, value_of_change)
            new_value = new_value % 100
        new_vec.append(new_value)
    return tuple(new_vec)

def make_x_mutation(vector, prev_score, x):
    new_vectors = set()
    new_vectors.add(vector)
    while len(new_vectors) < x:
        new_vectors.add(mutate(vector, prev_score))
    new_vectors.remove(vector)
    return list(new_vectors)


reconstructed_model = tf.keras.models.load_model("to_4_or_not_to_4_model.h5")

def evluate_png(filename):
    arr = img_to_array(load_img(filename, color_mode='grayscale', target_size=(PIXEL_SIZE, PIXEL_SIZE)))
    arr = arr.astype('float32')
    arr = arr/255
    arr = arr.reshape(1, PIXEL_SIZE, PIXEL_SIZE, 1)
    pred = reconstructed_model.predict(arr)
    return pred[0][1]

VECTOR_SIZE = 12 # 3 lines
MAX_ITERATIONS = 300

def main():
    best_vector = tuple(np.random.randint(0, 100, VECTOR_SIZE))
    itr = 0
    print(itr, best_vector)
    while True:
        itr += 1
        best_score = -1
        for vector in make_x_mutation(best_vector, 0, 10):
            draw("tmp_image", vector)
            score = evluate_png("tmp_image.png")
            # print(score, best_score)
            if score > best_score:
                # print("==>",score, best_score)
                best_vector = vector
                best_score = score
        print(itr, best_vector, best_score)
        if best_score > 0.99:
            break
        if itr > MAX_ITERATIONS:
            break
    draw("best_image", best_vector)
    return best_vector, best_score

# print(main())
if __name__ == "__main__":
    main()