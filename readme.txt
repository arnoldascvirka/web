##################################

Arnoldas Cvirka 2022-10-11

WEB Projektas su Flask

##################################

• Projektas įjungiamas su app.py

• Projektas gali įrašyti users ir posts.
• Slaptažodžiai hashinami in sql.
• Galima pakeisti profilio nuotrauka, default yra static/profile_pics/default.jpg
• Sukūrus posta, ant jo paspaudus su tinkamu useriu, galima ištrinti arba updatinti savo posta.
• Paspaudus ant userio, galima matyti visus jo postus.
• Runninamas SMTP client (Galima matyti config.py faile), su juo siunciami password reset emailai, su generated fitting user tokens.
• Routes suskirstyti į atitinkamus folderius, aka, visi user routes kaip login ir register bus in users folder.




Jei bus erroras dėl itsdangerous, irasyti galima per:
    pip install git+https://github.com/puiterwijk/flask-oidc.git@b10e6bf881a3fe0c3972e4093648f2b77f32a97c

Tai dėl to kad itsdangerous yra deprecated library.
