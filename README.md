# Package for Information Extraction from Arabic Medical Leaflets to use in web or other applications

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Collecting various information types from text and making it smoothly accessible for humans in
the simplest form has been a main concern over the past years. There has been increased interest
in extracting information from unstructured text and to acquire new organized data, which could
be achieved using information extraction. Information extraction provides semantic interpretation
which in turn solves some of the problems related to unstructured text processing and text mining.
Information extraction is gaining popularity in many languages and since the Arabic language has
earned its place on the web among other international languages, and along with the constant growth
of unstructured Arabic content, the necessity to extract information from Arabic documents has
evolved.
Data volume is in constant rise in many fields, and with the rapid increase of information comes a
great need for processing powers that far exceeds our ability to extract this knowledge manually.
Amid these fields is the medical one, where People’s awareness of the health culture makes the task
of automating the medical informatics processes crucial for better access to medical knowledge.
The need for extracting information from medical documents, and specifically drug leaflets, has
increased.
The system proposed in this project is being developed for the purpose of solving some of those
concerns and to make the task of turning free text medical leaflets into structured data. The system
consists of multiple modules. Firstly, sectioning and labeling where leaflets are divided into sections, and labels are assigned to them. Secondly, Named Entity Recognition to extract entities from
each section. Then, Relation Extraction, where entities are connected together to form relations.
Finally, Dawa’yTech application that makes the extracted information usable for target users such
as patients. The provided data then can be used for many tasks such as answering the user complex
queries that search engines are incapable of.

## Technologies
This project uses APIs such as UMLS and CRF deep learning

## Setup
To Use the package:
```
$pip install requirements.txt
$cd extraction
$pip install .
```

Go into the file you want to add the package to, then:
```
$import extraction
```
