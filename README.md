# Text-Classification

This work represents a project for the clustering of text documents by keywords in Russian, in particular, patent abstracts. This is a clustering task. Algorithm testing is carried out in two stages. First, the results are analyzed on the trained sample, and then the clustering analysis is used for a new sample.

### Files : 

\begin{itemize}
    \item google\_patents.csv - result from google patents service
    \item patents.csv - downloaded patent texts 
    \item clusters.csv -  is the data on which the model was trained with the clustering result
    \item validation.csv - new data sample with clustering results
    \item frequensy.csv - result of frequency analysis
    \iten converter.py - code parse data from google\_patents.csv and the web links of files and extract text from the pdf file.
    \item cluster.ipynb - code with preprocessing of data and clustering
    
\end{itemize}
