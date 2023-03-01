from typing import Dict

from app.schemas.ml import ModelSummaryResponse


class BaseMl:
    BATCH_SIZE = 32
    TRAIN_EPOCHS = 2

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self._model = None  # Model is lazy-loaded.

    def get_model(self):
        if self._model is None:
            self._model = self._generate_model()
        return self._model

    def get_summary(self) -> ModelSummaryResponse:
        raise NotImplementedError

    def reset_model(self):
        """Bust Model cache--next call to `get_model` will rebuild."""
        self._model = None
        self.class_names = None

    def _compile_model(self, model):
        raise NotImplementedError

    def _create_model(self, train_ds):
        raise NotImplementedError

    def _get_training_dataset(self):
        raise NotImplementedError

    def _get_validation_dataset(self):
        raise NotImplementedError

    def _train_model(self, model, train_ds, val_ds):
        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=self.TRAIN_EPOCHS
        )

    def _generate_model(self):
        """
        Follows very simply workflow for generating a model. This
        creates a training/validation set, creates the model, and
        finally trains the model. Inheriting classes must override
        each individual step--this method simply facilitates the full
        build.
        """
        train_ds = self._get_training_dataset()
        val_ds = self._get_validation_dataset()
        model = self._create_model(train_ds)
        self._compile_model(model)
        self._train_model(model, train_ds, val_ds)
        self._compile_model(model)
        self.class_names = train_ds.class_names
        return model
