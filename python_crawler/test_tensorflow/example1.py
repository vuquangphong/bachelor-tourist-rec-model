import tensorflow as tf

# define the shape of the input tensor
input_shape = (32, 32, 3)  # (height, width, channels)

# create an input tensor with the given shape and data type
input_tensor = tf.keras.Input(shape=input_shape, dtype=tf.float32)

print(input_tensor)