# Food habits

This project is part of the [EPFL](http://epfl.ch)'s [Applied Data Analysis course](http://ada.epfl.ch) and promotes Data Science in Switzerland. The concept is not spatialy restricted and can be easily generalized elsewhere.

## Abstract

Switzerland is well known for its rich heritage: incredible landscapes, watches, four official national languages (german, french, italian and romansh), cheese, chocolate and diversified influences from its five neighboring countries. This project investigate how this heritage is reflected in food habits through the whole country. Thanks to the high restaurant density we suggest insights about the following topics:
- food impacts on health conditions (e.g. size, weight)
- food trends according to clichés (e.g. Rösti, Malakoff)
- food variety per locations (e.g. international cities versus local villages) 
- food importance to people's perception (e.g. appreciations)
- food quality (e.g. poor dishes, price) 

## Data description

- restaurant menus (e.g. [LaFourchette](https://www.lafourchette.com), restaurant own websites)
- general food classification and insights (e.g. [OpenFoodFacts](http://ch-en.openfoodfacts.org), [OpenFood](https://www.openfood.ch))
- health data (e.g. [Swiss Administration](https://www.bfs.admin.ch/bfs/en/home/statistics/catalogues-databases.html), [Open Health data](http://make.opendata.ch/wiki/data:health))

Additionnal complementary datasets:

- tweets for people opinions about places/foods (e.g. [Twitter](https://twitter.com))
- restaurants comments (e.g. [TripAdvisor](https://fr.tripadvisor.ch))

## Feasibility and risks

- datasets collect : menus data can be difficult to gather
- sparsity and spatial homogeneity : depending on datasets quality some regions might need to be ignored due to lack of data
- content languages : textual informations (including menus) can have different name depending on area, standardization and translation might be needed
- data completeness : non food data might need be extracted from different sources to achieve a valuable meaning

## Deliverables

- replicable pipeline from data to insights (stack not yet known)
- insights graphs (interactive if relevant)

## Timeplan

- [x] november: data gathering
- [ ] first part of december: analysis
- [ ] last part of december: modelling and visualisation

## License

Project is available under [Apache 2.0](./LICENSE) license and data belong their owners under appropriate licensing.
