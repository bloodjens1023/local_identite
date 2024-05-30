import os
from dotenv import load_dotenv

import datetime
import math
from django.http import HttpResponse, JsonResponse
from backend.lib.Email import envoie_email
from backend.models import *
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password,make_password
from django.core.serializers import serialize
from vonage import vonage
from twilio.rest import Client
import requests


def get_document(request, user):
    try:
        users = Utilisateur.objects.get(identifiant = user )
        docs = Document.objects.filter(utilisateur=users)
    except:
        return JsonResponse({'donne':False})
    nombre = 0
    for doc in docs:
        nombre+=1


    for doc in docs:

        return JsonResponse({'nom':doc.nom,
                             'prenom':doc.prenom,
                             'adresse':doc.adresse,
                             'numCni': doc.numCni,
                             'photo':str(doc.photo),
                             'declarationPerte':str(doc.declarationPerte),
                             'certificat':str(doc.certificat),
                             'acteNaissance':str(doc.acteNaissance),
                             'typeDocument':doc.typeDocument,
                             'etatDocument': doc.etatDocument,
                             'dateDebut': doc.dateDebut,
                             'archiver':doc.archiver,

                             })

    else:
        return JsonResponse({'donne':'aucun'})




def get_user(request, user):
    try:
        users = Utilisateur.objects.get(identifiant = user )
    except:
        return JsonResponse({'donne':False})

    if users is not None :
        return JsonResponse({'identifiant':users.identifiant,
                             'email':users.email,
                             'tel':users.tel,
                             'password': users.password,
                             'photo':str(users.photo),
                             'role':str(users.role)
                             })
    else:
        return JsonResponse({'donne':'aucun'})





def get_arrondissement(request):
    try:
        arrondissements = Arrondissement.objects.all().order_by("district")
        data = []

        for arrondissement in arrondissements:
            if(arrondissement.nom != "tous"):
                data.append({'id':arrondissement.id,'nom':arrondissement.nom, 'code':arrondissement.code,'district':arrondissement.district.nom,'district_id':arrondissement.district.id})



        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})







def get_utilisateur_tout(request):
    try:
        user = Utilisateur.objects.all()
        data = []

        for use in user:
            if(use.identifiant != "admin"):
                data.append({'identifiant':use.identifiant, 'email':use.email, 'tel':use.tel})

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})







def get_chef_tout(request):
    try:
        user = Chef.objects.all()
        data = []

        for use in user:

           data.append({'nom':use.nom,'prenom':use.prenom, 'email':use.email, 'tel':use.tel,'cni':use.numCni, 'dirige':use.arrondissementChef.nom,'district':use.arrondissementChef.district.nom,'region':use.arrondissementChef.district.region.nom})

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})








def get_arrondissement_chef(request):
    try:
        arrondissements = Arrondissement.objects.filter(diriger="non")
        data = []

        for arrondissement in arrondissements:

            if(arrondissement.nom != "tous"):
                data.append({'id':arrondissement.id,'nom':arrondissement.nom})



        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def get_chef(request,user):
    try:
        user = Chef.objects.filter(email = user)
        data = []

        for use in user:

           data.append({'nom':use.nom,'prenom':use.prenom, 'email':use.email, 'tel':use.tel,'cni':use.numCni, 'dirige':use.arrondissementChef.nom, "photo":str(use.photo), "password":use.password})

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})

def delete_document(request, user):
    try:

        users = Utilisateur.objects.get(identifiant = user )
    except:
        return JsonResponse({'donne':False})

    doc = Document.objects.get(utilisateur=users)
    doc.delete()
    return JsonResponse({'donne':'supprimer avec succès'})

def delete_arrondissements(request, user):

    doc = Arrondissement.objects.get(id=user)
    doc.delete()
    return JsonResponse({'donne':'supprimer avec succès'})

def delete_region(request, user):

    doc = Region.objects.get(id=user)
    doc.delete()
    return JsonResponse({'donne':'supprimer avec succès'})

def delete_district(request, user):

    doc = District.objects.get(id=user)
    doc.delete()
    return JsonResponse({'donne':'supprimer avec succès'})


@api_view(["POST"])
def update_arrondissements(request, user):
    district = District.objects.get(id= request.POST.get('district'))
    doc = Arrondissement.objects.get(id=user)
    doc.nom = request.POST.get('nom')
    doc.code = request.POST.get('code')
    doc.district = district
    doc.save()
    return JsonResponse({'message': True,'donne':'supprimer avec succès'})

@api_view(["POST"])
def update_regions(request, user):

    doc = Region.objects.get(id=user)
    doc.nom = request.POST.get('nom')
    doc.code = request.POST.get('code')
    doc.save()
    return JsonResponse({'message': True,'donne':'supprimer avec succès'})

@api_view(["POST"])
def update_district(request, user):
    region = Region.objects.get(id=request.POST.get('region'))
    doc = District.objects.get(id=user)
    doc.nom = request.POST.get('nom')
    doc.code = request.POST.get('code')
    doc.region = region
    doc.save()
    return JsonResponse({'message': True,'donne':'supprimer avec succès'})

def delete_utilisateur(request, user):
    try:

        users = Utilisateur.objects.get(identifiant = user )
    except:
        return JsonResponse({'donne':False})

    users.delete()
    return JsonResponse({'donne':'supprimer avec succès'})

def delete_chef(request, user):
    try:
        chef = Chef.objects.get(email = user)
        arrond = Arrondissement.objects.get(id = chef.arrondissementChef.id)

        arrond.diriger = "non"
        arrond.save()
    except:
        return JsonResponse({'donne':False})

    chef.delete()
    return JsonResponse({'donne':'supprimer avec succès'})





