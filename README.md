# backend

<h2>API Endpoints</h2>

<h3>/nutri/fooditem/</h3>

<h4>POST</h4>

```javascript
// Request
{
    "name": "oatmeal",
    "protein": 9,
    "fat": 12,
    "carb":36
}

// Response
{
    "fooditem": {
        "id": 4,
        "name": "oatmeal",
        "protein": 9,
        "carb": 36,
        "fat": 12,
        "user": 1
    }
}

```

<h3>/nutri/meal/</h3>

<h4>POST</h4>

```javascript
// Request
{
    "fooditems": [1, 2, 3],
    "name": "smoothie"
}

// Response
{
    "meal": {
        "id": 5,
        "name": "smoothie",
        "protein": 21,
        "carb": 52,
        "fat": 7,
        "user": null,
        "fooditems": [
            1,
            2,
            3
        ]
    }
}
```

or, alternatively supply macronutrients and no FoodItem IDs

```javascript
// Request
{
    "name": "meal without food items",
    "protein": 10,
    "fat": 20,
    "carb": 30
}

// Response
{
    "meal": {
        "id": 6,
        "name": "meal without food items",
        "protein": 10,
        "carb": 30,
        "fat": 20,
        "user": 1,
        "fooditems": []
    }
}
```
