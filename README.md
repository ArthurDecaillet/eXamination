# eXamination

This is the eXamination project created during the 3rd year of apprentiship in the EPTM as a training for the TPI.

## Why was it made?

It's a mandatory project for the 3rd year of the EPTM in Valais, the project's subject was decide by the teachers and the students needed to make it and developp as much as they wanted.
This project was the one I was given to do. So there it is.

## To Launch

This project needs a Mongo database on the 10.205.201.100:17027 IP to work properly.
>To start the MongoDB docker


`docker compose start`

Then you need to create some Collections (Question,Examen,Examen_eleve,Subject) => it is in french because the interfaces needed to be in this language

>To turn off the docker


`docker compose stop`

You also need to download two libraries for python, pymongo and pyqt5.


>To download the libraries in a terminal


`pip install pymongo pyqt5`

Then, The socket server can be started but it needs the ORM and the Student file in the same folder to work.

This part represent the student computer that receives an exam and then needs to complete it and send it back the the teacher present in the same network.

Finally, for the Teacher, you need to start the UI file and do what you want, once you create an exam, it is automatically sent to all the students in the network.

## Important things to know

This project is not by any means secured, this was not the purpose of this, so be careful while using this project.

Everything can be copied but not used for any lucrative means.
