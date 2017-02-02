# Food habits

This project is part of the [EPFL](http://epfl.ch)'s [Applied Data Analysis course](http://ada.epfl.ch) and promotes Data Science in Switzerland. The concept is not spatialy restricted and can be easily generalized elsewhere.

## Abstract
Switzerland is well know for its rich heritage: incredible landscapes, watches, cheese, chocolate and diversified influences from its five neighboring countries. This project investigates how this heritage is reflected in terms of food habits.
Thanks to the high restaurant density, we picked 2 Swiss and 3 French cities to get insights about dietetics. We mapped restaurant meals to recipes and ingredients of recipes to products to analyze corresponding nutriments. 
_Is any area-based nutrition bias ?_
Our infrastructure and datasets also allow us to explore other topics such as:

- food trends according to clichés (e.g. Rösti, Malakoff)
- food/nutriments variety per locations (e.g. meals with more salt/lipids/etc..) 


## Data description

- 11k restaurants (e.g. [LaFourchette](https://www.lafourchette.com))
- 35k meals (extracted from the restaurants' menus)
- 170k recipes (various websites, e.g [cuisineAZ](http://cuisineaz.com))
- 5k products (e.g. [FDDB](http://fddb.info), [OpenFood](https://www.openfood.ch))
- 40k nutriments (extracted from the products)

## Data pipeline 

![Visualization of the data pipeline](images/pipeline.png)

## Matching

![Visualization of the matching system](images/matching.png)

## Food trends

|                                                           |                                                    |
|:---------------------------------------------------------:|:--------------------------------------------------:|
|               Energy(kCal) per country                    |               Energy(kCal) per city                |
| ![Energy trend per country](images/energy_country.png)    | ![Energy trend per city](images/energy_city.png)   |
|               Protein per country                         |               Protein per city                     |
| ![Protein trend per country](images/protein_country.png)  | ![Protein trend per city](images/protein_city.png) |
|               Carbohydrates per country                   |               Carbohydrates per city               |
| ![carbs trend per country](images/carbs_country.png)      | ![Carbs trend per city](images/carbs_city.png)     |
|               Salt per country                            |               Salt per city                        |
| ![Salt trend per country](images/salt_country.png)        | ![Salt trend per city](images/salt_city.png)       |

## Visualization

Here are a few visualization examples for cliché-meal searches:

|     |     |
|:---:|:---:|
| ![First visualization example](images/map1.png)  | ![Second visualization example](images/map2.png) |
| Choucroute (red), Malakoff (blue)    |  Fondue Savoyarde (red), Fondue au fromage (blue)   |

## Results

Expected food trends were present as one could expect from well-known clichés. Looking closer at the estimated nutritious facts, the high variance and noisiness of the datasets coupled to matching process increases the difficutly of the analysis.
No relevant area-based nutrition bias among the insights was found. One could nonetheless use the matching process and the pipeline as tools for further investigation.

## Expected and encountered challenges
Before starting the project, we expected the following points to be the most challenging:

- datasets collection : menus data can be difficult to gather
- sparsity and spatial homogeneity : depending on datasets quality some regions might need to be ignored due to lack of data
- content languages : textual informations (including menus) can have different name depending on area, standardization and translation might be needed
- data completeness : non food data might need be extracted from different sources to achieve a valuable meaning

After finishing the projects, the challenges actually were the following ones:

- Data mining and normalization (high variance, different sources, captchas)
- Data organization (complex queries, centralized storage with ElasticSearch)
- French NLP (weird characters, hard modeling)
- Matching (many candidates, heterogeneous units)
- Computationally heavy (vectorization, visualization)

Regarding the content languages, no data was available for the German and Italian part of Switzerland on LaFourchette. Therefore we focused our work on France and the French part of Switzerland.

## Improvements

- Formal statistical evaluation
- Deep recurrent model for matching
- Computational efficiency
- Expand visualization
- More and enhanced data for Switzerland

## License

Project is available under [Apache 2.0](./LICENSE) license and data belong their owners under appropriate licensing.
