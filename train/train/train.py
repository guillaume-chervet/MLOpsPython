# https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/

# vgg16 model used for transfer learning on the dogs and cats dataset
import sys
from matplotlib import pyplot
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from tensorflow.keras.optimizers import SGD
import tensorflow
from keras.preprocessing.image import ImageDataGenerator


# define cnn model
def define_model():
    # load model
    model = VGG16(include_top=False, input_shape=(224, 224, 3))
    # mark loaded layers as not trainable
    for layer in model.layers:
        layer.trainable = False
    # add new classifier layers
    flat1 = Flatten()(model.layers[-1].output)
    class1 = Dense(128, activation="relu", kernel_initializer="he_uniform")(flat1)
    output = Dense(3, activation="sigmoid")(class1)
    # define new model
    model = Model(inputs=model.inputs, outputs=output)
    # compile model
    opt = SGD(lr=0.001, momentum=0.9)
    model.compile(
        optimizer=opt, loss=tensorflow.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"]
    )
    return model


# plot diagnostic learning curves
def summarize_diagnostics(history):
    # plot loss
    pyplot.subplot(211)
    pyplot.title("Cross Entropy Loss")
    pyplot.plot(history.history["loss"], color="blue", label="train")
    pyplot.plot(history.history["val_loss"], color="orange", label="test")
    # plot accuracy
    pyplot.subplot(212)
    pyplot.title("Classification Accuracy")
    pyplot.plot(history.history["accuracy"], color="blue", label="train")
    pyplot.plot(history.history["val_accuracy"], color="orange", label="test")
    # save plot to file
    filename = sys.argv[0].split("/")[-1]
    plot_filename = "../train/" + filename + "_plot.png"
    pyplot.savefig(plot_filename)
    pyplot.close()


# run the test harness for evaluating a model
def run_test_harness():
    # define model
    model = define_model()
    # create data generator
    datagen = ImageDataGenerator(featurewise_center=True)
    # specify imagenet mean values for centering
    datagen.mean = [123.68, 116.779, 103.939]
    # prepare iterator
    train_it = datagen.flow_from_directory(
        "../train/dataset_dogs_vs_cats/train/", class_mode="binary", batch_size=64, target_size=(224, 224)
    )
    test_it = datagen.flow_from_directory(
        "../train/dataset_dogs_vs_cats/test/", class_mode="binary", batch_size=64, target_size=(224, 224)
    )
    # fit model
    history = model.fit_generator(
        train_it,
        steps_per_epoch=len(train_it),
        validation_data=test_it,
        validation_steps=len(test_it),
        epochs=10,
        verbose=1,
    )
    # evaluate model
    evaluate_it = datagen.flow_from_directory(
        "../train/dataset_dogs_vs_cats/evaluate/", class_mode="binary", batch_size=64, target_size=(224, 224)
    )
    _, acc = model.evaluate_generator(evaluate_it, steps=len(evaluate_it), verbose=0)
    print("> %.3f" % (acc * 100.0))
    # learning curves
    summarize_diagnostics(history)
    model.save("../train/final_model.h5")


# entry point, run the test harness
run_test_harness()
