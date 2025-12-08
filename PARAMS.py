import requests
import urllib.parse


FILE_LOCATION = "C:\\Users\\jani\\Downloads\\useless-shit.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; VeetiBot/1.0; +https://example.com)"
}

BASE_URL = "https://www.nettimokki.com/vuokramokit/mokit-jarven-rannalla/"

PARAMS = {
    "item_availability__date_from"   : "2026-07-01",       # change via params_set_date(a,b)
    "item_availability__date_to"     : "2026-07-07",       # change via params_set_date(a,b)
    "page"                           : "null",             # change via params_set_page(a)
    "item__is_payment_ad"            : "null",             # change via params_set_nettimaksu(True)
    "item__avg_overall_rating_4"     : "null",             # change via params_set_require_4_stars(True)

    "attr__number_of_bedrooms[0]"    : "null",             #
    "attr__number_of_bedrooms[1]"    : "null",             # change via params_set_bedrooms(a)
    "attr__number_of_bedrooms[2]"    : "null",             # or change via params_set_bedrooms_range(a,b)
    "attr__number_of_bedrooms[3]"    : "null",             #

    "attr__type_of_waters[0]"        : "null",             # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_waters[1]"        : "null",             #
    "attr__type_of_waters[2]"        : "null",             # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_waters[3]"        : "null",             #

    "attr__type_of_beach[0]"         : "null",             # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_beach[1]"         : "null",             #
    "attr__type_of_beach[2]"         : "null",             # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_beach[3]"         : "null",             #

    "attr__electric_sauna"           : "null",             #
    "attr__smoke_sauna"              : "null",             # change via params_set_sauna(electric_sauna = False, smoke_sauna = False, wood_sauna = False)
    "attr__wood_sauna"               : "null",             #

    "attr__dishwater"                : "null",
    "attr__refridgerator"            : "null",
    "attr__cooking_possibility"      : "null",
    "attr__microwave_oven"           : "null",
    "attr__freezer"                  : "null",
    "attr__stove"                    : "null",             # change via params_set_kitchen_equipment(astianpesukone = False, jääkaappi = False, keittomahdollisuus = False, mikroaaltouuni = False, pakastin = False, liesi = False, uuni = False, kahvinkeitin = False, grillikota = False, ):
    "attr__owen"                     : "null",
    "attr__coffee_maker"             : "null",
    "attr__barbecue_hut"             : "null",

    "attr__ski_center_nearby"        : "null",             # change via def params_set_features(hiihtokeskus_lähellä=False, internetyhteys=False, kuivauskaappi=False, kuivausrumpu=False, laituri=False, parvi=False, palju=False, poreamme=False, pyykinpesukone=False, syöttötuoli=False, suihku=False, sähköauton_lataus=False, takka=False, tv=False, uima_allas=False, ulkoporeallas=False, vauvasänky=False, mökkissä_ei_sähköjä=False, sähkö_aurinkopaneeleista=False, kantovesi=False, viilentävä_ilmalämpöpumppu=False, sisä_wc=False, ulko_wc=False, vene=False, kanootti=False, lemmikit_sallittu=False)
    "attr__internet"                 : "null",
    "attr__drying_cabinet"           : "null",
    "attr__tumble_dryer"             : "null",
    "attr__pier"                     : "null",
    "attr__loft"                     : "null",
    "attr__outdoor_hot_tub_barrel_style" : "null",
    "attr__hot_tub"                  : "null",
    "attr__washing_machine"          : "null",
    "attr__feeding_chair"            : "null",
    "attr__shower"                   : "null",
    "attr__electric_vehicle_charging": "null",
    "attr__fireplace_decoration"     : "null",
    "attr__television"               : "null",
    "attr__swimming_pool"            : "null",
    "attr__outdoor_hot_tub"          : "null",
    "attr__baby_crib"                : "null",
    "attr__no_electricity"           : "null",
    "attr__solar_panel_electricity"  : "null",
    "attr__water_carried"            : "null",
    "attr__ac_unit"                  : "null",
    "attr__indoor_toilet"            : "null",
    "attr__outoor_toilet"            : "null",
    "attr__boat"                     : "null",
    "attr__paddling"                 : "null",
    "attr__pets_allowed"             : "null",

    "attr__wheel_chair_accessible"   : "null",

}


