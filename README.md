# deep-president

Backend:
The package uses a Deep LSTM to generate presidential speeches. Developed all in Python. We also provide a HMM option, which is considerably faster to train. The comparison of generated text is shown below in the #comparison section.

Frontend:
The speech is fed through AWS to Alexa for text-to-speech. Developed in Javascript. 

## Getting Started with Our Backend Scripts

The scripts included in the backends can be run individually without having a front-facing interface. We will demonstrate how to install all the dependencies.

### Prerequisites

The backend is developed in Python, and we will be using `pip` for installing that. 

The system is assumed to have installed CUDA (v8.0), cuDNN, [Keras](https://github.com/NVIDIA/keras) (version 1.2.2) with mxnet (`pip install mxnet-cu80==0.11.0`) backend.
```
pip install tqdm
pip install autocorrect
pip install nltk
pip install numpy
```
### Installing

```
git clone https://github.com/hi-im-ryanli/deep-president.git
```

## Running the model and generate some speeches!

Run the code with our pretrained model inside of `models`.
```
python pipeline.py
```

## Train your own model
Based on your GPU specs, training might be potentially a long wait. We trained our model on AWS `p2.16xlarge` and the scaling is awesome. The network defined here has around `10,000,000` parameters to train, and we are feeding it with around `1,500,000` training samples.

You can modify our model architecutre based on your hardware. Fewer layers and smaller unit sizes will speed up the training process, with the trade of losing expressive power on the LSTM networks.

The network training is done inside of `deep-text-char.py`, and modify the network as you see fit in `LSTM()`.

Compile and run your final model like this:
```
ryan = DeepText(folderName='democrat')
raw = ryan.LoadText()
ryan.GenrateData(raw)
model = ryan.LSTM()
ryan.Compile(model)
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* LTSM model: Keras, Python

* Data scraping: BeautifulSoup, Python

* Server: Amazon EC2 (AWS), Flask

* User Interfaces: React, HTML, CSS, Amazon Alexa Echo

## Authors

* Aidan Curtis
* Titus Deng
* Ryan Li
* Linus Shih
* Gary Wang

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments