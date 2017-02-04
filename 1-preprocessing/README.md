# 1 Preprocessing

Before we used the data for our project we had to first preprocess it so that it was usable as we wanted to.
For each of the websites we scrapped we had to do a different process to get the data we wanted out of the text.

## Restaurants

We had to extract from each restaurant the meals they were prposing and integrated it in a Pandas dataFrame. 
As we had only one restaurant it we used the internal hierachy of the webpage as a template for our dataFrame.

## Recipes

This was the most difficult part as we had so many websites. Therefore we choose a simple representation of a recipe :

```
recipe: {
    name: "",
    ingredients: [
        {
            {
              "content": "",
              "quantity": 1,
              "unit": "g"
            },
            ...
        }
    ],
}
```

We extracted all we could from the different scraps in this form so that we could use them in the same way and aggregate them together.


## Products

We got a postgres dump from OpenFood with a lot of information on products sold in switzerland (Migros and Coop). 
We transformed this data in a pandas dataframe to be able to manipulate it better later on.