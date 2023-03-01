import tensorflow as tf

from keras.utils.layer_utils import count_params
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from app.ml.base import BaseMl
from app.schemas.ml import Layer, ModelPrediction, ModelSummaryResponse
from app.services.images import ImageService


class SequentialImageMl(BaseMl):
    IMG_HEIGHT = 360
    IMG_WIDTH = 360
    SEED = 123

    def get_prediction(self, file_path: str) -> ModelPrediction:
        model = self.get_model()
        img = tf.keras.utils.load_img(file_path, target_size=(self.IMG_HEIGHT, self.IMG_WIDTH))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        return ModelPrediction(
            class_name=self.class_names[np.argmax(score)],
            confidence=np.max(score),
        )

    def get_summary(self) -> ModelSummaryResponse:
        model = self.get_model()
        trainable_params = count_params(model.trainable_weights)
        non_trainable_params = count_params(model.non_trainable_weights)
        return ModelSummaryResponse(
            name=model.name,
            total_params=trainable_params + non_trainable_params,
            trainable_params=trainable_params,
            non_trainable_params=non_trainable_params,
            layers=[
                Layer(
                    name=layer.name,
                    class_name=layer.__class__.__name__,
                    params=layer.count_params(),
                    output_shape=layer.output_shape,
                ) for layer in model.layers
            ]
        )

    def _compile_model(self, model):
        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'],
        )

    def _create_model(self, train_ds):
        class_names = train_ds.class_names
        return Sequential([
            layers.Rescaling(1./255, input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(len(class_names))
        ])

    def _get_training_dataset(self):
        return tf.keras.utils.image_dataset_from_directory(
            self.data_dir,
            validation_split=0.2,
            subset="training",
            seed=self.SEED,
            image_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
            batch_size=self.BATCH_SIZE,
        )

    def _get_validation_dataset(self):
        return tf.keras.utils.image_dataset_from_directory(
            self.data_dir,
            validation_split=0.2,
            subset="training",
            seed=self.SEED,
            image_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
            batch_size=self.BATCH_SIZE,
        )

    def _train_model(self, model, train_ds, val_ds):
        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=self.TRAIN_EPOCHS
        )


# Instantiate. This is to allow model to persist between requests.
sequential_image_ml = SequentialImageMl(ImageService.get_downloaded_path())
