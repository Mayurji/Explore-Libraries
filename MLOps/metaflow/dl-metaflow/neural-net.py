from metaflow import FlowSpec, step, Parameter

class NeuralNetFlow(FlowSpec):
    
    epochs = Parameter('e', default=10)

    @step
    def start(self):
        import numpy as np
        from tensorflow import keras
        self.num_classes = 10
        ((x_train, y_train), 
         (x_test, y_test)) = keras.datasets.mnist.load_data()
        x_train = x_train.astype("float32") / 255
        x_test = x_test.astype("float32") / 255
        self.x_train = np.expand_dims(x_train, -1)
        self.x_test = np.expand_dims(x_test, -1)
        self.y_train = keras.utils.to_categorical(
            y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(
            y_test, self.num_classes)
        self.next(self.build_model)

    @step
    def build_model(self):
        import tempfile
        import numpy as np
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers # pylint: disable=import-error
        self.model = keras.Sequential([
            keras.Input(shape=(28,28,1)),
            layers.Conv2D(32, kernel_size=(3, 3), 
                          activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), 
                          activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation="softmax")
        ])
        self.model.compile(loss="categorical_crossentropy",
                           optimizer="adam", metrics=["accuracy"])
        self.next(self.train)

    @step
    def train(self):
        import tempfile
        import tensorflow as tf
        self.batch_size = 128
        self.model.fit(
            self.x_train, self.y_train,
            batch_size=self.batch_size,
            epochs=self.epochs, validation_split=0.1
        )
        self.next(self.end)

    @step
    def end(self):
        print("NeuralNetFlow is all done.")

if __name__ == "__main__":
    NeuralNetFlow()