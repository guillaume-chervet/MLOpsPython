# https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/
from dataclasses import dataclass
# vgg16 model used for transfer learning on the dogs and cats dataset
from pathlib import Path

from matplotlib import pyplot
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from tensorflow.keras.optimizers import SGD
import keras
from keras.preprocessing.image import ImageDataGenerator


# define cnn model
def define_model():
    # load model
    model = VGG16(include_top=False, input_shape=(224, 224, 3))
    # mark loaded layers as not trainable
    for layer in model.layers:
        layer.trainable = False
    # add new classifier layers
    output = model.layers[-1].output
    drop1 = keras.layers.Dropout(0.2)(output)
    flat1 = Flatten()(drop1)
    class1 = Dense(64, activation="relu", kernel_initializer="he_uniform")(flat1)
    #class2 = Dense(42, activation="relu", kernel_initializer="he_uniform")(class1)
    output = Dense(3, activation="sigmoid")(class1)
    # define new model
    model = Model(inputs=model.inputs, outputs=output)
    # compile model
    #opt = SGD(lr=0.0002, momentum=0.8)
    #model.compile(
    #    optimizer=opt, loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"]
    #)
    model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    return model


# plot diagnostic learning curves
def summarize_diagnostics(history, output_directory: Path):
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
    plot_filepath = output_directory / "model_plot.png"
    pyplot.savefig(plot_filepath)
    pyplot.close()
    return plot_filepath

@dataclass
class ModelResult:
    evaluate_accuracy_percentage: int
    summary_image_path: Path
    model_path: Path


# run the test harness for evaluating a model
def run_test_harness(input_directory: Path, output_directory: Path, batch_size=64, epochs=7) -> ModelResult:
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    # define model
    model = define_model()
    # create data generator
    datagen = ImageDataGenerator(featurewise_center=True)
    # specify imagenet mean values for centering
    datagen.mean = [123.68, 116.779, 103.939]
    # prepare iterator
    train_it = datagen.flow_from_directory(
        str(input_directory / "train"),
        class_mode="binary",
        batch_size=batch_size,
        target_size=(224, 224)
    )
    validation_it = datagen.flow_from_directory(
        str(input_directory / "evaluate"),
        class_mode="binary",
        batch_size=batch_size,
        target_size=(224, 224)
    )
    # fit model
    history = model.fit_generator(
        train_it,
        steps_per_epoch=len(train_it),
        validation_data=validation_it,
        validation_steps=len(validation_it),
        epochs=epochs,
        verbose=1,
    )
    # test model
    evaluate_it = datagen.flow_from_directory(
        str(input_directory / "test"), class_mode="binary", batch_size=batch_size, target_size=(224, 224)
    )
    _, acc = model.evaluate_generator(evaluate_it, steps=len(evaluate_it), verbose=1)
    evaluate_accuracy_percentage = acc * 100.0
    print("> %.3f" % (evaluate_accuracy_percentage))
    # learning curves
    summary_image_path = summarize_diagnostics(history, output_directory)
    model_path = output_directory / "final_model.keras"
    model.save(str(model_path))
    return ModelResult(evaluate_accuracy_percentage, summary_image_path, model_path)
