"""
tools to explore effect of hyperparameters
"""

import tensorflow as tf


def build_model(input_dim, output_dim, options):
    """Build a keras model using the Sequential API.

    Arguments:
        input_dim {int} -- number of input features
        output_dim {int} -- number of output features
        options {dict} -- dictionary containing all network options
            should contain the keys:
                n_hidden_layers {int} -- number of hidden layers
                units {list} -- list of ints of length `n_hidden_layers`
                batch_norm {bool} -- to use BatchNormalization layers or not
                activation {tf.keras activation layer} -- e.g. layers.ReLU
                activation_kwargs {dict} -- containing options for act. layer

    Returns:
        keras Sequential model -- [description]
    """
    options = options.copy()
    if options['batch_norm']:
        use_bias = False
    else:
        use_bias = True

    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(input_dim,)))

    for i in range(options['n_hidden_layers']):
        model.add(tf.keras.layers.Dense(
            options['units'][i], use_bias=use_bias))
        if options['batch_norm']:
            model.add(tf.keras.layers.BatchNormalization())
        model.add(options['activation'](**options['activation_kwargs']))

    model.add(tf.keras.layers.Dense(output_dim, activation='linear'))

    return model


def compile_model(model, options):
    """compile a model

    Arguments:
        model {keras Sequential model} -- pre-build model ready for compilation
        options {dict} -- dictionary containing compilation options.
            Should contain the keys:
                optimizer {tf.keras.optimizer} -- e.g. optimizer.Adam
                learning_rate {float} -- initial learning rate
                loss {str} -- loss function to use
                metrics {list} -- list of strings containing metrics

    Returns:
        keras Sequential model -- [description]
    """
    options = options.copy()
    opt = options['optimizer'](learning_rate=options['learning_rate'])
    model.compile(loss=options['loss'],
                  metrics=options['metrics'], optimizer=opt)

    return model
