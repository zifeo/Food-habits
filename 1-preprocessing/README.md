# 1 Preprocessing

Before we used the data for our project we had to first preprocess it so that it was usable as we wanted to.
For each of the websites we scrapped we had to do a different process to get the data we wanted out of the text.

## Restaurants

From each restaurant we had to extract the meals they were offering and to integrate them in a Pandas dataFrame. 
As we had only one restaurant website, we used the internal hierachy of the webpage as a template for our dataFrame.

## Recipes

This was the most difficult part as we had so many websites. Therefore we choose this simple representation for a recipe :

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

We got a Postgres dump from OpenFood with a lot of information on products sold in Switzerland (Migros and Coop). 
We transformed this data in a Pandas dataFrame to be able to manipulate it better later on.
