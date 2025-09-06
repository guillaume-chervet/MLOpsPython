from dataclasses import dataclass
from pathlib import Path

import tensorflow as tf
import keras
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.layers import Dense, Flatten
from keras.models import Model
from matplotlib import pyplot as plt


def define_model(num_classes: int = 3) -> Model:
    base = VGG16(include_top=False, input_shape=(224, 224, 3))
    for layer in base.layers:
        layer.trainable = False

    x = base.output
    x = Flatten()(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base.inputs, outputs=outputs)
    model.compile(
        optimizer="adam",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )
    return model


def _make_ds(dirpath: Path, batch_size: int, shuffle: bool) -> tf.data.Dataset:
    ds = keras.utils.image_dataset_from_directory(
        directory=str(dirpath),
        labels="inferred",
        label_mode="int",          # sparse labels
        image_size=(224, 224),
        batch_size=batch_size,
        shuffle=shuffle,
        seed=1337,
    )
    autotune = tf.data.AUTOTUNE
    # VGG16 preprocess (soustraction des moyennes ImageNet, etc.)
    ds = ds.map(lambda x, y: (preprocess_input(tf.cast(x, tf.float32)), y),
                num_parallel_calls=autotune)
    return ds.prefetch(autotune)


def summarize_diagnostics(history, output_directory: Path) -> Path:
    plt.figure(figsize=(8, 6))
    plt.subplot(2, 1, 1)
    plt.title("Cross Entropy Loss")
    plt.plot(history.history["loss"], label="train")
    plt.plot(history.history["val_loss"], label="val")
    plt.legend()
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

    # jeux de données
    train_ds = _make_ds(input_directory / "train", batch_size, shuffle=True)
    val_ds   = _make_ds(input_directory / "evaluate", batch_size, shuffle=False)
    test_ds  = _make_ds(input_directory / "test", batch_size, shuffle=False)

    # inférer nb classes à partir du dataset
    num_classes = len(train_ds.element_spec[1].shape) if False else None  # placeholder
    # plus simple: lire depuis la structure de dossiers
    class_names = keras.utils.get_file  # dummy to avoid linter (we compute below)
    # On peut récupérer depuis l'itérateur (plus fiable):
    #   Keras ne fournit pas class_names directement pour tf.data, donc on lit le dossier.
    classes = sorted([p.name for p in (input_directory / "train").iterdir() if p.is_dir()])
    model = define_model(num_classes=len(classes))

    callbacks = [
        keras.callbacks.ModelCheckpoint(filepath=output_directory / "final_model.keras",
                                        save_best_only=True, monitor="val_loss"),
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        verbose=1,
        callbacks=callbacks,
    )

    loss, acc = model.evaluate(test_ds, verbose=1)
    evaluate_accuracy_percentage = float(acc) * 100.0

    summary_image_path = summarize_diagnostics(history, output_directory)
    return ModelResult(evaluate_accuracy_percentage, summary_image_path, output_directory / "final_model.keras")
