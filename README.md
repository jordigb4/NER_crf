# <span style="font-family:Courier New; color:#CCCCCC">**Named Entity Recognition using CRF**</span>

<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/albertojc6/Opinion_detection-Supervised-Unsupervised-">
    <img src="images/NER-Text.png" alt="Logo" width="200" height="200">
  </a>

<h3 align="center"></h3>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#repo-structures">Repository Structures</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

In this project, we employ Conditional Random Fields (CRF), a stochastic discriminative model commonly used for labeling data, to perform named entity recognition. We utilize a CRF model for each language to compare their performance and analyze the preprocessing steps tailored to each dataset.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites


* Python
  ```sh
  pip install nltk
  pip install numpy
  ```

### Installation

1. Clone the repo
  ```sh
  git clone https://github.com/jordigb4/NER_crf
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

```python
from hybrid_classifier import HybridClassifier

# Train classifier
classifier = HybridClassifier()

#Predict
pred = classifier.predict(X_test)
print(pred)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Repository Structures

    ª   CADEC_crf.ipynb                   # Cadec dataset NER
    ª   feature_getter.py                 # Class with feature getter
    ª   hyper&feature_opt-esp.ipynb       # Hiperparameter and feature selection spanish dataset
    ª   hyper&feature_opt-ned.ipynb       # Hiperparameter and feature selection dutch dataset
    ª   NER_evaluation.py                 # Evaluation functions and metrics
    ª   preprocessing.py                  # Preprocessing and tag converting functions
    ª   README.md
    ª   test.ipynb                        # Results and conclusion with final models
    
    +---data                              # Labeled CADEC datasets
        ª       test.conll                
        ª       train.conll     
    +---images                            
        ª       esp_confusion_matrix.png
        ª       ned_confusion_matrix.png
        ª       NER-Text.png    
        

<p align="right">(<a href="#repo-structures">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

[Alberto J. LinkedIn](https://www.linkedin.com/in/alberto-jerez-cubero-65abb82a3/)  
[Jordi G. LinkedIn](https://www.linkedin.com/in/jordi-granja-bayot/)

Project Link: [https://github.com/jordigb4/Opinion_detection-Supervised-Unsupervised-](https://github.com/jordigb4/Opinion_detection-Supervised-Unsupervised-)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
