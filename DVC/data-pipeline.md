### Building Data Pipeline Using DVC

In ML, only keep tracking of data with versioning is never enough. \
Data needs to be cleaned, filtered, and transformed before sending \
it to ML model.

In this session, we'll discuss how to build a system with DVC that \
is capable of defining, executing and tracking data pipelines — a \
series of data processing stages, that produce a final result.

DVC pipelines are versioned using Git, and allow you to better organize \
projects and reproduce complete workflows and results at will. You \
could capture a simple ETL workflow, organize your project, or build \
a complex DAG (Directed Acyclic Graph) pipeline.

**Steps**

1. Create and clone a git repository.
2. Switch to the git repo
3. Turn the git repo into DVC repo

```
dvc init

git status

git commit -m "initialized dvc"
```

**Download a Sample Code**

```
wget https://code.dvc.org/get-started/code.zip
unzip code.zip && rm -f code.zip
```

**Download the data for example code**

```
dvc get https://github.com/iterative/dataset-registry \
          get-started/data.xml -o data/data.xml
```

**Track the data**

```
dvc add data/data.xml
```

**Install Packages from sample code**

```
pip install -r src/requirements.txt
```

**Git commit the sample code and data**

```
git add .github/ data/ params.yaml src .gitignore #create .gitignore if not present
git commit -m "Initial commit"
```

## Pipeline Stages

Using `dvc stage add` to create stages. It represent processing steps \
(usually scripts/code tracked with Git) and combine to form the pipeline. \
Stages allow connecting code to its corresponding data input and output.

```
dvc stage add -n prepare \
                -p prepare.seed,prepare.split \
                -d src/prepare.py -d data/data.xml \
                -o data/prepared \
                python src/prepare.py data/data.xml
```

A dvc.yaml file is generated. It includes information about the command we \
want to run (python src/prepare.py data/data.xml), its dependencies, and outputs.

DVC uses the pipeline definition to automatically track the data used \
and produced by any stage, so there's no need to manually run dvc add \
for data/prepared!

Similarly, we add the stage for featurizer and training. We define \
outputs of a stage as dependencies of another, we can describe a sequence of \
dependent commands which gets to some desired result. This is what we call a \
dependency graph which forms a full cohesive pipeline.

### Featurize

```
dvc stage add -n featurize \
                -p featurize.max_features,featurize.ngrams \
                -d src/featurization.py -d data/prepared \
                -o data/features \
                python src/featurization.py data/prepared data/features

```

### Train

```
dvc stage add -n train \
                -p train.seed,train.n_est,train.min_split \
                -d src/train.py -d data/features \
                -o model.pkl \
                python src/train.py data/features model.pkl
```

### Running the pipeline

It uses dvc.yaml to easily reproduce the pipeline.

```
dvc repro
```

It will create a `dvc.lock` (a "state file") was created to capture the reproduction's results.

Next, we immediately commit dvc.lock to Git after its creation or modification, to record the current state & results: 

```
git add dvc.lock && git commit -m "first pipeline repro"
```

Visualizing the pipeline

```
dvc dag
```