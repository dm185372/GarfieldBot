# GarfieldBot

![Build Status](https://github.com/dm185372/GarfieldBot/actions/workflows/build.yml/badge.svg)
![Deploy Status](https://github.com/dm185372/GarfieldBot/actions/workflows/deploy.yml/badge.svg)

Ever need a boost in morale? Fear no more! Every day at 9 AM EST this bot will deploy a randomly selected garfield gif to lift your spirits!

## To add GarfieldBot to your server:
1. Click [here](https://discord.com/api/oauth2/authorize?client_id=934093638466699266&permissions=515396590656&scope=bot) to add Garfield to Discord
2. Clone this repo and apply the terraform code (you will need an AWS account, but fortunately it is all serverless so it falls under free tier.)
   You will need to modify the values of "bucket_name" (to your own s3 bucket name), "profile" (to the name of your aws profile in your creds file), 
   and "region" (if you want a different AWS region) in [this](https://github.com/dm185372/GarfieldBot/blob/main/terraform/main.tf) file.
3. Profit!

<br>

![Garfield](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpKnxKTVTkcKWuew1RH_Pco2AZvLW8Eo0XgQ&usqp=CAU)