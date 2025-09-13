## Tutorial: Data and Model Versioning

Understand the basics of data and model versioning by managing multiple \
datasets and ML models.

### Task

1. Train a ML model on dataset with 1000 images.
2. Version the experiment
3. Retrain the ML model on dataset with 2000 images.
4. Version the experiment
5. Switch between experiments using `dvc checkout`

We'll reuse script developed by Keras Team for model training.

### Pre-requisite

1. DVC
2. Git
3. Python
4. Keras

### Getting Started with Data & Model Versioning

**Switch to DVC env**

```
source dvc-env/bin/activate
```

**Clone the sample code**

```
git clone https://github.com/iterative/example-versioning.git
cd example-versioning
```

**Install the Python Package**

```
pip install -r requirements.txt
```

**Start with Data Setup**

```
dvc get https://github.com/iterative/dataset-registry \
          tutorials/versioning/data.zip
unzip -q data.zip
rm -f data.zip
```

**Track the data**

```
dvc add data
```

**Train the model**

```
python train.py
```

**Track the model**

```
dvc add model.weights.h5
```

*DVC does not commit the data/ directory and model.weights.h5 file with Git. \
Instead, dvc add stores them in the cache (usually in .dvc/cache) and adds them to .gitignore.*

*In this case, we created data.dvc and model.weights.h5.dvc, which contain file \
hashes that point to cached data. We then git commit these .dvc files.*


**Commit the current state**

```
git add data.dvc model.weights.h5.dvc metrics.csv .gitignore
git commit -m "First model, trained with 1000 images"
git tag -a "v1.0" -m "model v1.0, 1000 images"
```

**Untracked files**

```
git status
```

## Second Experiment

Additional images are downloaded

```
dvc get https://github.com/iterative/dataset-registry \
          tutorials/versioning/new-labels.zip
unzip -q new-labels.zip
rm -f new-labels.zip
```

**Track the data, retrain, and then track the new model**

```
dvc add data
python train.py
dvc add model.weights.h5
```

Updated data, model, and metrics.

**Commit the second experiment**

```
git add data.dvc model.weights.h5.dvc metrics.csv
git commit -m "Second model, trained with 2000 images"
git tag -a "v2.0" -m "model v2.0, 2000 images"
```

## Switch between different workspace versions

We use `dvc checkout` command to pull up specific commited version.

**Full workspace checkout**

```
git checkout v1.0
dvc checkout
```

*These commands will restore the workspace to the first snapshot we made: code, data files, model, all of it. DVC optimizes this operation to avoid copying data or model files each time. So dvc checkout is quick even if you have large datasets, data files, or models.*

**Checkout specific data or model**

```
git checkout v1.0 data.dvc
dvc checkout data.dvc
```

**Automate Capturing**

While running pipeline or code that generates files as output, which inturn is \
a dependency to the next workflow. It becomes to difficult to track them manually \
using `dvc add`.

A better approach is `dvc stage add`, it tracks everything as part of dvc pipeline.

Let us switch back to master branch, and remove model.weights.h5.dvc file.

```
git checkout master
dvc checkout
dvc remove model.weights.h5.dvc
```

Track the train as DVC stage and run the pipeline.

```
dvc stage add -n train -d train.py -d data \
          -o model.weights.h5 -o bottleneck_features_train.npy \
          -o bottleneck_features_validation.npy -M metrics.csv \
          python train.py
dvc repro
```

`dvc add` and `dvc checkout` provide a basic mechanism for model and large dataset versioning. \
`dvc stage add` and `dvc repro` provide a build system for machine learning models, which is similar to Make in software build automation.