# --------------- params / muuttojen funktiot ---------------
def params_clean(PARAMS = PARAMS): # PITÄÄ käyttää, muuten nullit ovat literaaleja

    PARAMS = {k: v for k, v in PARAMS.items() if v != "null"}

    return PARAMS

def params_set_date(date_from, date_to): # format vvvv-kk-pv

    global PARAMS

    PARAMS.update({
    "item_availability__date_from": date_from,
    "item_availability__date_to": date_to
    })
    
def params_set_page(page): # menee asetetulle sivulle, ei tarkista onko olemassa jne, käytä for loopis tai jotai

    global PARAMS

    PARAMS.update({
    "page": page
    })

def params_set_nettimaksu(a): # tarvii True / False

    global PARAMS
    if a:
        PARAMS.update({
            "item__is_payment_ad" : 1
        })
    else:
        PARAMS.update({
            "item__is_payment_ad" : "null"
        })

def params_set_require_4_stars(a): # tarvii True / False
    global PARAMS
    if a:
        PARAMS.update({
            "item__avg_overall_rating_4" : 1
        })
    else:
        PARAMS.update({
            "item__avg_overall_rating_4" : "null"
        })

def params_set_bedrooms(a): # asettaa tarkan haettavan huoneitten määrän, esim 2 on vaan 2 makuuhuonetta ei enemmän ei vähemmän
    global PARAMS

    PARAMS.update({ # Tyhjentää vanhat pois 
        "attr__number_of_bedrooms[0]" : "null",
        "attr__number_of_bedrooms[1]" : "null",
        "attr__number_of_bedrooms[2]" : "null",
        "attr__number_of_bedrooms[3]" : "null",
    })

    PARAMS.update({ # Laittaa valitun huoneitten määrän
        "attr__number_of_bedrooms[0]": a
    })

def params_set_bedrooms_range(a,b): # asettaa haettavan numeroalueen makuuhuoneen määrän varten, esim 1,4 etsii kaikki paikat jossa on 1-4 huonetta
                                                # range 1-4
    global PARAMS
    if(a >= 5 or a <= 0 or b >= 5 or b <= 0):   # asettaa range 1-4 
        return "range is 1-4"
    
    PARAMS.update({                             # Tyhjentää vanhat pois 
        "attr__number_of_bedrooms[0]" : "null",
        "attr__number_of_bedrooms[1]" : "null",
        "attr__number_of_bedrooms[2]" : "null",
        "attr__number_of_bedrooms[3]" : "null",
    })

    if(a<b):                                    # tarkista numerojärjestys
        for i in range(0, b-a+1):
            k = f"attr__number_of_bedrooms[{i}]"

            PARAMS.update({ 
                k : a+i,
            })
    else:
        for i in range(0, a-b+1):
            k = f"attr__number_of_bedrooms[{i}]"
            
            PARAMS.update({ 
                k : a+i,
            })

def params_set_water(järvi = False, meri = False, joki = False, lampi = False): # asettaa halutut vesistön tyyppi parametrit
    
    global PARAMS

    PARAMS.update({ # Tyhjentää vanhat pois 
        "attr__type_of_waters[0]" : "null",                 
        "attr__type_of_waters[1]" : "null",                 
        "attr__type_of_waters[2]" : "null",                 
        "attr__type_of_waters[3]" : "null",                 
    })

    if(järvi):
        PARAMS.update({ 
            "attr__type_of_waters[0]" : 4503,                         
        })

    if(meri):
        PARAMS.update({ 
            "attr__type_of_waters[1]" : 4504,                         
        })

    if(joki):
        PARAMS.update({ 
            "attr__type_of_waters[2]" : 4505,                         
        })

    if(lampi):
        PARAMS.update({ 
            "attr__type_of_waters[3]" : 4507,                         
        })

