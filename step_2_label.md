## Second step: labelling

![1-paradigm-shift.PNG](documentation%2Flabelling%2F1-paradigm-shift.PNG)

Il y a trois gros changement de paradigmen a comprendre pour réaliser des IA.
![2-paradigm-shift-skills.PNG](documentation%2Flabelling%2F2-paradigm-shift-skills.PNG)

La premier c'est que l'on travaille différament.
En informatique classique, on nous donne des règles et quelque données d'entrée avec cela un développeur on code un algortihme qui permet de récupérer les réponses.
En Machine Learning, il nous faut de la données d'entrées + des réponses. Par qu'un peu des 100 ène, des milliers voires des millions d'exemple. AVec cela un développeur écrit du code qui permet de générer les règles, ce que l'on appel une IA. EN terme informatique on parle de modèle IA que l'on exécute (infére).

![3-paradigm-shift-skills.PNG](documentation%2Flabelling%2F3-paradigm-shift-skills.PNG)

En production cela fonctionne pareil. On reçoit de a data on exécute les alrgorithme et on obtien un resultat.


![4-paradigm-shift-data.PNG](documentation%2Flabelling%2F4-paradigm-shift-data.PNG)

La data c'est de l'or pour les entreprises.
Avant on parlais de modèle IA centrique car on n'était pas sûr de pouvoir réaliser les modèles IA associé aux problématiques.
Aujourd'hui pour la plupart des entreprise ce n'est plus un problème. on sais que l'on va pouvoir réaliser l'IA.
Ce qui fait la différence que 'on va pouvoire réaliser un projet ou pas c'est la données.
- la quantité
- la qualité des entrées et de réponses.

![5-paradigm-shift-alive.PNG](documentation%2Flabelling%2F5-paradigm-shift-alive.PNG)

La données: c'est vivant, c'est vivant dans le sens ou le monde bouge, évolue, la données évolue.
Vous connaissez cette nouvelle carte d'identité ?
Nous on sais la lire et s'adapter rapidement même si on ne la jamais vu, mais une IA non, il va falloir l'éduquer, l'entrainer a lire cette carte d'identitée.
Le changement c'est permanant, l'entrainement des IA est quelque chose qui es quotidient qui doit continuer jour apres jour.

![5-paradim-shift-alive.PNG](documentation%2Flabelling%2F5-paradim-shift-alive.PNG)
Dans un workflow complexe ou l'on chaîne plusieurs algorithmes IA, ou la sortie de l'algorithme précédent influe sur l'entrée du suivant.
Il faut comprende que si on n'a au total par exemple 8 étapes avec 8 IA qui s'enchaine.
Si chaque étape doit être entrainer avec 10 000 entrées et 10 000 sorties.

il vous faudra environ 80 000 annotations a chaque fois que vous voulez réentrainer vos IA avec de nouvelles données.

La phase d'annotation est une étape important qui doit être réaliser de manière industriel.

### Labelling
In this step we will learn about importance of data quality and labelling process.

Important points :
- Data/Response and quality is the key for generating good ML algorithm
- If data and response are correct at 80% rate, your ML model cannot perform better than 80%
- Labelling instructions are build with the entire team and must resolve, add new sample of edge cases when you encounter an example
  - Start with small amount of data to affine labelling rules
- Data labelling cost a lot, if you can accelerate labelling with automatic pre-labelling phase, do it.
- Feeback loop is a good way to have pre-label set up
- Data/Reponse must always be verified by human

How do you label the zoning of this image ?

//TODO add image

How to you re-transcribe this sound ?

//TODO add sound

We will label cats-dogs-other dataset together using ecotag:

https://axaguildev-ecotag.azurewebsites.net

Ecotag is an Open Source tool avalable here : 

https://github.com/AxaGuilDEv/react-oidc

![Ecotag.png](documentation%2FEcotag.png)
### Data drift

You will encounter a lot of kind of drift.
Monitoring data drift is mandatory to go to production.

- Exemple controle qualité, changement ampoule en production. 
