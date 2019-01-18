# UnderstandingTopicEvolutionUsingSpatialAutocorrelation
1. Python is used to process the literature datasets downloaded from Web of Science (WoS) core database. Keyword list and abstracts from the literature are obtained.
2. Keywords are represented by the Word2Vec model using the abstract as the training corpus.
3. Keyword vectors are reduced as the keyword points using T-SNE in a two-dimensional plane like a geographical map.
4. After the triangular network built from the keyword points, each keyword is assigned a piece of land.
5. The Spatial Autocorrelation (SA) mapping is drawn using Geoda and R packages for the keyword points.
6. The prediction using SLM is compared with the LM for the top 20 keywords preditions, namely citations before 2010, citations before 2013 used to predict citations before 2016 and the prediction is compared with the real world results.