@api_view(['POST'])
def update_document(request, user):
    try:
        users = Utilisateur.objects.get(identifiant = user )
        doc = Document.objects.get(utilisateur=users)


        if request.POST.get('type') == "primata":

            doc.nom = request.POST.get('nom')
            doc.prenom = request.POST.get('prenom')
            doc.adresse = request.POST.get('adresse')
            doc.numCni = ""
            doc.photo = request.FILES['photo']
            doc.declarationPerte = ""
            doc.certificat = request.FILES['certificat']
            doc.acteNaissance = request.FILES['acteNaissance']
            doc.typeDocument = request.POST.get('type')
            doc.utilisateur = users
            doc.dateDebut = datetime.datetime.now()

            doc.save()
            return JsonResponse({'message': True,'info':"Pas d'erreur"})
        elif request.data["type"] == "duplicatatUse":

            doc.nom = request.POST.get('nom'),
            doc.prenom = request.POST.get('prenom')
            doc.adresse = request.POST.get('adresse')
            doc.numCni = request.POST.get('numCni')
            doc.photo = request.FILES['photo']
            doc.declarationPerte = ""
            doc.certificat = request.FILES['certificat']
            doc.typeDocument = request.POST.get('type')
            doc.acteNaissance = ""
            doc.dateDebut = datetime.datetime.now()
            doc.utilisateur = users

            doc.save()
            return JsonResponse({'message': True,'info':"Pas d'erreur"})
        elif request.data["type"] == "duplicatatPerte":

            doc.nom = request.POST.get('nom')
            doc.prenom = request.POST.get('prenom')
            doc.adresse = request.POST.get('adresse')
            doc.numCni = request.POST.get('numCni')
            doc.photo = request.FILES['photo']
            doc.declarationPerte = request.FILES['declarationPerte']
            doc.certificat = request.FILES['certificat']
            doc.typeDocument = request.POST.get('type')
            doc.acteNaissance = ""
            doc.dateDebut = datetime.datetime.now()
            doc.utilisateur = users
            doc.save()
            return JsonResponse({'message': True,'info':"Pas d'erreur"})
        else:
            return JsonResponse({'message': False,'info':"Un erreur s'est survenue"})
    except:
        return JsonResponse({'donne':False})






@api_view(['POST'])
def update_utilisateur(request, user):
    reponse = False

    prefixes = ["033", "034", "038","032"]
    numero = str(request.data["tel"])
    request.user = request.data

    for prefixe in prefixes:

                if numero.startswith(prefixe):
                    reponse =  True
                    break
                else:
                    reponse = False
    if reponse:
                try:
                    users = Utilisateur.objects.get(identifiant = user )

                    if(request.POST.get('photo') != ""):
                        users.photo = request.FILES['photo']
                    users.tel = request.POST.get('tel')
                    users.email = request.POST.get('email')
                    if(request.POST.get('password') != ""):
                        users.password = make_password(request.POST.get('password'))
                    users.save()
                    return JsonResponse({'message': True,'info':"Pas d'erreur"})
                except:

                    return JsonResponse({'message':False,'info':"Un erreur s'est survenue"})

    else:
                return JsonResponse({'message': False,'info':"Numero pas pris en charge"})


@api_view(['POST'])
def update_chef(request, user):
    reponse = False

    prefixes = ["033", "034", "038","032"]
    numero = str(request.data["tel"])
    request.user = request.data

    for prefixe in prefixes:

                if numero.startswith(prefixe):
                    reponse =  True
                    break
                else:
                    reponse = False
    if reponse:
                try:
                    users = Chef.objects.get(email = user )

                    if(request.POST.get('photo') != ""):
                        users.photo = request.FILES['photo']
                    users.nom = request.POST.get('nom')
                    users.prenom = request.POST.get('prenom')
                    users.numCni = request.POST.get('cni')
                    users.tel = request.POST.get('tel')
                    users.email = request.POST.get('email')
                    if(request.POST.get('password') != ""):
                        users.password = make_password(request.POST.get('password'))
                    users.save()
                    return JsonResponse({'message': True,'info':"Pas d'erreur"})
                except:

                    return JsonResponse({'message':False,'info':"Un erreur s'est survenue"})

    else:
                return JsonResponse({'message': False,'info':"Numero pas pris en charge"})



def index(request):
    return HttpResponse("hello world {}")



@api_view(['POST'])
def connexion(request):
    try:
        user = Utilisateur.objects.get(identifiant = request.data["identifiant"])
    except:
        return JsonResponse({'message': False,'info':'Utilisateur non identifier'})
    if check_password(request.data["password"],user.password):
        return JsonResponse({'message': True,'info':'Connexion réussite'})
    else:
        return JsonResponse({'message': False,'info':'Erreur connéxion'})


@api_view(['POST'])
def insertion_verif(request):
    try:
        verif = Verif.objects.get()
        verif.contenu = request.data["code"]
        verif.save()
        return JsonResponse({'message': True,'info':'Connexion réussite'})
    except:
        verif = Verif(contenu = request.data["code"])
        verif.save()
        return JsonResponse({'message': True,'info':'Connexion réussite'})


def get_verif(request):
    try:
        verif = Verif.objects.all()
        data = []

        for verifs in verif:

            data.append({'code':verifs.contenu})

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})






