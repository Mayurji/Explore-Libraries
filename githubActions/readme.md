# Automate Machine Learning Workflow Using GitHub Actions

It is a powerful tool for continuous integration and continuous delivery (CI/CD) pipeline.

It automates the software development lifecycle, from creating and testing to deploying code.

## GitHub Action Features

- Workflow (yaml file - composed of multiple jobs)
- Jobs and steps (job is a set of steps)
- Events (trigger such push, pull, forks, stars, release, and more)
- Runners (Environment where workflows are executed.)
- Actions (reusable unit of code)

## Kick starting GitHub Action for ML Workflow

1. Setting Up git repo
2. Clone and switch to the repo folder
3. Open the repo in code editor
4. Create a requirements.txt for your ml experiment
5. Download the data (https://www.kaggle.com/datasets/rangalamahesh/bank-churn?select=train.csv)
6. To track the dataset (git-lfs) #sudo apt install git-lfs
7. Write code for ml training - generates evaluation metrics, confusion metrics, and so on.
8. Add files to .gitignore
9. Git add, commit, and push
10. Go to your repo, click Actions.
11. Write main.yaml file with set of config and commands.
```yaml
name: ML Workflow
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch:
  
permissions: write-all

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          lfs: true
      - uses: iterative/setup-cml@v2
      - name: Install Packages
        run: pip install --upgrade pip && pip install -r requirements.txt
      - name: Format
        run: black *.py
      - name: Train
        run: python train.py
      - name: Evaluation
        env:
          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: | 
          echo "## Model Metrics" > report.md
          cat metrics.txt >> report.md
            
          echo '## Confusion Matrix Plot' >> report.md
          echo '![Confusion Matrix](model_results.png)' >> report.md

          cml comment create report.md
```
12. commit changes.
13. Trigger the pipeline by go to action and re-run the pipeline.
14. Make changes in your code base locally, and commit it.
15. After commit, the pipeline will trigger.