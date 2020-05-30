
from word2vec.word2veclite import Word2Vec
#import numpy as np
#import tensorflow as tf


corpus = "I like playing football with my friends"
cbow = Word2Vec(method="cbow", corpus=corpus,
                window_size=1, n_hidden=2,
                n_epochs=10, learning_rate=0.8)
W1, W2, loss_vs_epoch = cbow.run()

print(W1)
#[[ 0.99870389  0.20697257]
# [-1.01911559  2.26364436]
# [-0.69737232  0.14131477]
# [ 3.28315183  1.13801973]
# [-1.42944927 -0.62142097]
# [ 0.65359329 -2.21415048]
# [-0.22343751 -1.17927987]]

print(W2)
#[[-0.97080793  1.21120331  2.15603796 -1.79083151  3.38445043 -1.65295511
#   1.36685097]
# [2.77323464  0.78710269  2.74152617  0.08953005  0.04400675 -1.34149651
#   -2.19375528]]

print(loss_vs_epoch)
#[14.328868654443703, 12.290456644464603, 10.366644621637064,
# 9.1759777684446622, 8.4233626997233895, 7.3952948684910256,
# 6.1727393307549736, 5.1639476117698191, 4.6333377088153043,
# 4.2944697259465485]

#smax=cbow.predict('I like playing',W1,W2)
#print(smax)