def params_set_beach(oma = False, jaettu = False, käyttöoikeus_ranttan = False, käyttöoikeus_vesialueisiin = False): # asettaa halutut ranta parametrit
    global PARAMS

    PARAMS.update({
        "attr__type_of_beach[0]" : "null",                 
        "attr__type_of_beach[1]" : "null",                 
        "attr__type_of_beach[2]" : "null",                 
        "attr__type_of_beach[3]" : "null", 

    })

    if(oma):
        PARAMS.update({
            "attr__type_of_beach[0]" : "own_beach"
        })
    if(jaettu):
        PARAMS.update({
            "attr__type_of_beach[1]" : "shared_beach"
        })
    if(käyttöoikeus_ranttan):
        PARAMS.update({
            "attr__type_of_beach[2]" : "permission_to_use_beach"
        })
    if(käyttöoikeus_vesialueisiin):
        PARAMS.update({
            "attr__type_of_beach[3]" : "permission_to_use_waterways"
        })

def params_set_kitchen_equipment(astianpesukone = False, jääkaappi = False, keittomahdollisuus = False, mikroaaltouuni = False, pakastin = False, liesi = False, uuni = False, kahvinkeitin = False, grillikota = False, ):
    global PARAMS
    PARAMS.update({
        "attr__dishwater"                : "null",
        "attr__refridgerator"            : "null",
        "attr__cooking_possibility"      : "null",
        "attr__microwave_oven"           : "null",
        "attr__freezer"                  : "null",
        "attr__stove"                    : "null",
        "attr__owen"                     : "null",
        "attr__coffee_maker"             : "null",
        "attr__barbecue_hut"             : "null",
    })

    if(astianpesukone):
        PARAMS.update({
            "attr__dishwater" : "1"
        })

    if(jääkaappi):
        PARAMS.update({
            "attr__dishwater" : "1"
        })

    if(keittomahdollisuus):
        PARAMS.update({
            "attr__dishwater" : "1"
        })

    if(mikroaaltouuni):
        PARAMS.update({
            "attr__dishwater" : "1"
        })


    if(pakastin):
        PARAMS.update({
            "attr__dishwater" : "1"
        })


    if(liesi):
        PARAMS.update({
            "attr__dishwater" : "1"
        })


    if(uuni):
        PARAMS.update({
            "attr__dishwater" : "1"
        })


    if(kahvinkeitin):
        PARAMS.update({
            "attr__dishwater" : "1"
        })


    if(grillikota):
        PARAMS.update({
            "attr__dishwater" : "1"
        })

def params_set_sauna(electric_sauna = False, smoke_sauna = False, wood_sauna = False):
    global PARAMS

    PARAMS.update({
        "attr__electric_sauna"  : "null",
        "attr__smoke_sauna"     : "null",
        "attr__wood_sauna"      : "null",
    })

    if(electric_sauna):
        PARAMS.update({
            "attr__electric_sauna"  : "1",
        })


    if(smoke_sauna):
        PARAMS.update({
            "attr__smoke_sauna"  : "1",
        })


    if(wood_sauna):
        PARAMS.update({
            "attr__wood_sauna"  : "1",
        })