@api_view(['POST'])
def inscription(request):
    try:
        if(str(request.data["identifiant"]).isspace() or str(request.data["identifiant"]).isidentifier() == False):
            return JsonResponse({'message': False,'info':"Erreur de l'identifiant"})

        if(str(request.data["email"]).__contains__("@gmail.com") == False):
             return JsonResponse({'message': False,'info':"Erreur de l'email"})

        if(len(request.data["password"])<12):
            return JsonResponse({'message': False,'info':"Mots de passe trops faible"})
        elif(str(request.data["password"]).isspace()):
            return JsonResponse({'message': False,'info':"Mots de passe impossible"})

        reponse = False
        arrond = Arrondissement.objects.get(id = request.data["arrond"])
        prefixes = ["033", "034", "038","032"]
        numero = str(request.data["tel"])
        request.user = request.data
        if not Utilisateur.objects.filter(email = request.data["email"]).exists():
            if not Utilisateur.objects.filter(identifiant = request.data["identifiant"]).exists():
                for prefixe in prefixes:

                    if numero.startswith(prefixe):
                        reponse =  True
                        break
                    else:
                        reponse = False
                if reponse:
                    serializer = Utilisateur(identifiant = request.data["identifiant"], email = request.data["email"], tel = request.data["tel"],  password = request.data["password"],arrondissement = arrond)
                    test = serializer.set_mot_de_passe(serializer.password)
                    serializer.save()
                    return JsonResponse({'message': True,'info':"Un erreur s'est survenue"})
                else:
                    return JsonResponse({'message': False,'info':"Numero pas pris en charge"})
            else:
                return JsonResponse({'message': False,'info':'Identifiant déja prise'})
        else:
            return JsonResponse({'message': False,'info':'email déja utilisée'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de remplissage de donnée"})

@api_view(['POST'])
def envoieDemande(request):
    user = Utilisateur.objects.get(identifiant = request.POST.get("identifiant"))

    if(str(request.POST.get('nom')).isspace() or str(request.POST.get('prenom')).isspace() or str(request.POST.get('adresse')).isspace()):
        return JsonResponse({'message': False,'info':"Erreur de l'identifiant"})



    if request.POST.get('type') == "primata":
        serializer = Document(nom = request.POST.get('nom'),
                               prenom = request.POST.get('prenom'),
                               adresse = request.POST.get('adresse'),
                               sexe = request.POST.get('genre'),
                               numCni = "",
                               photo = request.FILES['photo'],
                               declarationPerte = "",
                               certificat = request.FILES['certificat'],
                               acteNaissance = request.FILES['acteNaissance'],
                               typeDocument = request.POST.get('type'),
                               utilisateur = user)
        print(request.data['photo'])
        serializer.save()
        return JsonResponse({'message': True,'info':"Pas d'erreur"})
    elif request.data["type"] == "duplicatatUse":
        serializer = Document(nom = request.POST.get('nom'),
                               prenom = request.POST.get('prenom'),
                               adresse = request.POST.get('adresse'),
                               sexe = request.POST.get('genre'),
                               numCni = request.POST.get('numCni'),
                               photo = request.FILES['photo'],
                               declarationPerte = "",
                               certificat = request.FILES['certificat'],
                               typeDocument = request.POST.get('type'),
                               acteNaissance = "",
                               utilisateur = user)
        print(request.data['photo'])
        serializer.save()
        return JsonResponse({'message': True,'info':"Pas d'erreur"})
    elif request.data["type"] == "duplicatatPerte":
        serializer = Document(nom = request.POST.get('nom'),
                               prenom = request.POST.get('prenom'),
                               adresse = request.POST.get('adresse'),
                               sexe = request.POST.get('genre'),
                               numCni = request.POST.get('numCni'),
                               photo = request.FILES['photo'],
                               declarationPerte = request.FILES['declarationPerte'],
                               certificat = request.FILES['certificat'],
                               acteNaissance = "",
                               typeDocument = request.POST.get('type'),
                               utilisateur = user)
        print(request.data['photo'])
        serializer.save()
        return JsonResponse({'message': True,'info':"Pas d'erreur"})
    else:
        return JsonResponse({'message': False,'info':"Un erreur s'est survenue"})



@api_view(['POST'])
def inscription_chef(request):
    try:
        if(str(request.data["nom"]).isspace() or
           str(request.data["prenom"]).isspace() == ""
            or str(request.data["numCni"]).isspace() == ""):
             return JsonResponse({'message': False,'info':"Erreur de replissage du formulaire"})


        if(len(request.data["password"])<12):
            return JsonResponse({'message': False,'info':"Mots de passe trops faible"})
        elif(str(request.data["password"]).isspace()):
            return JsonResponse({'message': False,'info':"Mots de passe impossible"})


        reponse = False
        arrond = Arrondissement.objects.get(id = request.data["arrond"])
        arrond.diriger = "oui"
        arrond.save()
        prefixes = ["033", "034", "038","032"]
        numero = str(request.data["tel"])
        request.user = request.data
        if not Chef.objects.filter(email = request.data["email"]).exists():

                for prefixe in prefixes:

                    if numero.startswith(prefixe):
                        reponse =  True
                        break
                    else:
                        reponse = False
                if reponse:
                    serializer = Chef(nom = request.data["nom"],
                                    prenom = request.data["prenom"],
                                    email = request.data["email"],
                                    numCni = request.data["numCni"],
                                    tel = request.data["tel"],
                                    password = request.data["password"],

                                    arrondissementChef = arrond)
                    serializer.set_mot_de_passe(serializer.password)
                    serializer.save()
                    return JsonResponse({'message': True,'info':"Un erreur s'est survenue"})
                else:
                    return JsonResponse({'message': False,'info':"Numero pas pris en charge"})
        else:
            return JsonResponse({'message': False,'info':'email déja utilisée'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de replissage du formulaire"})


@api_view(['POST'])
def connexion_chef(request):
    try:
        user = Chef.objects.get(email = request.data["email"])
    except:
        return JsonResponse({'message': False,'info':'email non identifier'})
    if check_password(request.data["password"],user.password):
        return JsonResponse({'message': True,'info':'Connexion réussite'})
    else:
        return JsonResponse({'message': False,'info':'Erreur connexion'})


@api_view(["POST"])
def ajout_arrondissement(request):
    try:
        district = District.objects.get(id=request.POST.get('district'))
        arrond = Arrondissement(nom= request.POST.get('nom'),code= request.POST.get('code'),district=district)
        arrond.save()
        return JsonResponse({'message': True,'info':'Arrondissement inserer avec success'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de l'insertion"})


@api_view(["POST"])
def ajout_region(request):
    try:
        arrond = Region(nom= request.POST.get('nom'), code = request.POST.get('code'))
        arrond.save()
        return JsonResponse({'message': True,'info':'Arrondissement inserer avec success'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de l'insertion"})


@api_view(["POST"])
def ajout_district(request):
    try:
        region = Region.objects.get(id=request.POST.get("region"))
        arrond = District(nom= request.POST.get('nom'), code = request.POST.get('code'), region = region)
        arrond.save()
        return JsonResponse({'message': True,'info':'district inserer avec success'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de l'insertion"})

@api_view(["POST"])
def ajout_pub(request):
    try:
        dems = Utilisateur.objects.all()
        for dem in dems:
            notif = Notification(utilisateur = dem,
                                 description = "vous avez reçu une nouvelle actualité de la part de l'administrateur",
                                 lien = "/Utilisateur/Attente",
                                 )
            notif.save()
        if(request.POST.get('photo') == ""):
            pub = Publication(description = request.POST.get("description"))
            pub.save()

            return JsonResponse({'message': True,'info':'publication inserer avec success'})
        else:
            pub = Publication(photo = request.FILES['photo'],description = request.POST.get("description"))
            pub.save()
            return JsonResponse({'message': True,'info':'publication inserer avec success'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de l'insertion de la publication"})

@api_view(["POST"])
def delete_pub(request,id):
    try:
        pub = Publication.objects.filter(id = id)
        pub.delete()
        return JsonResponse({'message': True,'info':'publication inserer avec success'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de l'insertion de la publication"})


def get_pub_tout(request):
    try:
        pub = Publication.objects.all()
        data = []

        for pubs in pub:
            data.append({'id':pubs.id,'photo':str(pubs.photo),'description':pubs.description, 'aimer':pubs.aimer })


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


@api_view(["POST"])
def modif_pub(request,id):
    try:
        pub = Publication.objects.get(id = id)
        if(request.POST.get('photo') == ""):
            pub.description = request.POST.get("description")
            pub.save()
            return JsonResponse({'message': True,'info':'publication inserer avec success'})
        else:
            pub.photo = request.FILES['photo']
            pub.description = request.POST.get("description")
            pub.save()
            return JsonResponse({'message': True,'info':'publication inserer avec success'})
    except:
        return JsonResponse({'message': False,'info':"Erreur de l'insertion de la publication"})


def get_pub_simple(request,id):
    try:
        pub = Publication.objects.filter(id = id)
        data = []

        for pubs in pub:
            data.append({'id':pubs.id,'photo':str(pubs.photo),'description':pubs.description, 'aimer':pubs.aimer })


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})



# Réaction

@api_view(["POST"])
def ajout_reaction(request):
    try:
        user = Utilisateur.objects.get(identifiant = request.POST.get('identifiant'))
        pub = Publication.objects.get(id =request.POST.get('id'))
        reaction = Reaction.objects.get(utilisateur = user, publication=pub)
        if(reaction.liker == False):
            reaction.liker = True
            reaction.save()
            pub.aimer +=1
            pub.save()
            return JsonResponse({'message': True,'info':"creation de pub"})
        else:
            reaction.liker = False
            reaction.save()
            pub.aimer -=1
            pub.save()
            return JsonResponse({'message': True,'info':"creation de pub"})
    except:
        user = Utilisateur.objects.get(identifiant =  request.POST.get('identifiant'))
        pub = Publication.objects.get(id =request.POST.get('id'))
        reaction = Reaction(utilisateur = user, publication=pub, liker = True)
        reaction.save()
        pub.aimer +=1
        pub.save()
        return JsonResponse({'message': True,'info':"creation de pub"})



# COmmentaire

@api_view(["POST"])
def ajout_commentaire(request,id):
    try:
        user = Utilisateur.objects.get(identifiant =  request.POST.get('identifiant'))
        pub = Publication.objects.get(id =id)
        comm = Commentaire(utilisateur = user, publication = pub, contenue= request.POST.get('contenue'))
        comm.save()
        return JsonResponse({'message': True,'info':"creation de pub"})
    except:

        return JsonResponse({'message': True,'info':"creation de pub"})



def get_commentaire_simple(request,ids):
    try:
        pub = Publication.objects.get(id =ids)
        com = Commentaire.objects.filter(publication = pub)
        data = []

        for coms in com:
            data.append({'utilisateur':coms.utilisateur.identifiant,'contenu':coms.contenue ,'photo' : str(coms.utilisateur.photo) })


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


# notification
def get_notification_simple(request,id):
    try:
        user = Utilisateur.objects.get(identifiant = id)
        notification = Notification.objects.filter(utilisateur = user)
        data = []

        for pubs in notification:
            data.append({'id': pubs.id, 'description':pubs.description, 'date': pubs.date, 'lue':pubs.lue, "lien":pubs.lien})


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def get_notification_non_lue(request,id):
    try:
        user = Utilisateur.objects.get(identifiant = id)
        notification = Notification.objects.filter(utilisateur = user,  lue = False)
        data = []

        for pubs in notification:
            data.append({'id': pubs.id, 'description':pubs.description, 'date': pubs.date, 'lue':pubs.lue})


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def set_notification_lue(request,id):
    try:
        user = Utilisateur.objects.get(identifiant = id)
        notification = Notification.objects.filter(utilisateur = user,  lue = False)
        data = []

        for pubs in notification:
            pubs.lue = True
            pubs.save()

        data.append({"resultat": "oui"})


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


# selection demande par arrondissement

def get_demande_arrondissement(request,id):
    try:
        chef = Chef.objects.get(email = id)
        arrondis = Arrondissement.objects.get(id = chef.arrondissementChef.id)
        demande = Document.objects.all()
        data = []

        for dem in demande:
            if(dem.utilisateur.arrondissement == arrondis and dem.etatDocument == "encours"):
                data.append({
                                "id": dem.id,
                                "nom" : dem.nom,
                               "prenom" : dem.prenom,
                               "adresse" : dem.adresse,
                               "numCni" : dem.numCni,
                               "photo" : str(dem.photo),
                               "declarationPerte ": str(dem.declarationPerte),
                               "certificat" : str(dem.certificat),
                               "acteNaissance" : str(dem.acteNaissance),
                               "etatDocument": dem.etatDocument,
                               "typeDocument": dem.typeDocument,
                               "utilisateur" : dem.utilisateur.identifiant,
                               "date": dem.dateDebut

                               })


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})

@api_view(["POST"])
def refuser_demande_arrondissement(request,id):
    temps = request.POST.get("motif")
    try:
        demande = Document.objects.filter(id = id)
        data = []

        for dem in demande:
            dem.etatDocument = "refuser"
            dem.save()
            notif = Notification(utilisateur = dem.utilisateur,
                                 description = "vous avez reçu la réponse de votre demande de délivrance de votre CNI",
                                 lien = "/Utilisateur/XDemande",
                                 )
            notif.save()
            # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            # client = Client(account_sid, auth_token)

            # message = client.messages.create(
            # from_='+19164768748',
            # body=' Bonjour {} {}, nous sommes dans l\'obligence de refuser votre demande le {} à cause de plusieur motif qui sont : {}.'.format(dem.nom, dem.prenom, dem.dateDebut, temps),
            # to='+261320410659'
            # )
            contenue = ""
            if(dem.typeDocument == "primata"):
                contenue = """
                    <html>
                        <body style="padding: 50px;" border:3px solid black;>
                            <center style="font-size: 1.3em; font-weight: bold;">🔶 RESULTAT DU DEMANDE DE DELIVRANCE 🔶</center>
                            <hr>
                            <br>
                            <p style="font-size: 1.3em;">🔷 Bonjour <span style="font-weight: bold;">{} {}</span></p>
                            <p style="font-size: 1.3em;">Nous regrettons de vous informer que votre demande de carte nationale d'identité le <span style="font-weight: bold;">{}</span> a été refusée.</p>
                            <p style="font-size: 1.3em;">Plusieur raison nous a pousser a le refuser qui sont : </p>
                            <p style="font-size: 1.3em;">Vous pouvez contacter notre service client pour plus d'informations.</p>
                            <p style="font-size: 1.3em;">Cordiallement.</p>
                            <center><p style="font-size: 1.3em;">Ministère de l'intérieur</p></center>
                        </body>
                    </html>
                """.format(dem.nom, dem.prenom, dem.dateDebut, temps)
            elif(dem.typeDocument == "duplicatatUse"):
                contenue = """
                    <html>
                        <body style="padding: 50px; border:3px solid black;">
                            <center style="font-size: 1.3em; font-weight: bold;">🔶 RESULTAT DU DEMANDE DE DELIVRANCE 🔶</center>
                            <hr>
                            <br>
                            <p style="font-size: 1.3em;">🔷 Bonjour <span style="font-weight: bold;">{} {}</span> portant le numero CNI {}</p>
                            <p style="font-size: 1.3em;">Nous regrettons de vous informer que votre demande de carte nationale d'identité le <span style="font-weight: bold;">{}</span> a été refusée.</p>
                            <p style="font-size: 1.3em;">Plusieur raison nous a pousser a le refuser qui sont : <span style="font-weight: bold;">{}</span></p>

                            <p style="font-size: 1.3em;">Cordiallement.</p>
                            <center><p style="font-size: 1.3em;">Ministère de l'intérieur</p></center>

                        </body>
                    </html>
                """.format(dem.nom,  dem.prenom, dem.numCni, dem.dateDebut, temps)
            elif(dem.typeDocument == "duplicatatPerte"):
                contenue = """
                    <html>
                        <body style="padding: 50px; border:3px solid black;">
                            <center style="font-size: 1.3em; font-weight: bold;">🔶 RESULTAT DU DEMANDE DE DELIVRANCE 🔶</center>
                            <hr>
                            <br>
                            <p style="font-size: 1.3em;">🔷 Bonjour <span style="font-weight: bold;">{} {}</span> portant le numero CNI {}</p>
                            <p style="font-size: 1.3em;">Nous regrettons de vous informer que votre demande de carte nationale d'identité le <span style="font-weight: bold;">{}</span> a été refusée.</p>
                            <p style="font-size: 1.3em;">Plusieur raison nous a pousser a le refuser qui sont : <span style="font-weight: bold;">{}</span></p>

                            <p style="font-size: 1.3em;">Cordiallement.</p>
                            <center><p style="font-size: 1.3em;">Ministère de l'intérieur</p></center>
                        </body>
                    </html>
                """.format(dem.nom, dem.prenom,dem.numCni, dem.dateDebut, temps)

            envoie_email(dem.utilisateur.email,"Démande de delivrance de CNI",contenue)


        return JsonResponse({'data': data})
    except:
        return JsonResponse({'data': False})


@api_view(["POST"])
def accepter_demande_arrondissement(request,id):
    dats = request.POST.get("date")
    temps = request.POST.get("temp")
    codes = request.POST.get("code")
    try:
        demande = Document.objects.filter(id = id)

        data = []

        for dem in demande:
            rendevou = Rendezvou(document = dem, date_fin = dats, heure = temps,code = codes)
            rendevou.save()

            # dem.utilisateur.arrondissement.district.region :

            notif = Notification(utilisateur = dem.utilisateur,
                                 description = "vous avez reçu la réponse de votre demande de délivrance de votre CNI",
                                 lien = "/Utilisateur/XDemande",
                                 )
            notif.save()
            dem.etatDocument = "accepter"
            dem.save()
            # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            # client = Client(account_sid, auth_token)

            # message = client.messages.create(
            # from_='+19164768748',
            # body=' Bonjour {} {}, nous sommes ravit de informer que votre demande de carte National d\'identité a été approuvé rendez-vous le {} à {} afin de valider et recuperer votre CNI.'.format(dem.nom, dem.prenom, dats, temps),
            # to='+261320410659'
            # )

            contenue = ""
            if(dem.typeDocument == "primata"):
                contenue = """
                <html>
                    <body style="padding: 50px; border:3px solid black;">
                        <center style="font-size: 1.3em; font-weight: bold;">🔶 RESULTAT DU DEMANDE DE DELIVRANCE 🔶</center>
                        <hr>
                        <br>
                        <p style="font-size: 1.3em;">🔷 Bonjour <span style="font-weight: bold;">{} {}</span></p>
                        <p style="font-size: 1.3em;">Nous avons le plaisir de vous informer que votre demande de carte nationale d'identité envoyer le <span style="font-weight: bold;">{}</span> a été acceptée.</p>
                        <p style="font-size: 1.3em;">Vous pouvez venir récupérer votre CNI le <span style="font-weight: bold;">{}</span> à <span style="font-weight: bold;">{}</span> selon les instructions fournies précédemment.</p>
                        <p style="font-size: 1.3em;">Cordiallement.</p>
                        <center><p style="font-size: 1.3em;">Ministère de l'intérieur</p></center>
                    </body>
                </html>
                """.format(dem.nom, dem.prenom, dem.dateDebut, dats, temps)
            elif(dem.typeDocument == "duplicatatUse"):
                contenue = """
                <html>
                    <body style="padding: 50px; border:3px solid black;">
                        <center style="font-size: 1.3em; font-weight: bold;">🔶 RESULTAT DU DEMANDE DE DELIVRANCE 🔶</center>
                        <hr>
                        <br>
                        <p style="font-size: 1.3em;">🔷 Bonjour <span style="font-weight: bold;">{} {}</span> portant le numero CNI {}</p>
                        <p style="font-size: 1.3em;">Nous avons le plaisir de vous informer que votre demande de carte nationale d'identité envoyer le <span style="font-weight: bold;">{}</span> a été acceptée.</p>
                        <p style="font-size: 1.3em;">Vous pouvez venir récupérer votre CNI le <span style="font-weight: bold;">{}</span> à <span style="font-weight: bold;">{}</span> selon les instructions fournies précédemment.</p>
                        <p style="font-size: 1.3em;">De plus, veuillez noter que votre CNI est délivrée en tant que duplicata en raison de l'usure de votre précédent document. Assurez-vous de prendre soin de votre nouvelle carte d'identité.</p>
                        <p style="font-size: 1.3em;">Cordiallement.</p>
                        <center><p style="font-size: 1.3em;">Ministère de l'intérieur</p></center>
                    </body>
                </html>
                """.format(dem.nom, dem.prenom, dem.numCni, dem.dateDebut, dats, temps)
            elif(dem.typeDocument == "duplicatatPerte"):
                 contenue = """
                    <html>
                        <body style="padding: 50px; border:3px solid black;">
                            <center style="font-size: 1.3em; font-weight: bold;">🔶 RESULTAT DU DEMANDE DE DELIVRANCE 🔶</center>
                            <hr>
                            <br>
                            <p style="font-size: 1.3em;">🔷 Bonjour <span style="font-weight: bold;">{} {}</span> portant le numero CNI {}</p>
                            <p style="font-size: 1.3em;">Nous avons le plaisir de vous informer que votre demande de carte nationale d'identité envoyer le <span style="font-weight: bold;">{}</span> a été acceptée.</p>
                            <p style="font-size: 1.3em;">Vous pouvez venir récupérer votre CNI le <span style="font-weight: bold;">{}</span> à <span style="font-weight: bold;">{}</span> selon les instructions fournies précédemment.</p>
                            <p style="font-size: 1.3em;">De plus, veuillez noter que votre CNI est délivrée en tant que duplicata en raison de la perte de votre précédent CNI. Assurez-vous de prendre soin de votre nouvelle carte d'identité.</p>
                            <p style="font-size: 1.3em;">Cordiallement.</p>
                            <center><p style="font-size: 1.3em;">Ministère de l'intérieur</p></center>
                        </body>
                    </html>
                """.format(dem.nom, dem.prenom,dem.numCni, dem.dateDebut, dats, temps)

            envoie_email(dem.utilisateur.email,"Démande de delivrance de CNI",contenue)




        return JsonResponse({'data': data})
    except:
        return JsonResponse({'data': False})


def stat_arrondissement_chef(request,id):
    try:
        chef = Chef.objects.get(email=id)
        doc = Document.objects.all()
        # arrond = Arrondissement.objects.get(identifiant = id)
        encour = 0
        accepter = 0
        refuser = 0
        data = []

        for pubs in doc:
            if(chef.arrondissementChef == pubs.utilisateur.arrondissement):
                if(pubs.etatDocument == "encours"):
                    encour+=1
                elif(pubs.etatDocument == "refuser"):
                    refuser+=1
                elif(pubs.etatDocument == "accepter"):
                    accepter+=1


        data.append({"encour": encour, "refuser": refuser, "accepter": accepter})

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


@api_view(["POST"])
def stat_arrondissement_specifique(request,id):
    try:
        r = request.POST.get('type') 
        doc = Document.objects.all()
        arrond = Arrondissement.objects.get(id = id)
        encour = 0
        accepter = 0
        refuser = 0
        data = []



        if(r == ""):
            for pubs in doc:
                if(arrond == pubs.utilisateur.arrondissement):
                    if(pubs.etatDocument == "encours"):
                        encour+=1
                    elif(pubs.etatDocument == "refuser"):
                        refuser+=1
                    elif(pubs.etatDocument == "accepter"):
                        accepter+=1
        else:
            for pubs in doc:
                if(arrond == pubs.utilisateur.arrondissement and pubs.typeDocument == r):
                    if(pubs.etatDocument == "encours"):
                        encour+=1
                    elif(pubs.etatDocument == "refuser"):
                        refuser+=1
                    elif(pubs.etatDocument == "accepter"):
                        accepter+=1


        data.append({"encour": encour, "refuser": refuser, "accepter": accepter})

        encour = 0
        accepter = 0
        refuser = 0

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})




def stat_arrondissement_tous(request,id):

    try:
        doc = Document.objects.all()
        arrond = Arrondissement.objects.get(id = id)
        encour = 0
        accepter = 0
        refuser = 0
        data = []


        
        for pubs in doc:
                if(arrond == pubs.utilisateur.arrondissement):
                    if(pubs.etatDocument == "encours"):
                        encour+=1
                    elif(pubs.etatDocument == "refuser"):
                        refuser+=1
                    elif(pubs.etatDocument == "accepter"):
                        accepter+=1


        data.append({"encour": encour, "refuser": refuser, "accepter": accepter})

        encour = 0
        accepter = 0
        refuser = 0

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})






def stat_utilisateur_tous(request):
    try:
        users = Utilisateur.objects.all()

        data = []
        for user in users:
            data.append({'identifiant': user.identifiant, })

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data':False})


def stat_utilisateur_arrond(request,id, anne):
    noms_mois = [
    "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Decembre"
]
    try:
        users = Utilisateur.objects.all()
        chef = Chef.objects.get(email=id)
        data = []
        nombre = 0
        i = 1
        for mois in noms_mois:

            for user in users:
                if(chef.arrondissementChef == user.arrondissement and user.date_inscription.month == (i) and user.date_inscription.year == anne):
                    nombre += 1

                print(user.date_inscription.year)
            data.append({mois: nombre, })
            nombre = 0
            i+=1

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data':False})

def stat_utilisateur_arrond_tous(request, anne):
    noms_mois = [
    "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"
]
    try:
        users = Utilisateur.objects.all()

        data = []
        nombre = 0
        i = 1
        for mois in noms_mois:

            for user in users:
                if(user.date_inscription.month == (i) and user.date_inscription.year == anne and user.identifiant !="admin"):
                    nombre += 1


            data.append({mois: nombre, })
            nombre = 0
            i+=1

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data':False})



def get_rdv(request,id):
    try:
        user = Utilisateur.objects.get (identifiant = id)
        demande = Document.objects.get(utilisateur = user, archiver = False)
        rsv = Rendezvou.objects.filter(document = demande)
        data = []
        for dem in rsv:
                data.append({
                                "id": dem.id,
                                "date_fin" : dem.date_fin,
                               "code" : dem.code,
                               "heure" : dem.heure,
                               "recuperer" : dem.recuperer,

                               })


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def get_rdv_tous(request):
    try:
        rsv = Rendezvou.objects.all()
        data = []
        for dem in rsv:
            if dem.recuperer == False:
                data.append({
                                "id": dem.id,
                                "date_fin" : dem.date_fin,
                               "code" : dem.code,
                               "heure" : dem.heure,
                               "recuperer" : dem.recuperer,
                               "nom" : dem.document.nom,
                               "prenom" : dem.document.prenom,
                               "adresse" : dem.document.adresse,
                               "type_document" : dem.document.typeDocument,
                               "photo" : str(dem.document.photo),

                               })


        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def update_rdv(request,id):
    try:
        rsv = Rendezvou.objects.get(id = id)
        doc = Document.objects.get(id = rsv.document.id)
        rsv.recuperer = True
        rsv.save()

        doc.archiver = True
        doc.save()
        return JsonResponse({'data': True})
    except:
        return JsonResponse({'data': False})


@api_view(["POST"])
def ajouter_retour(request,id):
    try:
        user = Utilisateur.objects.get(identifiant = id)
        retour = Retour( note = request.POST.get("note"), utilisateur =  user)
        retour.save()
        return JsonResponse({'data': True})
    except:
        return JsonResponse({'data': False})

def voir_retour(request):
    try:
        retour = Retour.objects.all()
        un = 0
        deux = 0
        troi = 0
        quatre = 0
        cinq = 0
        total = 0
        data = []

        for rets in retour:
            if rets.note == 1:
               un += 1
            elif rets.note == 2:
               deux += 1
            elif rets.note == 3:
               troi += 1
            elif rets.note == 4:
               quatre += 1
            elif rets.note == 5:
               cinq += 1

            total += 1

        un = math.floor((un*100)/total)
        deux = math.floor((deux*100)/total)
        troi = math.floor((troi*100)/total)
        quatre = math.floor((quatre*100)/total)
        cinq = math.floor((cinq*100)/total)
        total = 100

        data.append({"un": un, "deux": deux, "trois": troi, "cinq":cinq, "quatre":quatre, "total":total})

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def get_region(request):
    try:
        region = Region.objects.all().order_by('nom')
        data = []

        for region in region:
            if(region.nom != "tous"):
                data.append({'id':region.id,'nom':region.nom, 'code':region.code})



        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def get_district(request,id):
    try:
        district = District.objects.all()
        region = Region.objects.get(id = id)
        data = []

        for district in district:
            if(district.nom != "tous" and district.region == region):
                data.append({'id':district.id,'nom':district.nom, 'code':district.code, 'region': district.region.nom})



        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def get_district_all(request):
    try:
        district = District.objects.all().order_by('region').order_by("nom")
        data = []

        for district in district:
            if(district.nom != "tous"):
                data.append({'id':district.id,'nom':district.nom, 'code':district.code, 'region': district.region.nom,'region_id': district.region.id})



        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})



def get_arrondissement_par_district(request,id):
    try:
        arrondissements = Arrondissement.objects.all()
        district = District.objects.get(id = id)
        data = []

        for arrondissement in arrondissements:
            if(arrondissement.nom != "tous" and arrondissement.district == district):
                data.append({'id':arrondissement.id,'nom':arrondissement.nom, 'code':arrondissement.code,'district':arrondissement.district.nom})



        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})



def get_arrondissement_par_district_libre(request,id):
    try:
        arrondissements = Arrondissement.objects.all()
        district = District.objects.get(id = id)
        data = []

        for arrondissement in arrondissements:
            if(arrondissement.nom != "tous" and arrondissement.district == district and arrondissement.diriger == "non"):
                data.append({'id':arrondissement.id,'nom':arrondissement.nom, 'code':arrondissement.code,'district':arrondissement.district.nom})



        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data': False})


def get_uploaded_file_url(request):
    # Supposons que vous avez un modèle UploadedFile avec un champ 'file'
    # qui stocke le chemin du fichier téléchargé.
    uploaded_file = Utilisateur.objects.first()  # Récupère le dernier fichier téléchargé
    r = []
    if uploaded_file:


        return JsonResponse({'file_url': str(uploaded_file.photo)})
    else:
        return JsonResponse({'error': 'No uploaded file found'}, status=404)




@api_view(["POST"])
def gestionKaratra(request,id):
    doc = Document.objects.filter(id = id)

    karatra = Karatra.objects.all()

    if(len(karatra) == 0):
         for docs in doc:
                r = str(docs.utilisateur.arrondissement.district.region.code)+str(docs.utilisateur.arrondissement.district.code)+str(docs.utilisateur.arrondissement.code)+str(docs.sexe)
                if(docs.typeDocument == "primata"):
                    s = r+("000001")
                    kart = Karatra(numero = s, document = docs)
                    kart.save()
                    return JsonResponse({"data":"pas de carte existant"})
                elif(docs.typeDocument == "duplicataUse" or docs.typeDocument == "duplicataPerte"):
                    kart = Karatra(numero = docs.numCni, document = docs)
                    kart.save()
                    return JsonResponse({"data":"pas de carte existant"})
    for v in karatra:
            for docs in doc:
                r = str(docs.utilisateur.arrondissement.district.region.code)+str(docs.utilisateur.arrondissement.district.code)+str(docs.utilisateur.arrondissement.code)
                if(docs.typeDocument == "primata"):
                    if(v.numero.__contains__(r)):
                        orig = karatra[len(karatra)-1].numero
                        final = ""
                        for i in range(len(orig)):
                            if(i == 5):
                                final = final + str(docs.sexe)
                            else:
                                final = final + orig[i]
                        kart = Karatra(numero = str(int(final)+1) , document = docs)
                        kart.save()
                        return JsonResponse({'data': 'suite carte'})
                    else:
                        s = r+("000001")
                        kart = Karatra(numero = s, document = docs)
                        kart.save()
                        return JsonResponse({"data":"pas de carte existant"})
                elif(docs.typeDocument == "duplicataUse" or docs.typeDocument == "duplicataPerte"):
                    kart = Karatra(numero = docs.numCni, document = docs)
                    kart.save()
                    return JsonResponse({"data":"pas de carte existant"})


def affiche_karatra(request, id):
    user = Utilisateur.objects.get(identifiant=id)
    kart = Karatra.objects.all()
    dat = []
    for karts in kart:
        if(karts.document.utilisateur == user and karts.document.archiver == True):
            dat.append({'photo':str(karts.document.photo),'nom':karts.document.nom,'prenom':karts.document.prenom,'numCNI': karts.numero,'adresse':karts.document.adresse, 'date':karts.date})
            return JsonResponse({'data': dat})

    return JsonResponse({'data':'aucun'})


def affiche_karatra_tous(request):
    try:
        kart = Karatra.objects.all()
        dat = []
        for karts in kart:
            dat.append({'photo':str(karts.document.photo),'nom':karts.document.nom,'prenom':karts.document.prenom,'numCNI': karts.numero,'adresse':karts.document.adresse, 'date':karts.date})


        return JsonResponse({'data': dat})
    except:
        return JsonResponse({'data': 'false'})


def stat_karatra (request,anne):
    noms_mois = [
    "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"
    ]
    try:
        users = Karatra.objects.all()

        data = []
        nombre = 0
        i = 1
        for mois in noms_mois:

            for user in users:
                if(user.date.month == (i) and user.date.year == anne):
                    nombre += 1


            data.append({mois: nombre, })
            nombre = 0
            i+=1

        return JsonResponse({'data': data,})
    except:
        return JsonResponse({'data':False})


# api verification des documents
@api_view(["POST"])
def verifier_certificat(request):
    try:
        api_key = 'acc_e201826d4119173'
        api_secret = '5aec3dbd2376f2f590ac3f7f3e3df044'
        image_file = request.FILES['certificat']

        response = requests.post(
            'https://api.imagga.com/v2/text',
            auth=(api_key, api_secret),
            files={'image': image_file})

        r = response.json().get('result', {}).get('text', [])

        for j in r:
            if str(j["data"]).lower().__contains__("certificat de residence"):
                return JsonResponse({'data': True})

        return JsonResponse({'data': False})
    except:
        return JsonResponse({'data': False})

@api_view(["POST"])
def verifier_acte(request):
    try:
        api_key = 'acc_e201826d4119173'
        api_secret = '5aec3dbd2376f2f590ac3f7f3e3df044'
        image_file = request.FILES['acte']

        response = requests.post(
            'https://api.imagga.com/v2/text',
            auth=(api_key, api_secret),
            files={'image': image_file})

        r = response.json().get('result', {}).get('text', [])

        for j in r:
            if str(j["data"]).lower().__contains__("acte de naissance"):
                return JsonResponse({'data': True})

        return JsonResponse({'data': False})
    except:
        return JsonResponse({'data': False})

@api_view(["POST"])
def verifier_perte(request):
    try:
        api_key = 'acc_e201826d4119173'
        api_secret = '5aec3dbd2376f2f590ac3f7f3e3df044'
        image_file = request.FILES['perte']

        response = requests.post(
            'https://api.imagga.com/v2/text',
            auth=(api_key, api_secret),
            files={'image': image_file})

        r = response.json().get('result', {}).get('text', [])

        for j in r:
             if str(j["data"]).lower().__contains__("declaration de perte"):
                return JsonResponse({'data': True})

        print("fatal")
        return JsonResponse({'data': False})
    except:
        print("fatal")
        return JsonResponse({'data': False})

@api_view(["POST"])
def verifier_photo(request):
    try:
        api_key = 'acc_e201826d4119173'
        api_secret = '5aec3dbd2376f2f590ac3f7f3e3df044'
        image_file = request.FILES['photo']

        response = requests.post(
            'https://api.imagga.com/v2/tags',
            auth=(api_key, api_secret),
            files={'image': image_file})

        r = response.json().get('result', {}).get('tags', [])
        one = False
        two = False
        genre = ""
        for i in r:
            if(i["confidence"]>=20):
                    
                if i['tag']['en'] == "portrait" :
                    two = True
                
                if i['tag']['en'] == "male" or i['tag']['en'] == "woman" :
                    genre = i['tag']['en']
                    one = True
                if(one and two):
                    print("ok")
                    return JsonResponse({'data': True, 'genre':genre})

        return JsonResponse({'data': False})
    except:
        return JsonResponse({'data': False})
    

@api_view(["POST"])
def verification_dupli(request):
    try:
        doc = Karatra.objects.filter(numero = request.POST.get("numCni"))
        count = 0
        
        for i in range(doc.count()):
            count+=1
            
        return JsonResponse({'data': count})
    except:
        return JsonResponse({'data': False}) 
