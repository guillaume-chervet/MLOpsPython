from dataclasses import dataclass
from pathlib import Path

import keras
from keras.applications.vgg16 import VGG16
from keras.layers import Dense, Flatten
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator  # ok to keep; Keras 3 still ships legacy API
from matplotlib import pyplot as plt


# define cnn model
def define_model(num_classes: int = 3) -> Model:
    # load base model
    base = VGG16(include_top=False, input_shape=(224, 224, 3))
    # freeze base
    for layer in base.layers:
        layer.trainable = False

    # add classifier head
    x = base.layers[-1].output
    x = Flatten()(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base.inputs, outputs=outputs)
    model.compile(
        optimizer="adam",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )
    return model


def summarize_diagnostics(history, output_directory: Path) -> Path:
    plt.figure(figsize=(8, 6))
    # loss
    plt.subplot(2, 1, 1)
    plt.title("Cross Entropy Loss")
    plt.plot(history.history["loss"], label="train")
    plt.plot(history.history["val_loss"], label="val")
    plt.legend()
    # accuracy
    plt.subplot(2, 1, 2)
    plt.title("Classification Accuracy")
    plt.plot(history.history["accuracy"], label="train")
    plt.plot(history.history["val_accuracy"], label="val")
    plt.legend()

    plot_filepath = output_directory / "model_plot.png"
    plt.tight_layout()
    plt.savefig(plot_filepath)
    plt.close()
    return plot_filepath


@dataclass
class ModelResult:
    evaluate_accuracy_percentage: float
    summary_image_path: Path
    model_path: Path


def run_test_harness(
    input_directory: Path, output_directory: Path, batch_size: int = 64, epochs: int = 7
) -> ModelResult:
    output_directory.mkdir(parents=True, exist_ok=True)

    # define model (3 classes: e.g., cats/dogs/others)
    model = define_model(num_classes=3)

    # data pipeline
    datagen = ImageDataGenerator(featurewise_center=True)
    datagen.mean = [123.68, 116.779, 103.939]

    train_it = datagen.flow_from_directory(
        str(input_directory / "train"),
        class_mode="sparse",               # <-- multi-class integer labels
        batch_size=batch_size,
        target_size=(224, 224),
        shuffle=True,
    )
    val_it = datagen.flow_from_directory(
        str(input_directory / "evaluate"),
        class_mode="sparse",
        batch_size=batch_size,
        target_size=(224, 224),
        shuffle=False,
    )

    # callbacks
    model_path = output_directory / "final_model.keras"
    callbacks = [
        keras.callbacks.ModelCheckpoint(filepath=model_path, save_best_only=True, monitor="val_loss"),
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),
    ]

    # Keras 3: use fit() directly (fit_generator is removed)
    history = model.fit(
        train_it,
        steps_per_epoch=len(train_it),
        validation_data=val_it,
        validation_steps=len(val_it),
        epochs=epochs,
        verbose=1,
        callbacks=callbacks,
    )

    # evaluate (evaluate_generator is removed)
    test_it = datagen.flow_from_directory(
        str(input_directory / "test"),
        class_mode="sparse",
        batch_size=batch_size,
        target_size=(224, 224),
        shuffle=False,
    )
    loss, acc = model.evaluate(test_it, steps=len(test_it), verbose=1)
    evaluate_accuracy_percentage = float(acc) * 100.0

    summary_image_path = summarize_diagnostics(history, output_directory)
    return ModelResult(evaluate_accuracy_percentage, summary_image_path, model_path)