def params_set_features(hiihtokeskus_lähellä=False, internetyhteys=False, kuivauskaappi=False, kuivausrumpu=False, laituri=False, parvi=False, palju=False, poreamme=False, pyykinpesukone=False, syöttötuoli=False, suihku=False, sähköauton_lataus=False, takka=False, tv=False, uima_allas=False, ulkoporeallas=False, vauvasänky=False, mökkissä_ei_sähköjä=False, sähkö_aurinkopaneeleista=False, kantovesi=False, viilentävä_ilmalämpöpumppu=False, sisä_wc=False, ulko_wc=False, vene=False, kanootti=False, lemmikit_sallittu=False):
    global PARAMS
    PARAMS.update({
        "attr__ski_center_nearby"        : "null",
        "attr__internet"                 : "null",
        "attr__drying_cabinet"           : "null",
        "attr__tumble_dryer"             : "null",
        "attr__pier"                     : "null",
        "attr__loft"                     : "null",
        "attr__outdoor_hot_tub_barrel_style" : "null",
        "attr__hot_tub"                  : "null",
        "attr__washing_machine"          : "null",
        "attr__feeding_chair"            : "null",
        "attr__shower"                   : "null",
        "attr__electric_vehicle_charging": "null",
        "attr__fireplace_decoration"     : "null",
        "attr__television"               : "null",
        "attr__swimming_pool"            : "null",
        "attr__outdoor_hot_tub"          : "null",
        "attr__baby_crib"                : "null",
        "attr__no_electricity"           : "null",
        "attr__solar_panel_electricity"  : "null",
        "attr__water_carried"            : "null",
        "attr__ac_unit"                  : "null",
        "attr__indoor_toilet"            : "null",
        "attr__outoor_toilet"            : "null",
        "attr__boat"                     : "null",
        "attr__paddling"                 : "null",
        "attr__pets_allowed"             : "null",
    })

    if (hiihtokeskus_lähellä):
        PARAMS.update({"attr_ski_center_nearby": "1"})
    if (internetyhteys):
        PARAMS.update({"attr_internet": "1"})
    if (kuivauskaappi):
        PARAMS.update({"attr_drying_cabinet": "1"})
    if (kuivausrumpu):
        PARAMS.update({"attr_tumble_dryer": "1"})
    if (laituri):
        PARAMS.update({"attr_pier": "1"})
    if (parvi):
        PARAMS.update({"attr_loft": "1"})
    if (palju):
        PARAMS.update({"attr_outdoor_hot_tub_barrel_style": "1"})
    if (poreamme):
        PARAMS.update({"attr_hot_tub": "1"})
    if (pyykinpesukone):
        PARAMS.update({"attr_washing_machine": "1"})
    if (syöttötuoli):
        PARAMS.update({"attr_feeding_chair": "1"})
    if (suihku):
        PARAMS.update({"attr_shower": "1"})
    if (sähköauton_lataus):
        PARAMS.update({"attr_electric_vehicle_charging": "1"})
    if (takka):
        PARAMS.update({"attr_fireplace_decoration": "1"})
    if (tv):
        PARAMS.update({"attr_television": "1"})
    if (uima_allas):
        PARAMS.update({"attr_swimming_pool": "1"})
    if (ulkoporeallas):
        PARAMS.update({"attr_outdoor_hot_tub": "1"})
    if (vauvasänky):
        PARAMS.update({"attr_baby_crib": "1"})
    if (mökkissä_ei_sähköjä):
        PARAMS.update({"attr_no_electricity": "1"})
    if (sähkö_aurinkopaneeleista):
        PARAMS.update({"attr_solar_panel_electricity": "1"})
    if (kantovesi):
        PARAMS.update({"attr_water_carried": "1"})
    if (viilentävä_ilmalämpöpumppu):
        PARAMS.update({"attr_ac_unit": "1"})
    if (sisä_wc):
        PARAMS.update({"attr_indoor_toilet": "1"})
    if (ulko_wc):
        PARAMS.update({"attr_outoor_toilet": "1"})
    if (vene):
        PARAMS.update({"attr_boat": "1"})
    if (kanootti):
        PARAMS.update({"attr_paddling": "1"})
    if (lemmikit_sallittu):
        PARAMS.update({"attr_pets_allowed": "1"})

def params_set_wheelchair_accessibility(wheelchair = False):
    global PARAMS
    PARAMS.update({
        "attr__wheel_chair_accessible"   : "null",
    })

    if(wheelchair):
        PARAMS.update({
            "attr__wheel_chair_accessible"   : "1",
        })

