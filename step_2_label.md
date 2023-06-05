## Second step: labelling

![1-paradigm-shift.PNG](documentation%2Flabelling%2F1-paradigm-shift.PNG)

There are three big paradigm shifts to understand to achieve AI.
![2-paradigm-shift-skills.PNG](documentation%2Flabelling%2F2-paradigm-shift-skills.PNG)

The first is that we work differently.
In classical computer science, we are given rules and some input data with that a developer codes an algorithm that allows us to retrieve the answers.

In Machine Learning, we need input data + answers. From as little as 100, to thousands or even millions of examples. The objective is to learn, grasp some patterns from the data to be able to predict answers from data the model never saw before. To do so, developers write code that generates what we call a model. In computer terms we speak of an AI model that we execute (infere).

![3-paradigm-shift-skills.PNG](documentation%2Flabelling%2F3-paradigm-shift-skills.PNG)

In production it works the same. We receive from a data we execute the algorithm and we get a result.

![4-paradigm-shift-data.PNG](documentation%2Flabelling%2F4-paradigm-shift-data.PNG)

Data is as precious as gold for companies.
Before we talked about a centered AI model because we were not sure we could make the AI models associated with the problems.
Today for most companies this is no longer a problem. we know that we will be able to realize AI.
What makes the difference that we will be able to carry out a project or not is the data.
- the quantity
- the quality of inputs and responses.

![5-paradigm-shift-alive.PNG](documentation%2Flabelling%2F5-paradigm-shift-alive.PNG)

Data: it is alive, it is alive in the sense that the world moves, evolves, data evolves.
Look at this brand new french identity card.
As humans we know how to read it and adapt quickly even if we have never seen it before, but an AI model trained to read an older version of the french identity card is unable to adapt as easily as we do. We will have to teach it, train it to read this new identity card.
Change is permanent, AI training is something that we should do regularly, even on a daily basis in some cases.

![5-paradim-shift-alive.PNG](documentation%2Flabelling%2F5-paradim-shift-alive.PNG)
In a complex workflow where several AI algorithms are chained, or the output of the previous algorithm influences the input of the next.
It must be understood that, for example, if we have a total of 8 steps involving 8 AI models that chains together, if each stage must be trained with 10,000 entries and 10,000 outputs.

You'll need about 80,000 annotations each time you want to retrain your AIs with new data.

The annotation phase is an important step that must be carried out industrially.

### Labelling
In this step we will learn about importance of data quality and labelling process.

Important points :
- Data/Response and quality is the key for generating good ML algorithm
- If data and response are correct at 80% rate, your ML model cannot perform better than 80%
- Labelling instructions are build with the entire team and must resolve, add new sample of edge cases when you encounter an example
  - Start with small amount of data to affine labelling rules
- Data labelling is expensive, if you can accelerate labelling with an automated pre-labelling phase, do it.
- Feeback loop is a good way to have pre-label set up
- Data/Reponse must always be verified by human

How do you classify the image bellow ?

![labelling_rules.png](documentation%2Flabelling%2Flabelling_rules.png)

How do you classify the image bellow ?

![labelling_rules-1.png](documentation%2Flabelling%2Flabelling_rules-1.png)

We will label cats-dogs-other dataset together using ecotag:

https://axaguildev-ecotag.azurewebsites.net

Ecotag is an Open Source tool available here : 

https://github.com/AxaGuilDEv/react-oidc

![Ecotag.png](documentation%2FEcotag.png)

### Data drift

You will encounter a lot of kind of drift.
Monitoring data drift is mandatory to go to production.

- Example quality control, change bulb in production.
