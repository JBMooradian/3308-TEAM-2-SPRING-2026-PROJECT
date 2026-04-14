# Guide to the New Folders and Files
---
### This commit has quite a lot of new stuff in it. Key new features include:
- birdTrapper shell script showcased in our Week 8 Sprint. Use this to gather more samples from xeno-canto.org
- trapped_birds_nest directory, which is the default destination for scraped audio files
- Additional source files added to reference and test to practice and train on
- NeuralNetwork, model, and spectrograms directories, all used in the new offline pipeline

As we discussed in Sprint 8, the new pipline is split into two separate streams: offline and online 

offline: dataset_builder(used on reference files) -> nn_trainer(to generate traing arrays) -> populate model dir \
online: user input(via UI) -> classifier (one-time generation of input spec saved to memory only) -> compare against trained data -> output confidence level and SQL query for highest match bird data

---
### birdTrapper.sh
- Run this shellscript with the format $ bash birdTrapper.sh https://xeno-canto.org/[page_code]
- It will scrape and dump the .mp3 file from the specified page to the nest directory
- It will name the .mp3 dump with the format Bird_Name-Species_name(entrycode).mp3 to retain cited source info and bird details. This info can be used in SQL queries

### spectrograms directory
- This directory has been populated with numpy arrays that have been generated via the new combination program dataset_builder, which bundles functions from Bri and Peyton's scripts
- the .npy binaries can now be sourced as reference files for the new classifier program

### model directory
- destination of the trained model (bird_nn.npy) and the bird labels (labels.npy) for use in the classifier program and future training

### NeuralNetwork
- The big one! Following a tutorial found at https://pyimagesearch.com/2021/05/06/backpropagation-from-scratch-with-python/, I built a standard backpropagation model to be used in the offline pipeline
- nn_original_comments.py is the untouched version from the tutorial, with modified comments from me so that it is easier to follow the math
- nn.py is used in the offline pipeline. It has an added @classmethod so it can load saved training data for future training, and comments have been removed for easier adaptation
- dataset_builder.py is a combination of Bri's generate_mel_spectrogram function and Peyton's normalize function, so that spectrogram arrays can be generated, normalized, and saved offline. It includes a loop function for one-and-done
- nn_trainer.py is the entry point of the offline pipline. Use this to call the .fit() function from the NeuralNetwork class to generate two trained binaries, saved in the model directory
- classifier.py is a prototype to replace similarity_ranker as the main program for UI output. Structure is nearly identical to similarity_ranker, with the main differences being:
  - it loads the trained model for a one-to-many confidence comparison, rather than a one-time correlation score
  - identify_bird() calls nn.predict() rather than scipy.correlate()
  - it also flattens and crops the spectrogram in one function, padding misaligned inputs with zeros, rather than cropping shape. This ideally avoids data loss (this should probably be hoisted into the dataset_builder)
  - return printout provides confidence scores rather than ranked scores. Results from first train are inaccurate.
- ranker_rewrite was my first attempt at optimizing similarity_ranker by relying on pre-generated spectogram arrays. Included here for process preservation, and is not used

---
# Next Steps
- As it stands, the basic neural network implementation is not efficient for one-to-many comparisons.
- The original implementation uses a linear regression model, but we have multiple possibilities. This math needs to be refactored
- Sigmoid activation can get easily overwhelmed with several cases. Again, linear regression is not a good fit (pun intended)
- The error rate is MSE (mean squared error), so it has the same problem as sigmoid. Convolutional logic needs to be looked into.
- On the first train, error rate plateaued at about 0.7, which indicates poor optimization and ill-fitting math.



Note: you may need to move these files into the top of the directory in order to experiment with them. I am still not very good with PATH finding variables, and trying the sys function that Peyton wrote has not worked for me.