def params_set_none():
    global PARAMS
    PARAMS.update({
    "item_availability__date_from"   : "null",       # change via params_set_date(a,b)
    "item_availability__date_to"     : "null",       # change via params_set_date(a,b)
    "page"                           : "null",             # change via params_set_page(a)
    "item__is_payment_ad"            : "null",             # change via params_set_nettimaksu(True)
    "item__avg_overall_rating_4"     : "null",             # change via params_set_require_4_stars(True)

    "attr__number_of_bedrooms[0]"    : "null",             #
    "attr__number_of_bedrooms[1]"    : "null",             # change via params_set_bedrooms(a)
    "attr__number_of_bedrooms[2]"    : "null",             # or change via params_set_bedrooms_range(a,b)
    "attr__number_of_bedrooms[3]"    : "null",             #

    "attr__type_of_waters[0]"        : "null",             # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_waters[1]"        : "null",             #
    "attr__type_of_waters[2]"        : "null",             # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_waters[3]"        : "null",             #

    "attr__type_of_beach[0]"         : "null",             # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_beach[1]"         : "null",             #
    "attr__type_of_beach[2]"         : "null",             # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_beach[3]"         : "null",             #

    "attr__electric_sauna"           : "null",             #
    "attr__smoke_sauna"              : "null",             # change via params_set_sauna(electric_sauna = False, smoke_sauna = False, wood_sauna = False)
    "attr__wood_sauna"               : "null",             #

    "attr__dishwater"                : "null",
    "attr__refridgerator"            : "null",
    "attr__cooking_possibility"      : "null",
    "attr__microwave_oven"           : "null",
    "attr__freezer"                  : "null",
    "attr__stove"                    : "null",             # change via params_set_kitchen_equipment(astianpesukone = False, jääkaappi = False, keittomahdollisuus = False, mikroaaltouuni = False, pakastin = False, liesi = False, uuni = False, kahvinkeitin = False, grillikota = False, ):
    "attr__owen"                     : "null",
    "attr__coffee_maker"             : "null",
    "attr__barbecue_hut"             : "null",

    "attr__ski_center_nearby"        : "null",             # change via def params_set_features(hiihtokeskus_lähellä=False, internetyhteys=False, kuivauskaappi=False, kuivausrumpu=False, laituri=False, parvi=False, palju=False, poreamme=False, pyykinpesukone=False, syöttötuoli=False, suihku=False, sähköauton_lataus=False, takka=False, tv=False, uima_allas=False, ulkoporeallas=False, vauvasänky=False, mökkissä_ei_sähköjä=False, sähkö_aurinkopaneeleista=False, kantovesi=False, viilentävä_ilmalämpöpumppu=False, sisä_wc=False, ulko_wc=False, vene=False, kanootti=False, lemmikit_sallittu=False)
    "attr__internet"                 : "null",
    "attr__drying_cabinet"           : "null",
    "attr__tumble_dryer"             : "null",
    "attr__pier"                     : "null",
    "attr__loft"                     : "null",
    "attr__outdoor_hot_tub_barrel_style" : "null",
    "attr__hot_tub"                  : "null",
    "attr__washing_machine"          : "null",
    "attr__feeding_chair"            : "null",
    "attr__shower"                   : "null",
    "attr__electric_vehicle_charging": "null",
    "attr__fireplace_decoration"     : "null",
    "attr__television"               : "null",
    "attr__swimming_pool"            : "null",
    "attr__outdoor_hot_tub"          : "null",
    "attr__baby_crib"                : "null",
    "attr__no_electricity"           : "null",
    "attr__solar_panel_electricity"  : "null",
    "attr__water_carried"            : "null",
    "attr__ac_unit"                  : "null",
    "attr__indoor_toilet"            : "null",
    "attr__outoor_toilet"            : "null",
    "attr__boat"                     : "null",
    "attr__paddling"                 : "null",
    "attr__pets_allowed"             : "null",

    "attr__wheel_chair_accessible"   : "null",})

