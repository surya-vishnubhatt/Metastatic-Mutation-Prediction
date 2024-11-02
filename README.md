# Metastatic-Mutation-Prediction

### Forward

The following repository serves to store the codebase for my thesis project conducted at the Khurana Lab at the Weill Cornell Graduate School of Medical Sciences (https://khuranalab.med.cornell.edu) an affiliate of the Meyer Cancer Center and the Weill Cornell Department of Physiology and Biophysics. Due to data privacy issues, all data is stored on our lab's compute server, the included Jupyter Notebook and python script houses the code implemented. 

### Abstract 

Metastatic cancer occurs when cancer cells break from the original tumor site, enter the bloodstream or lymphatic system, and spread to other areas of the body; it is considered the final stage of cancer progression. Previous studies have been able to link cancer mutation density to regulatory genomic annotations. This investigation leverages this knowledge, employing a Random Forest model to develop a predictive tool that can serve to explain metastatic cancer mutations, using annotations in primary cancer, which lends key insight towards identifying the cell type of origin of metastasized cancers (i.e. the site of metastasis). This project focuses on primary annotations of colorectal cancer. These annotations include chromatin accessibility (via ATAC-seq), histone modifications (one dimensional H3K27ac), and HCT116 replication timing data. Results show that primary colorectal cancer annotations provide a solid basis for predicting the resulting mutational distribution in metastasis; however, further refinement and validation of the model are necessary to enhance accuracy, applicability, and generalizability.

### Repo Breakdown

```metastatic_SNV_process.py```: Processes raw metastatic mutation information from the Hartwig Medical Database (https://www.hartwigmedicalfoundation.nl/en/)

```main.ipynb```: Houses the bulk of the investigation including exploratory data analysis, data preprocessing, visualization, and Machine Learning Analyses

```Thesis_Writeup.pdf```: Finalized thesis writeup 
