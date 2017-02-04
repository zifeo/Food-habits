# Food habits

This project is part of the [EPFL](http://epfl.ch)'s [Applied Data Analysis course](http://ada.epfl.ch) and promotes Data Science in Switzerland. The concept is not spatialy restricted and can be easily generalized elsewhere.

## Abstract

Switzerland is well know for its rich heritage: incredible landscapes, watches, cheese, chocolate and diversified influences from its five neighboring countries. This project investigates how this heritage is reflected in terms of food habits.
We picked 2 Swiss and 3 French cities with high restaurant density to get insights about dietetics. We mapped restaurant meals to recipes and ingredients of recipes to products to analyze the corresponding nutriments. 

_**Is there any area-based nutrition bias ?**_

Our infrastructure and datasets also allow us to explore other topics such as:

- food trends according to clichés (e.g. Rösti, Malakoff)
- food/nutriments variety per locations (e.g. meals with more salt/lipids/etc..) 

## Data description

- 11k restaurants (e.g. [LaFourchette](https://www.lafourchette.com))
- 35k meals (extracted from the restaurants' menus)
- 170k recipes (various websites, e.g. [CuisineAZ](http://cuisineaz.com))
- 1.3M ingredients (derived from the recipes)
- 5k products (e.g. [FDDB](http://fddb.info), [OpenFood](https://www.openfood.ch))
- 40k nutriments (extracted from the products)

## Assumptions

We assumed that:

- the restaurants listed in LaFourchette were representative enough of the local food habits.
- we could associate recipes to meals and products to recipes well enough to derive the nutritious facts for a meal without suffering too much of variance and central limit theorem.

## Data pipeline 

We implemented the following data pipeline:

![Visualization of the data pipeline](images/pipeline.png)

## Matching

We used this process to find matches:

![Visualization of the matching system](images/matching.png)

#### Types of matching

| Disadvantage | Advantage |
|:---:|:---:|
| **Rare events, misspelled, grouped**<br />Pavé de boeuf aux morilles<br />_Pavé de boeuf aux morilles_ simplissimes   |   **Order tolerance**<br />Tiramisu caramel speculos beurre salé<br />_Tiramisu au caramel_ au _beurre salé_  et _spéculoos_    |
| **Wide, personal meaning**<br />café gourmand<br />_café gourmand_ à ma façon     | **Exact match**<br />Salade d'orange au miel et à la cannelle<br />_Salade d'orange au miel et à la cannelle_   |
| **Principal component**<br />Rognons de lapins à la moutarde de Meaux<br />Fricassée de champignons _à la moutarde de Meaux_    | **Limited difference**<br />Terrine de foie gras et confiture de pruneaux<br />_Terrine de foie gras_ aux _pruneaux_ et raisins secs    |
| **Unknown, language**<br />Tartare de boeuf minute, salade et potatoes<br />Twice baked _potatoes_ au bacon | **Complex**<br />Cassolette de Saint-Jacques et crevettes<br />Ravioles, noix _de Saint-Jacques_ et _crevettes_ en _cassolettes_ raffinées    |

## Food trends

A few examples of food facts we can extract from the datasets with our infrastructure.

| Per country | Per city |
|:-------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------:|
| ![Energy trend per country](images/energy_country.png)<br />Energy(kCal) per country  | ![Energy trend per city](images/energy_city.png)<br />Energy(kCal) per city   |
| ![Protein trend per country](images/protein_country.png)<br />Protein per country     | ![Protein trend per city](images/protein_city.png)<br />Protein per city      |
| ![carbs trend per country](images/carbs_country.png)<br />Carbohydrates per country   | ![Carbs trend per city](images/carbs_city.png)<br />Carbohydrates per city    |
| ![Salt trend per country](images/salt_country.png)<br />Salt per country              | ![Salt trend per city](images/salt_city.png)<br />Salt per city               |

## Visualization

Here are a few visualization examples for cliché-meal searches.

| Speciality | Different kind |
|:-------------------------------------------------:|:-------------------------------------------------:|
| ![First visualization example](images/map1.png)   | ![Second visualization example](images/map2.png)  |
| [Choucroute](https://en.wikipedia.org/wiki/Choucroute_garnie) (red), [Malakoff](https://en.wikipedia.org/wiki/Malakoff_(food)) (blue) | [Fondue Savoyarde](https://en.wikipedia.org/wiki/Fondue) (red), [Fondue au fromage](https://en.wikipedia.org/wiki/Fondue#French_alpine) (blue) |

## Results

Expected food trends were present as one could expect from well-known clichés. Looking closer at the estimated nutritious facts, the high variance and noisiness of the datasets coupled to the matching process increases greatly the difficutly of our analysis.
No relevant area-based nutrition bias among the insights was found. One could nonetheless use the matching process and the pipeline as tools for further in depth investigation.

## Expected and encountered challenges

Before starting the project, we expected the following points to be the most challenging:

- datasets collection : menus data can be difficult to gather
- sparsity and spatial homogeneity : depending on datasets quality some regions might need to be ignored due to lack of data
- content languages : textual informations (including menus) can have different name depending on area, standardization and translation might be needed
- data completeness : non food data might need be extracted from different sources to achieve a valuable meaning

After finishing the project, the challenges actually were the following ones:

- data mining and normalization (high variance, different sources, captchas)
- data organization (complex queries, centralized storage with ElasticSearch)
- french NLP (weird characters, hard modeling)
- matching (many candidates, heterogeneous units)
- computationally heavy (vectorization, visualization)

Regarding the content languages, no data was available for the German and Italian part of Switzerland on LaFourchette. Hence we focused our work on France and the French part of Switzerland.

## Improvements

- formal statistical evaluation: as limited in time, the project does not contain a lot of insights. This could be definetly enhanced to increase modelling and evaluation.
- deep recurrent neural network for matching: one should evalute the effiency of neural net to match meal to recipes.
- computational efficiency: currently the matching lasts 20 seconds per restaurant (centralized server), this could be improved by batching, parallelisation and local server.
- expand visualization: better interactive and more diverse kind of visuzalization.
- more and enhanced data for Switzerland: data precision is still an issue. This could have been improved by using personal restaurant websites for example. 

## License

Project is available under [Apache 2.0](./LICENSE) license and data belong to their owners under appropriate licensing.