def params_set_all():
    global PARAMS

    PARAMS.update({
    "item_availability__date_from"   : "1",       # change via params_set_date(a,b)
    "item_availability__date_to"     : "1",       # change via params_set_date(a,b)
    "page"                           : "1",             # change via params_set_page(a)
    "item__is_payment_ad"            : "1",             # change via params_set_nettimaksu(True)
    "item__avg_overall_rating_4"     : "1",             # change via params_set_require_4_stars(True)

    "attr__number_of_bedrooms[0]"    : "1",             #
    "attr__number_of_bedrooms[1]"    : "1",             # change via params_set_bedrooms(a)
    "attr__number_of_bedrooms[2]"    : "1",             # or change via params_set_bedrooms_range(a,b)
    "attr__number_of_bedrooms[3]"    : "1",             #

    "attr__type_of_waters[0]"        : "1",             # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_waters[1]"        : "1",             #
    "attr__type_of_waters[2]"        : "1",             # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_waters[3]"        : "1",             #

    "attr__type_of_beach[0]"         : "1",             # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_beach[1]"         : "1",             #
    "attr__type_of_beach[2]"         : "1",             # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_beach[3]"         : "1",             #

    "attr__electric_sauna"           : "1",             #
    "attr__smoke_sauna"              : "1",             # change via params_set_sauna(electric_sauna = False, smoke_sauna = False, wood_sauna = False)
    "attr__wood_sauna"               : "1",             #

    "attr__dishwater"                : "1",
    "attr__refridgerator"            : "1",
    "attr__cooking_possibility"      : "1",
    "attr__microwave_oven"           : "1",
    "attr__freezer"                  : "1",
    "attr__stove"                    : "1",             # change via params_set_kitchen_equipment(astianpesukone = False, jääkaappi = False, keittomahdollisuus = False, mikroaaltouuni = False, pakastin = False, liesi = False, uuni = False, kahvinkeitin = False, grillikota = False, ):
    "attr__owen"                     : "1",
    "attr__coffee_maker"             : "1",
    "attr__barbecue_hut"             : "1",

    "attr__ski_center_nearby"        : "1",             # change via def params_set_features(hiihtokeskus_lähellä=False, internetyhteys=False, kuivauskaappi=False, kuivausrumpu=False, laituri=False, parvi=False, palju=False, poreamme=False, pyykinpesukone=False, syöttötuoli=False, suihku=False, sähköauton_lataus=False, takka=False, tv=False, uima_allas=False, ulkoporeallas=False, vauvasänky=False, mökkissä_ei_sähköjä=False, sähkö_aurinkopaneeleista=False, kantovesi=False, viilentävä_ilmalämpöpumppu=False, sisä_wc=False, ulko_wc=False, vene=False, kanootti=False, lemmikit_sallittu=False)
    "attr__internet"                 : "1",
    "attr__drying_cabinet"           : "1",
    "attr__tumble_dryer"             : "1",
    "attr__pier"                     : "1",
    "attr__loft"                     : "1",
    "attr__outdoor_hot_tub_barrel_style" : "1",
    "attr__hot_tub"                  : "1",
    "attr__washing_machine"          : "1",
    "attr__feeding_chair"            : "1",
    "attr__shower"                   : "1",
    "attr__electric_vehicle_charging": "1",
    "attr__fireplace_decoration"     : "1",
    "attr__television"               : "1",
    "attr__swimming_pool"            : "1",
    "attr__outdoor_hot_tub"          : "1",
    "attr__baby_crib"                : "1",
    "attr__no_electricity"           : "1",
    "attr__solar_panel_electricity"  : "1",
    "attr__water_carried"            : "1",
    "attr__ac_unit"                  : "1",
    "attr__indoor_toilet"            : "1",
    "attr__outoor_toilet"            : "1",
    "attr__boat"                     : "1",
    "attr__paddling"                 : "1",
    "attr__pets_allowed"             : "1",

    "attr__wheel_chair_accessible"   : "1",})

# ---------------------------------------------------------


def fetch_page(params=PARAMS, base_url=BASE_URL):
    

    if params:
        query_string = urllib.parse.urlencode(params, safe='/', encoding='utf-8')
        url = f"{base_url}?{query_string}"
        print(query_string)
        print(url)
    else:
        url = base_url
    print(f"Fetching URL: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout= 10)
        resp.raise_for_status()
        html = resp.text
        with open(FILE_LOCATION, "w", encoding="utf-8") as f:
            f.write(html)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

def get_url(params = PARAMS, base_url = BASE_URL):  

    params_clean()

    if params:
        query_string = urllib.parse.urlencode(params, safe='/', encoding='utf-8')
        url = f"{base_url}?{query_string}"
        return url

    else:
        url = base_url
        return url



if __name__ == "__main__":
    params_set_none()
    params_set_require_4_stars(True)
    fetch_page(params_clean(PARAMS))