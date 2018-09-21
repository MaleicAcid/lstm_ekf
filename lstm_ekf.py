import tensorflow as tf
import os
from numpy import resize, zeros

n_input = 9

def build_dataset():
    cmd = "top -b -n 2 | grep -v Tasks | grep -v top | grep -v %Cpu | grep -v KiB | grep -v PID | grep [0-9] | awk '{print $1,$3,$4,$5,$6,$7,$9,$10,$11}'"
    pstats = os.popen(cmd).read()
    print(pstats)
    print(len(pstats.split()))
    x = tf.Variable( resize(pstats.split(), (250,n_input)), name="inputs" )
    return x

def RNN(x, weights, biases):

    # reshape to [1, n_input]
    x = tf.reshape(x, [-1, n_input])

    # Generate a n_input-element sequence of inputs
    # (eg. [had] [a] [general] -> [20] [6] [33])
    x = tf.split(x,n_input,1)

    # 1-layer LSTM with n_hidden units.
    rnn_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden)

    # generate prediction
    outputs, states = tf.contrib.rnn.static_rnn(rnn_cell, x, dtype=tf.float32)

    # there are n_input outputs but
    # we only want the last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


x = build_dataset()
print(x)

# coefficients in noise and channel matrices, flattened out
vocab_size = 3

# number of units in RNN cell
n_hidden = 512

# RNN output node weights and biases
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, vocab_size]))
}
biases = {
    'out': tf.Variable(tf.random_normal([vocab_size]))
}

pred = RNN(x, weights, biases)

# TODO: implement EKF-based cost function
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(cost)

y = zeros([vocab_size], dtype=float)

_, acc, loss, onehot_pred = tf.Session.run([optimizer, accuracy, cost, pred], feed_dict={x: x, y: y})

