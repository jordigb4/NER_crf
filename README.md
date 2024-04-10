# <span style="font-family:Courier New; color:#CCCCCC">**Named Entity Recognition with CRF**</span>
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

This is a project to program a classifier of the polarity of subjective texts. In a first part, we implement a supervised ML method, using as data the Movie Reviews Corpus of NLTK, made up of 1000 examples of positive opinions and 1000 negative opinions. However, in order to compare the results, we will also want to adopt an unsupervised view, using the polarity scores that SentiWordNet provides.  

Among the objectives, the introduction of concepts and tools of Natural Language Processing stands out, as well as the analysis of which data preprocessing is most appropriate to the task of distinguishing its polarity. In addition, understanding the importance of disambiguation of senses, since relating the syntactic and semantic content of a sentence will lead models to better results.

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
  git clone https://github.com/jordigb4/Opinion_detection-Supervised-Unsupervised-.git
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

    .
    ├── models                                  # Trained models
    ├── images                                  # Resulting Confusion Matrices
    ├── contractions.py                         # Dict with english contractions expansion
    ├── text_normalizer.py                      # Text preprocessing function
    ├── textserver.py                           # Word Sense Desambiguation Module
    ├── hybrid_classifier.py                    # Class with hybrid classifier 
    ├── OpinionDetection-Supervised.ipynb       # Work on supervised classifiers
    ├── OpinionDetection-Unsupervised.ipynb     # Work on SentiWordnet-based model
    ├── OpinionDetection-Hybrid.ipynb           # Mix Supervised-Unsupervised
    └── README.md

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
