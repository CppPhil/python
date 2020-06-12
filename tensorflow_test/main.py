import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

print(tf.version)

rank1_tensor = tf.Variable(["Test", "Ok", "Tim"], tf.string)
rank2_tensor = tf.Variable([["test", "ok", ""], ["", "test", "yes"]], tf.string)

print(tf.rank(rank1_tensor))
print(tf.rank(rank2_tensor))

print(rank1_tensor.shape)
print(rank2_tensor.shape)

tensor1 = tf.ones([1, 2, 3])
tensor2 = tf.reshape(tensor1, [2, 3, 1])
tensor3 = tf.reshape(tensor2, [3, -1])  # -1 infers the actual number

print(tensor1)
print(tensor2)
print(tensor3)

t = tf.zeros([5, 5, 5, 5])
print(t)
t = tf.reshape(t, [125, -1])
print(t)
