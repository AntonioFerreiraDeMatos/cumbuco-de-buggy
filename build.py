# -*- coding: utf-8 -*-
"""
Gerador do site trilíngue — Igor Vasconcelos | Buggy Cumbuco
Edite os textos em TEXTOS e rode:  python build.py
Gera: pt-br/index.html, en/index.html, es/index.html, assets/js/i18n.js, sitemap.xml, robots.txt
"""
import json, re, urllib.parse, os

SITE = "https://www.buggycumbuco.com.br"   # <<< troque pelo domínio definitivo
WHATSAPP = "5585997126836"                  # número oficial (wa.me)
LANGS = {"pt": "pt-br", "en": "en", "es": "es"}
GOOGLE_REVIEWS_URL = "https://www.google.com/search?q=Cumbuco+de+buggy&oq=Cumbuco+de+buggy&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCAgCEAAYFhgeMggIAxAAGBYYHjIICAQQABgWGB4yCAgFEAAYFhgeMggIBhAAGBYYHjIGCAcQRRg80gEHODgxajBqN6gCCLACAfEFQpVpy0JiQGI&sourceid=chrome&source=chrome.ob&ie=UTF-8#sv=CAESzQEKuQEStgEKd0FERGJXZVlWM2pSR1lkSVlFeUZodVNOM3BqbDZWTm90RVpwRHN2OXBWU3RVb3lEY0dHMTYyaGJLRWxpbERWblFYMGVFN21mRFJVc3QzN3JwS29mQ1dwX1lINkpfbHhNV1BfbzZmOVkwSEI2VGl0Yk5VNTFZTkdvEhdCS0w1YXRfNUpyS0Y1T1VQd0pPWGlRVRoiQUhOMEU3RnRvbUg5bDNTdjVsRzZqdDdXVFFWa0hrYnRQdxIEODA1MRoBMyoAMAA4AUAAGAAgk_Dsww1KAhAB"
# Depoimentos REAIS copiados do Google (não inventar). Formato:
# ("Nome do cliente", 5, "Texto exatamente como está no Google", "mês/ano")
REVIEWS = [
 ("Osnir Santos", 5, "Tivemos uma das mais marcantes experiências nesse lugar. Foi uma sorte ter como nosso guia e bugueiro o Igor. Atenção impressionante e todo cuidado conosco. Conhecemos trilhas e lugares incríveis e um pôr do sol que de longe foi o mais perfeito até hoje. Quero aqui agradecer ao Igor por nos proporcionar isso. Forte abraço e até a próxima. Osnir e Bruno", ""),
 ("Tais Provensi", 5, "Ótima experiência, com emoção e segurança. Igor foi muito atencioso desde o atendimento no WhatsApp. Ele, juntamente com o Lucas, nos conduziram pelo roteiro completo nas dunas e lagoas de Cumbuco e nos deixaram a vontade para aproveitar as paradas. De quebra, recebemos registros lindíssimos feitos pelo Igor. Recomendo!", ""),
 ("Gabrielle Gonçalves", 5, "Excelente passeio. Igor muito atencioso e educado do momento que fechamos via WhatsApp até o fim do passeio. Passeio incrível, lugares lindos e emoção na dose certa!", ""),
 ("Nelson Marcos", 5, "O passeio foi super divertido. O buggueiro tem boa comunicação, deu dicas, chegou no horário combinado para nos buscar e deixou a gente curtir o passeio no nosso tempo. Recomendo.", ""),
 ("Daniela Badini Nacif", 5, "Foi excelente o passeio! O Igor me levou nos melhores lugares para conhecer e tirou as melhores fotos!! Recomendo muito!", ""),
 ("Andre Rego", 5, "Excelente atendimento! Guia Igor super educado e prestativo. Passeio top demais !!", ""),
 ("Marcos Sobral", 5, "Ótimo passeio, condutor do Buggy super atencioso. Valor justo e ótimo atendimento", ""),
 ("Tiago Moura", 5, "Passeio espetacular, atendimento excelente do igor, valeu muito a pena", ""),
 ("Vania Lucia", 5, "Passeio maravilho vale muito a pena , adorei", ""),
 ("Maria Francisca Cunha", 5, "Foi uma experiência inesquecível! Recomendo muito ❤️", ""),
 ("Warlen Silva", 5, "Passeio Sensacional", ""),
]
GOOGLE_RATING = "5,0"
GOOGLE_COUNT = 17

HTML_LANG = {"pt": "pt-BR", "en": "en", "es": "es"}
OG_LOCALE = {"pt": "pt_BR", "en": "en_US", "es": "es_ES"}

T = {
# ---------- SEO ----------
"meta.title": {
 "pt": "Passeio de Buggy em Cumbuco | Igor Vasconcelos — Bugueiro Credenciado",
 "en": "Buggy Tour Cumbuco | Igor Vasconcelos — Licensed Beach Buggy Driver",
 "es": "Paseo en Buggy por Cumbuco | Igor Vasconcelos — Bugueiro Acreditado"},
"meta.desc": {
 "pt": "Passeio completo de buggy nas dunas de Cumbuco com Igor Vasconcelos: bugueiro credenciado desde 2016, seguro passeio, buggy com som e busca no seu hotel. Passeios em Cumbuco e Fortaleza — reserve pelo WhatsApp.",
 "en": "Cumbuco beach buggy tour with Igor Vasconcelos: licensed driver since 2016, tour insurance, buggy with sound system and pickup at your hotel. The best buggy ride in Ceará, Brazil — book on WhatsApp.",
 "es": "Paseo en buggy por las dunas de Cumbuco con Igor Vasconcelos: bugueiro acreditado desde 2016, seguro de paseo, buggy con sonido y te recogemos en tu hotel. Paseos turísticos en Cumbuco, Brasil — reserva por WhatsApp."},
"meta.keywords": {
 "pt": "passeio de buggy Cumbuco, passeios em Cumbuco, passeios em Fortaleza, buggy nas dunas de Cumbuco, passeio completo de buggy em Cumbuco",
 "en": "buggy tour Cumbuco, Cumbuco buggy ride, Cumbuco beach buggy tour, buggy tour in Ceará Brazil",
 "es": "paseo en buggy por Cumbuco, paseos en buggy en Cumbuco, tour en buggy por las dunas de Cumbuco, paseos turísticos en Cumbuco Brasil"},

# ---------- Acessibilidade / navegação ----------
"a11y.skip": {"pt": "Pular para o conteúdo", "en": "Skip to content", "es": "Saltar al contenido"},
"a11y.menu": {"pt": "Abrir menu", "en": "Open menu", "es": "Abrir menú"},
"a11y.lang": {"pt": "Selecionar idioma", "en": "Select language", "es": "Seleccionar idioma"},
"a11y.wa": {"pt": "Conversar com Igor no WhatsApp", "en": "Chat with Igor on WhatsApp", "es": "Hablar con Igor por WhatsApp"},
"a11y.close": {"pt": "Fechar", "en": "Close", "es": "Cerrar"},
"a11y.prev": {"pt": "Foto anterior", "en": "Previous photo", "es": "Foto anterior"},
"a11y.next": {"pt": "Próxima foto", "en": "Next photo", "es": "Foto siguiente"},
"a11y.video": {"pt": "Vídeo das dunas e praias de Cumbuco", "en": "Video of Cumbuco's dunes and beaches", "es": "Video de las dunas y playas de Cumbuco"},
"nav.about": {"pt": "Sobre", "en": "About", "es": "Sobre mí"},
"nav.tours": {"pt": "Passeios", "en": "Tours", "es": "Paseos"},
"nav.pickup": {"pt": "Busca", "en": "Pickup", "es": "Recogida"},
"nav.gallery": {"pt": "Galeria", "en": "Gallery", "es": "Galería"},
"nav.video": {"pt": "Vídeo", "en": "Video", "es": "Video"},
"nav.cta": {"pt": "Reservar", "en": "Book now", "es": "Reservar"},

# ---------- Hero ----------
"hero.kicker": {"pt": "Cumbuco · Ceará · Brasil", "en": "Cumbuco · Ceará · Brazil", "es": "Cumbuco · Ceará · Brasil"},
"hero.title": {"pt": "Experimente Cumbuco. <em>Experimente de Buggy.</em>",
               "en": "Experience Cumbuco. <em>Experience it by Buggy.</em>",
               "es": "Experimenta Cumbuco. <em>Experimenta en Buggy.</em>"},
"hero.sub": {"pt": "Olá, eu sou Igor Vasconcelos 👋<br><br>Sou o responsável pela Cumbuco de Buggy e atuo como bugueiro há mais de 10 anos, levando visitantes para conhecer as dunas, lagoas, praias e os lugares mais especiais de Cumbuco.<br><br>Aqui você fala diretamente com quem vai realizar o seu passeio. Sem atravessadores, sem intermediários e sem complicação.<br><br>Você pode escolher um dos nossos roteiros ou, se preferir, montar seu próprio passeio. Quer conhecer uma lagoa específica? Fazer mais dunas? Ter mais tempo para aproveitar cada parada? Ou simplesmente criar um roteiro diferente? Conversamos e adaptamos a experiência às suas preferências.<br><br>Meu compromisso é proporcionar um passeio privativo, seguro, personalizado e acima de tudo, uma experiência que você realmente aproveite.<br><br>🌴 Conheça Cumbuco no seu ritmo.<br><br>🏜️ Experimente Cumbuco de Buggy.",
             "en": "Hi, I'm Igor Vasconcelos 👋<br><br>I run Cumbuco de Buggy and have been a buggy driver for over 10 years, taking visitors to discover the dunes, lagoons, beaches and the most special places in Cumbuco.<br><br>Here you talk directly to the person who will run your tour. No middlemen, no intermediaries and no hassle.<br><br>You can choose one of our routes or, if you prefer, build your own tour. Want to visit a specific lagoon? Ride more dunes? Have more time to enjoy each stop? Or simply create a different route? We talk and tailor the experience to your preferences.<br><br>My commitment is to provide a private, safe, personalized tour and, above all, an experience you truly enjoy.<br><br>🌴 Discover Cumbuco at your own pace.<br><br>🏜️ Experience Cumbuco by Buggy.",
             "es": "Hola, soy Igor Vasconcelos 👋<br><br>Soy el responsable de Cumbuco de Buggy y trabajo como bugueiro desde hace más de 10 años, llevando a visitantes a conocer las dunas, lagunas, playas y los lugares más especiales de Cumbuco.<br><br>Aquí hablas directamente con quien hará tu paseo. Sin intermediarios y sin complicaciones.<br><br>Puedes elegir una de nuestras rutas o, si prefieres, armar tu propio paseo. ¿Quieres conocer una laguna específica? ¿Hacer más dunas? ¿Tener más tiempo para disfrutar cada parada? ¿O simplemente crear una ruta diferente? Conversamos y adaptamos la experiencia a tus preferencias.<br><br>Mi compromiso es ofrecer un paseo privado, seguro, personalizado y, sobre todo, una experiencia que realmente disfrutes.<br><br>🌴 Conoce Cumbuco a tu ritmo.<br><br>🏜️ Experimenta Cumbuco en Buggy."},
"hero.cta": {"pt": "Reserve seu passeio pelo WhatsApp", "en": "Book your buggy tour on WhatsApp", "es": "Reserva tu paseo por WhatsApp"},
"hero.cta2": {"pt": "Conhecer os passeios", "en": "See the tours", "es": "Ver los paseos"},
"hero.b1": {"pt": "Desde 2016", "en": "Since 2016", "es": "Desde 2016"},
"hero.b2": {"pt": "Seguro Passageiro", "en": "Passenger insurance", "es": "Seguro de pasajero"},
"hero.b3": {"pt": "Buscamos você onde estiver!", "en": "We pick you up at your location!", "es": "¡Te recogemos donde estés!"},

# ---------- Credibilidade ----------
"cred.title": {"pt": "Por que passear com Igor", "en": "Why ride with Igor", "es": "Por qué pasear con Igor"},
"cred.1.t": {"pt": "Experiência desde 2016", "en": "Experience since 2016", "es": "Experiencia desde 2016"},
"cred.1.d": {"pt": "Há mais de 10 anos conduzindo com segurança, responsabilidade e proporcionando momentos inesquecíveis em Cumbuco.", "en": "Over 10 years driving safely and responsibly, creating unforgettable moments in Cumbuco.", "es": "Más de 10 años conduciendo con seguridad y responsabilidad, creando momentos inolvidables en Cumbuco."},
"cred.2.t": {"pt": "Bugueiro credenciado", "en": "Licensed buggy driver", "es": "Bugueiro acreditado"},
"cred.2.d": {"pt": "Profissional credenciado para conduzir passeios turísticos com segurança e responsabilidade.",
             "en": "A licensed professional, authorised to run tourist tours safely and responsibly.",
             "es": "Profesional acreditado para realizar paseos turísticos con seguridad y responsabilidad."},
"cred.3.t": {"pt": "Seguro Passageiro", "en": "Passenger insurance", "es": "Seguro de pasajero"},
"cred.3.d": {"pt": "Seu passeio conta com seguro passageiro, para você aproveitar cada momento com tranquilidade.", "en": "Your tour includes passenger insurance, so you can enjoy every moment with peace of mind.", "es": "Tu paseo cuenta con seguro de pasajero, para que disfrutes cada momento con tranquilidad."},
"cred.4.t": {"pt": "Buggy com som", "en": "Buggy with sound system", "es": "Buggy con sonido"},
"cred.4.d": {"pt": "Trilha sonora a bordo: a aventura fica ainda mais animada com sua música favorita.",
             "en": "Soundtrack on board: the adventure gets even better with your favourite music.",
             "es": "Música a bordo: la aventura es aún más animada con tus canciones favoritas."},

# ---------- Sobre ----------
"about.kicker": {"pt": "Seu bugueiro em Cumbuco", "en": "Your buggy driver in Cumbuco", "es": "Tu bugueiro en Cumbuco"},
"about.title": {"pt": "Olá, eu sou Igor Vasconcelos", "en": "Hi, I'm Igor Vasconcelos", "es": "Hola, soy Igor Vasconcelos"},
"about.p1": {"pt": "Sou o responsável pela <strong>Cumbuco de Buggy</strong> e atuo como bugueiro há <strong>mais de 10 anos</strong>, levando visitantes para conhecer as dunas, lagoas, praias e os lugares mais especiais de Cumbuco.",
             "en": "I run <strong>Cumbuco de Buggy</strong> and have been a buggy driver for <strong>more than 10 years</strong>, taking visitors to discover the dunes, lagoons, beaches and the most special places in Cumbuco.",
             "es": "Soy el responsable de <strong>Cumbuco de Buggy</strong> y trabajo como bugueiro desde hace <strong>más de 10 años</strong>, llevando a visitantes a conocer las dunas, lagunas, playas y los lugares más especiales de Cumbuco."},
"about.quote": {"pt": "Aqui você fala diretamente com quem vai realizar o seu passeio. <strong>Sem atravessadores, sem intermediários e sem complicação.</strong>",
             "en": "Here you talk directly to the person who will run your tour. <strong>No agents, no middlemen and no hassle.</strong>",
             "es": "Aquí hablas directamente con quien va a realizar tu paseo. <strong>Sin agencias, sin intermediarios y sin complicaciones.</strong>"},
"about.p2": {"pt": "Você pode escolher um dos nossos roteiros ou, se preferir, <strong>montar seu próprio passeio</strong>:",
             "en": "You can choose one of our routes or, if you prefer, <strong>build your own tour</strong>:",
             "es": "Puedes elegir una de nuestras rutas o, si lo prefieres, <strong>armar tu propio paseo</strong>:"},
"about.q1": {"pt": "Quer conhecer uma lagoa específica?", "en": "Want to visit a specific lagoon?", "es": "¿Quieres conocer una laguna específica?"},
"about.q2": {"pt": "Fazer mais dunas?", "en": "Ride more dunes?", "es": "¿Hacer más dunas?"},
"about.q3": {"pt": "Ter mais tempo para aproveitar cada parada?", "en": "Have more time to enjoy each stop?", "es": "¿Tener más tiempo para disfrutar cada parada?"},
"about.q4": {"pt": "Ou simplesmente criar um roteiro diferente?", "en": "Or simply create a different route?", "es": "¿O simplemente crear una ruta diferente?"},
"about.p3": {"pt": "Conversamos e adaptamos a experiência às suas preferências.", "en": "We talk it over and tailor the experience to your preferences.", "es": "Conversamos y adaptamos la experiencia a tus preferencias."},
"about.p4": {"pt": "Meu compromisso é proporcionar um passeio <strong>privativo, seguro e personalizado</strong> e, acima de tudo, uma experiência que você realmente aproveite.",
             "en": "My commitment is to offer a <strong>private, safe and personalised</strong> tour and, above all, an experience you truly enjoy.",
             "es": "Mi compromiso es ofrecer un paseo <strong>privado, seguro y personalizado</strong> y, sobre todo, una experiencia que realmente disfrutes."},
"about.s1": {"pt": "Conheça Cumbuco no seu ritmo.", "en": "Discover Cumbuco at your own pace.", "es": "Conoce Cumbuco a tu ritmo."},
"about.s2": {"pt": "Experimente Cumbuco de Buggy.", "en": "Experience Cumbuco de Buggy.", "es": "Vive Cumbuco de Buggy."},
"about.highlight": {"pt": "Fotos e vídeos do seu passeio inclusos", "en": "Photos and videos of your tour included", "es": "Fotos y videos de tu paseo incluidos"},
"about.alt": {"pt": "Buggy amarelo de Igor Vasconcelos nas dunas de Cumbuco", "en": "Igor Vasconcelos' yellow buggy on the Cumbuco dunes", "es": "Buggy amarillo de Igor Vasconcelos en las dunas de Cumbuco"},

# ---------- Passeios ----------
"tours.kicker": {"pt": "Experiências", "en": "Experiences", "es": "Experiencias"},
"tours.title": {"pt": "Passeios de buggy em Cumbuco", "en": "Buggy tours in Cumbuco", "es": "Paseos en buggy en Cumbuco"},
"tours.sub": {"pt": "Consulte condições e valores diretamente com Igor!", "en": "Check rates and availability directly with Igor!", "es": "¡Consulta condiciones y tarifas directamente con Igor!"},
"t1.tag": {"pt": "Mais procurado", "en": "Most popular", "es": "El más buscado"},
"t1.title": {"pt": "Passeio Completo", "en": "Complete Buggy Tour", "es": "Paseo Completo"},
"t1.desc": {"pt": "A experiência clássica de Cumbuco: dunas de areia branca, lagoas de água doce, mirantes com vista para o mar e muita emoção no caminho.",
            "en": "The classic Cumbuco experience: white sand dunes, freshwater lagoons, sea-view lookouts and plenty of thrills along the way.",
            "es": "La experiencia clásica de Cumbuco: dunas de arena blanca, lagunas de agua dulce, miradores con vista al mar y mucha emoción en el camino."},
"t1.route.t": {"pt": "Roteiro", "en": "Route", "es": "Recorrido"},
"t1.route": {"pt": "Dunas de Cumbuco · lagoas da região · mirantes · paradas para fotos",
             "en": "Cumbuco dunes · local lagoons · lookout points · photo stops",
             "es": "Dunas de Cumbuco · lagunas de la región · miradores · paradas para fotos"},
"t1.time.t": {"pt": "Duração e distância", "en": "Duration & distance", "es": "Duración y distancia"},
"t1.time": {"pt": "Informadas por Igor conforme o roteiro combinado", "en": "Confirmed by Igor according to the agreed route", "es": "Informadas por Igor según el recorrido acordado"},
"t1.cap.t": {"pt": "Capacidade", "en": "Capacity", "es": "Capacidad"},
"t1.cap": {"pt": "Até 4 passageiros por buggy", "en": "Up to 4 passengers per buggy", "es": "Hasta 4 pasajeros por buggy"},
"t1.media.t": {"pt": "Fotos e vídeos", "en": "Photos & videos", "es": "Fotos y videos"},
"t1.media": {"pt": "Inclusos no passeio", "en": "Included in the tour", "es": "Incluidos en el paseo"},
"t1.alt": {"pt": "Turistas em cima do buggy nas dunas de Cumbuco", "en": "Tourists standing on the buggy on the Cumbuco dunes", "es": "Turistas sobre el buggy en las dunas de Cumbuco"},
"t2.tag": {"pt": "Clássico", "en": "Classic", "es": "Clásico"},
"t2.title": {"pt": "Passeio Tradicional", "en": "Traditional Buggy Tour", "es": "Paseo Tradicional"},
"t2.desc": {"pt": "O passeio de buggy tradicional pelas paisagens de Cumbuco. Os detalhes do roteiro — trajeto, duração e paradas — são apresentados pessoalmente por Igor no WhatsApp.",
            "en": "The traditional buggy tour through Cumbuco's landscapes. Igor shares the full details of the route — itinerary, duration and stops — personally on WhatsApp.",
            "es": "El paseo en buggy tradicional por los paisajes de Cumbuco. Igor presenta personalmente por WhatsApp los detalles del recorrido: trayecto, duración y paradas."},
"t2.info": {"pt": "Converse com Igor para conhecer o roteiro", "en": "Chat with Igor to learn about the route", "es": "Habla con Igor para conocer el recorrido"},
"t2.alt": {"pt": "Grupo sobre o buggy ao pôr do sol entre coqueiros em Cumbuco", "en": "Group on the buggy at sunset among palm trees in Cumbuco", "es": "Grupo sobre el buggy al atardecer entre cocoteros en Cumbuco"},
"tours.btn": {"pt": "Consultar no WhatsApp", "en": "Ask on WhatsApp", "es": "Consultar por WhatsApp"},
"opt.title": {"pt": "Brincadeiras opcionais", "en": "Optional fun extras", "es": "Diversiones opcionales"},
"opt.sub": {"pt": "Durante o passeio você pode incluir brincadeiras à parte nas lagoas. Consulte com Igor.",
            "en": "During the tour you can add fun extras at the lagoons. Ask Igor for details.",
            "es": "Durante el paseo puedes sumar diversiones aparte en las lagunas. Consulta con Igor."},
"opt.1": {"pt": "Tirolesa", "en": "Zip line", "es": "Tirolesa"},
"opt.2": {"pt": "Toboágua", "en": "Water slide", "es": "Tobogán acuático"},
"opt.3": {"pt": "Catapulta aquática", "en": "Water catapult", "es": "Catapulta acuática"},
"opt.4": {"pt": "Pula-pula aquático", "en": "Water trampoline", "es": "Cama elástica acuática"},
"opt.5": {"pt": "Banana boat", "en": "Banana boat", "es": "Banana boat"},
"opt.6": {"pt": "Boia", "en": "Towed float", "es": "Boya arrastre"},
"opt.7": {"pt": "Jet-ski", "en": "Jet ski", "es": "Moto acuática"},
"opt.8": {"pt": "Lancha", "en": "Speedboat", "es": "Lancha"},
"opt.note": {"pt": "As brincadeiras opcionais são contratadas à parte, diretamente nos locais.",
             "en": "Optional fun extras are paid separately, directly on site.",
             "es": "Las diversiones opcionales se contratan aparte, directamente en el lugar."},


# ---------- Roteiros reais (informados pelo Igor) ----------
"t1.tag2": {"pt": "Roteiro completo", "en": "Full itinerary", "es": "Recorrido completo"},
"t1.desc2": {"pt": "Dunas, lagoas, praia e rio em uma experiência inesquecível. Conheça o melhor de Cumbuco a bordo de um buggy privativo, por trilhas e paisagens paradisíacas que fazem da região um dos destinos mais incríveis do Ceará.",
             "en": "Dunes, lagoons, beach and river in one unforgettable experience. Discover the best of Cumbuco aboard a private buggy, along trails and stunning landscapes that make this one of Ceará's most amazing destinations.",
             "es": "Dunas, lagunas, playa y río en una experiencia inolvidable. Conoce lo mejor de Cumbuco a bordo de un buggy privado, por senderos y paisajes paradisíacos que hacen de la región uno de los destinos más increíbles de Ceará."},
"t1.time2": {"pt": "Aproximadamente 2h30", "en": "Approximately 2h30", "es": "Aproximadamente 2h30"},
"t1.dist": {"pt": "Aproximadamente 28,5 km", "en": "Approximately 28.5 km", "es": "Aproximadamente 28,5 km"},
"t2.tag2": {"pt": "Mais curto", "en": "Shorter tour", "es": "Más corto"},
"t2.desc2": {"pt": "Uma aventura pelas dunas e lagoas mais famosas de Cumbuco. Ideal para quem quer conhecer os principais cenários em um passeio mais curto, com paradas para aproveitar e registrar momentos incríveis.",
             "en": "An adventure through Cumbuco's most famous dunes and lagoons. Ideal if you want to see the main sights on a shorter tour, with stops to enjoy and capture amazing moments.",
             "es": "Una aventura por las dunas y lagunas más famosas de Cumbuco. Ideal para conocer los principales escenarios en un paseo más corto, con paradas para disfrutar y registrar momentos increíbles."},
"t2.time2": {"pt": "Aproximadamente 1h30", "en": "Approximately 1h30", "es": "Aproximadamente 1h30"},
"t2.ideal.t": {"pt": "Ideal para", "en": "Best for", "es": "Ideal para"},
"t2.ideal": {"pt": "Quem tem pouco tempo", "en": "Travellers short on time", "es": "Quien tiene poco tiempo"},
"t1.route2": {"pt": "Parnamirim · Dunas · Lagoa do Banana · Barra do Cauípe", "en": "Parnamirim · Dunes · Banana Lagoon · Cauípe River mouth", "es": "Parnamirim · Dunas · Laguna del Banana · Barra do Cauípe"},
"t2.route2": {"pt": "Parnamirim · Dunas · Lagoa do Banana", "en": "Parnamirim · Dunes · Banana Lagoon", "es": "Parnamirim · Dunas · Laguna del Banana"},
"pick.slogan": {"pt": "Você escolhe o horário. Nós cuidamos da experiência!", "en": "You choose the time. We take care of the experience!", "es": "Tú eliges el horario. ¡Nosotros cuidamos la experiencia!"},
"tour.intro": {"pt": "Saímos para um parque de dunas móveis com destino à primeira parada:", "en": "We head out to a shifting dunes park towards our first stop:", "es": "Salimos hacia un parque de dunas móviles rumbo a la primera parada:"},
"st.ret.t": {"pt": "Retorno", "en": "Return", "es": "Regreso"},
"st.ret.d": {"pt": "Logo após, retornamos.", "en": "Then we head back.", "es": "Luego regresamos."},
"cr.kicker": {"pt": "Sua segurança", "en": "Your safety", "es": "Tu seguridad"},
"cr.title": {"pt": "Buggy Credenciado", "en": "Licensed Buggy", "es": "Buggy Acreditado"},
"cr.text": {"pt": "Veículo identificado, documentado e autorizado para realizar passeios turísticos em Cumbuco.", "en": "An identified, documented vehicle authorised to run tourist tours in Cumbuco.", "es": "Vehículo identificado, documentado y autorizado para realizar paseos turísticos en Cumbuco."},
"cr.how": {"pt": "Como Identificar um Buggy Credenciado?", "en": "How to identify a licensed buggy?", "es": "¿Cómo identificar un buggy acreditado?"},
"cr.how.d": {"pt": "Antes de embarcar, verifique se o buggy está devidamente autorizado para realizar passeios turísticos em Cumbuco.", "en": "Before boarding, check that the buggy is properly authorised to run tourist tours in Cumbuco.", "es": "Antes de subir, verifica que el buggy esté debidamente autorizado para realizar paseos turísticos en Cumbuco."},
"cr.1.t": {"pt": "Placa Vermelha", "en": "Red licence plate", "es": "Placa roja"},
"cr.1.d": {"pt": "Indica que o veículo está autorizado a exercer serviço remunerado de transporte, assim como os veículos utilizados em serviços de táxi.", "en": "Shows the vehicle is authorised for paid passenger transport, just like taxis.", "es": "Indica que el vehículo está autorizado a prestar servicio remunerado de transporte, al igual que los taxis."},
"cr.2.t": {"pt": "Numeração de Identificação", "en": "Identification number", "es": "Numeración de identificación"},
"cr.2.d": {"pt": "Os buggies credenciados são identificados por uma numeração própria, de 01 a 189, correspondente aos veículos credenciados no município de Caucaia.", "en": "Licensed buggies carry their own number, from 01 to 189, matching the vehicles licensed in the municipality of Caucaia.", "es": "Los buggies acreditados se identifican con una numeración propia, del 01 al 189, correspondiente a los vehículos acreditados en el municipio de Caucaia."},
"cr.3.t": {"pt": "Alvará de Autorização", "en": "Authorisation permit", "es": "Permiso de autorización"},
"cr.3.d": {"pt": "O bugueiro deve portar um alvará emitido pela Secretaria de Transportes da Prefeitura, que identifica e autoriza o veículo e o profissional para a realização de passeios de buggy em Cumbuco.", "en": "The driver must carry a permit issued by the City Transport Department, identifying and authorising both vehicle and professional to run buggy tours in Cumbuco.", "es": "El bugueiro debe portar un permiso emitido por la Secretaría de Transportes de la Alcaldía, que identifica y autoriza al vehículo y al profesional para realizar paseos en buggy en Cumbuco."},
"cr.4.t": {"pt": "Segurança e Tranquilidade", "en": "Safety and peace of mind", "es": "Seguridad y tranquilidad"},
"cr.4.d": {"pt": "Ao escolher um bugueiro credenciado, você pode conferir a documentação e a identificação do veículo antes de iniciar o passeio.", "en": "By choosing a licensed driver, you can check the vehicle's documents and identification before the tour starts.", "es": "Al elegir un bugueiro acreditado, puedes verificar la documentación y la identificación del vehículo antes de iniciar el paseo."},
"tour.private": {"pt": "Buggy privativo", "en": "Private buggy", "es": "Buggy privado"},
"tour.emotion": {"pt": "Com ou sem emoção", "en": "With or without thrills", "es": "Con o sin emoción"},
"tour.more": {"pt": "Ver roteiro completo", "en": "See full itinerary", "es": "Ver recorrido completo"},
"tour.stops": {"pt": "Roteiro do passeio", "en": "Tour itinerary", "es": "Recorrido del paseo"},
"tour.note": {"pt": "Observação: as atividades são opcionais e cobradas à parte.", "en": "Note: activities are optional and charged separately.", "es": "Observación: las actividades son opcionales y se cobran aparte."},
"st.parna.t": {"pt": "Lagoa do Parnamirim", "en": "Parnamirim Lagoon", "es": "Laguna de Parnamirim"},
"st.parna.d": {"pt": "Tradicional lagoa do Skibunda e Toboágua, um dos pontos mais famosos de Cumbuco.", "en": "The traditional lagoon of sand sledding (skibunda) and water slide, one of Cumbuco's most famous spots.", "es": "La tradicional laguna del Skibunda y el tobogán acuático, uno de los puntos más famosos de Cumbuco."},
"st.dunas.t": {"pt": "Parque de Dunas Móveis", "en": "Shifting Dunes Park", "es": "Parque de Dunas Móviles"},
"st.dunas.d": {"pt": "Percurso emocionante pelas dunas com opção “com emoção” ou “sem emoção”. Parada para fotos no famoso Mirante da Duna do Jegue (fotos inclusas).", "en": "A thrilling ride across the dunes, “with thrills” or “smooth ride”. Photo stop at the famous Duna do Jegue viewpoint (photos included).", "es": "Recorrido emocionante por las dunas “con emoción” o “sin emoción”. Parada para fotos en el famoso Mirador de la Duna do Jegue (fotos incluidas)."},
"st.banana.t": {"pt": "Lagoa do Banana", "en": "Banana Lagoon", "es": "Laguna del Banana"},
"st.banana.d": {"pt": "Momento de lazer com atividades opcionais: Tirolesa · Banana Boat · Boia Maluca · Jetski · Lancha · Futebol de sabão · Catapulta.", "en": "Leisure time with optional activities: Zipline · Banana Boat · Crazy Tube · Jet ski · Speedboat · Soap football · Catapult.", "es": "Momento de ocio con actividades opcionales: Tirolesa · Banana Boat · Boya Loca · Jet ski · Lancha · Fútbol de jabón · Catapulta."},
"st.dunas2.t": {"pt": "Segundo Parque de Dunas Móveis", "en": "Second Shifting Dunes Park", "es": "Segundo Parque de Dunas Móviles"},
"st.dunas2.d": {"pt": "A aventura continua pelas dunas em direção ao Rio Cauípe, passando por paisagens naturais incríveis.", "en": "The adventure continues across the dunes towards the Cauípe River, through stunning natural scenery.", "es": "La aventura continúa por las dunas hacia el Río Cauípe, pasando por paisajes naturales increíbles."},
"st.cauipe.t": {"pt": "Barra do Cauípe", "en": "Cauípe River Mouth", "es": "Barra do Cauípe"},
"st.cauipe.d": {"pt": "Nossa última parada é um dos cenários mais especiais do roteiro: o encontro do rio com o mar, cercado por natureza e belas paisagens.", "en": "Our final stop is one of the most special settings of the tour: where the river meets the sea, surrounded by nature and beautiful scenery.", "es": "Nuestra última parada es uno de los escenarios más especiales: el encuentro del río con el mar, rodeado de naturaleza y bellos paisajes."},
"st.back.t": {"pt": "Retorno pelas dunas", "en": "Return across the dunes", "es": "Regreso por las dunas"},
"st.back.d": {"pt": "Logo após, retornamos por dunas.", "en": "Then we head back across the dunes.", "es": "Luego regresamos por las dunas."},
"opt.9": {"pt": "Skibunda", "en": "Sand sledding", "es": "Skibunda"},
"opt.10": {"pt": "Boia maluca", "en": "Crazy tube ride", "es": "Boya loca"},
"opt.11": {"pt": "Futebol de Sabão", "en": "Soap football", "es": "Fútbol de jabón"},


# ---------- Preços das brincadeiras (panfleto do local) ----------
"op.futsabao.p": {"pt": "R$ 25 por pessoa", "en": "R$ 25 per person", "es": "R$ 25 por persona"},
"op.futsabao.d": {"pt": "Diversão garantida em grupo", "en": "Guaranteed group fun", "es": "Diversión garantizada en grupo"},
"op.skibunda.p": {"pt": "R$ 30 por pessoa", "en": "R$ 30 per person", "es": "R$ 30 por persona"},
"op.skibunda.d": {"pt": "Lagoa do Parnamirim", "en": "Parnamirim Lagoon", "es": "Laguna de Parnamirim"},
"op.toboagua.p": {"pt": "R$ 30 por pessoa", "en": "R$ 30 per person", "es": "R$ 30 por persona"},
"op.toboagua.d": {"pt": "Acesso livre o dia todo", "en": "Unlimited use all day", "es": "Acceso libre todo el día"},
"op.tirolesa.p": {"pt": "R$ 40 por pessoa", "en": "R$ 40 per person", "es": "R$ 40 por persona"},
"op.tirolesa.d": {"pt": "Acesso livre o dia todo", "en": "Unlimited use all day", "es": "Acceso libre todo el día"},
"op.banana.p": {"pt": "R$ 50 por pessoa", "en": "R$ 50 per person", "es": "R$ 50 por persona"},
"op.banana.d": {"pt": "Um percurso", "en": "One ride", "es": "Un recorrido"},
"op.jetski.p": {"pt": "R$ 220 (1 pessoa) · R$ 270 (2 pessoas)", "en": "R$ 220 (1 person) · R$ 270 (2 people)", "es": "R$ 220 (1 persona) · R$ 270 (2 personas)"},
"op.jetski.d": {"pt": "10 minutos", "en": "10 minutes", "es": "10 minutos"},
"op.lancha.p": {"pt": "R$ 60 por pessoa", "en": "R$ 60 per person", "es": "R$ 60 por persona"},
"op.lancha.d": {"pt": "Passeio de lancha na lagoa", "en": "Speedboat ride on the lagoon", "es": "Paseo en lancha por la laguna"},
"op.catapulta.p": {"pt": "R$ 35", "en": "R$ 35", "es": "R$ 35"},
"op.catapulta.d": {"pt": "Direito a três saltos", "en": "Three jumps included", "es": "Derecho a tres saltos"},
"op.boia.p": {"pt": "R$ 60 cada (dupla) · R$ 70 (1 pessoa)", "en": "R$ 60 each (pair) · R$ 70 (solo)", "es": "R$ 60 c/u (pareja) · R$ 70 (1 persona)"},
"op.boia.d": {"pt": "Boia rebocada na lagoa", "en": "Towed tube on the lagoon", "es": "Boya remolcada en la laguna"},
"op.card": {"pt": "Pagamentos no cartão de crédito têm acréscimo da taxa da maquininha. Valores praticados nos locais, sujeitos a alteração.",
            "en": "Credit card payments include a card machine fee. Prices are set on site and may change.",
            "es": "Los pagos con tarjeta de crédito tienen recargo por la tasa de la máquina. Valores del lugar, sujetos a cambios."},


# ---------- Depoimentos / Google ----------
"nav.home": {"pt": "Início", "en": "Home", "es": "Inicio"},
"a11y.top": {"pt": "Voltar ao início", "en": "Back to top", "es": "Volver al inicio"},
"nav.reviews": {"pt": "Avaliações", "en": "Reviews", "es": "Opiniones"},
"rev.kicker": {"pt": "Quem passeou recomenda", "en": "Guests recommend", "es": "Quien paseó lo recomienda"},
"rev.title": {"pt": "Depoimentos de clientes", "en": "Guest reviews", "es": "Opiniones de clientes"},
"rev.text": {"pt": "Veja o que clientes reais dizem no Google. Fez o passeio com o Igor? Conte como foi: sua avaliação ajuda outros turistas a escolher.",
             "en": "See what real guests say on Google. Did you ride with Igor? Tell others how it went: your review helps other travellers choose.",
             "es": "Mira lo que dicen clientes reales en Google. ¿Paseaste con Igor? Cuenta cómo fue: tu opinión ayuda a otros turistas a elegir."},
"rev.see": {"pt": "Ver avaliações no Google", "en": "See reviews on Google", "es": "Ver opiniones en Google"},
"rev.rate": {"pt": "Avaliar no Google", "en": "Review us on Google", "es": "Opinar en Google"},
"rev.cta.t": {"pt": "Já passeou com a gente?", "en": "Already rode with us?", "es": "¿Ya paseaste con nosotros?"},
"rev.cta.d": {"pt": "Deixe sua avaliação com estrelas no Google. Leva menos de 1 minuto e faz toda a diferença para o Igor.",
              "en": "Leave a star rating on Google. It takes less than a minute and means a lot to Igor.",
              "es": "Deja tu valoración con estrellas en Google. Toma menos de 1 minuto y hace toda la diferencia para Igor."},
"rev.src": {"pt": "Avaliação no Google", "en": "Google review", "es": "Opinión en Google"},
"rev.count": {"pt": "avaliações no Google", "en": "reviews on Google", "es": "opiniones en Google"},
"rev.orig": {"pt": "Comentários reais, exibidos como foram publicados.", "en": "Real reviews, shown as originally posted (in Portuguese).", "es": "Opiniones reales, mostradas tal como fueron publicadas (en portugués)."},
"a11y.revprev": {"pt": "Depoimentos anteriores", "en": "Previous reviews", "es": "Opiniones anteriores"},
"a11y.revnext": {"pt": "Próximos depoimentos", "en": "Next reviews", "es": "Opiniones siguientes"},

# ---------- Faixa comercial ----------
"band.title": {"pt": "Quer viver essa experiência?", "en": "Ready for this experience?", "es": "¿Quieres vivir esta experiencia?"},
"band.text": {"pt": "Converse diretamente com Igor e consulte disponibilidade e condições especiais para seu passeio.",
              "en": "Talk directly to Igor and check availability and special conditions for your tour.",
              "es": "Habla directamente con Igor y consulta disponibilidad y condiciones especiales para tu paseo."},
"band.btn": {"pt": "Consultar valores e disponibilidade", "en": "Check rates and availability", "es": "Consultar tarifas y disponibilidad"},

# ---------- Busca ----------
"pick.kicker": {"pt": "Busca personalizada", "en": "Personal pickup", "es": "Recogida personalizada"},
"pick.title": {"pt": "Buscamos você onde estiver!", "en": "We pick you up at your location!", "es": "¡Te recogemos donde estés!"},
"pick.text": {"pt": "Hotel, pousada ou casa de temporada em Cumbuco ou região: Igor vai até você. Preencha abaixo e envie seu pedido pelo WhatsApp.",
              "en": "Hotel, guesthouse or holiday rental in Cumbuco or nearby: Igor comes to you. Fill in the form and send your request on WhatsApp.",
              "es": "Hotel, posada o casa de vacaciones en Cumbuco o alrededores: Igor va hasta ti. Completa el formulario y envía tu pedido por WhatsApp."},
"pick.name": {"pt": "Seu nome", "en": "Your name", "es": "Tu nombre"},
"pick.date": {"pt": "Data desejada", "en": "Preferred date", "es": "Fecha deseada"},
"pick.time": {"pt": "Horário desejado", "en": "Preferred time", "es": "Hora deseada"},
"pick.people": {"pt": "Nº de pessoas", "en": "Number of people", "es": "Nº de personas"},
"pick.place": {"pt": "Local de busca (hotel/pousada)", "en": "Pickup location (hotel/guesthouse)", "es": "Lugar de recogida (hotel/posada)"},
"pick.placeholder": {"pt": "Ex.: nome do hotel em Cumbuco", "en": "e.g. hotel name in Cumbuco", "es": "Ej.: nombre del hotel en Cumbuco"},
"pick.tour": {"pt": "Passeio", "en": "Tour", "es": "Paseo"},
"pick.btn": {"pt": "Enviar pedido pelo WhatsApp", "en": "Send request on WhatsApp", "es": "Enviar pedido por WhatsApp"},
"pick.alt": {"pt": "Buggy na praia de Cumbuco com kitesurf ao fundo", "en": "Buggy on Cumbuco beach with kitesurfers behind", "es": "Buggy en la playa de Cumbuco con kitesurf al fondo"},

# ---------- Galeria ----------
"gal.kicker": {"pt": "Momentos reais", "en": "Real moments", "es": "Momentos reales"},
"gal.title": {"pt": "Galeria de Fotos", "en": "Photo Gallery", "es": "Galería de Fotos"},
"gal.f.all": {"pt": "Todas", "en": "All", "es": "Todas"},
"gal.f.dunas": {"pt": "Dunas", "en": "Dunes", "es": "Dunas"},
"gal.f.sunset": {"pt": "Pôr do sol", "en": "Sunset", "es": "Atardecer"},
"gal.f.groups": {"pt": "Famílias e grupos", "en": "Families & groups", "es": "Familias y grupos"},
"gal.f.couples": {"pt": "Casais", "en": "Couples", "es": "Parejas"},

# ---------- Vídeo ----------
"vid.kicker": {"pt": "Sinta o clima", "en": "Feel the vibe", "es": "Siente el ambiente"},
"vid.title": {"pt": "Cumbuco em movimento", "en": "Cumbuco in motion", "es": "Cumbuco en movimiento"},
"vid.text": {"pt": "Dunas, lagoas, kitesurf e um pôr do sol inesquecível. Assista e imagine você aqui.",
             "en": "Dunes, lagoons, kitesurfing and an unforgettable sunset. Watch and picture yourself here.",
             "es": "Dunas, lagunas, kitesurf y un atardecer inolvidable. Mira e imagínate aquí."},

# ---------- Avisos ----------
"notice.title": {"pt": "Avisos importantes", "en": "Important information", "es": "Avisos importantes"},
"notice.1": {"pt": "Valores e condições são informados apenas pelo WhatsApp, diretamente com o Bugueiro.", "en": "Rates and conditions are provided only on WhatsApp, directly with the buggy driver.", "es": "Las tarifas y condiciones se informan solo por WhatsApp, directamente con el bugueiro."},
"notice.2": {"pt": "Reservas sujeitas à disponibilidade de data e horário.",
             "en": "Bookings are subject to date and time availability.",
             "es": "Reservas sujetas a disponibilidad de fecha y horario."},
"notice.3": {"pt": "Use protetor solar, óculos escuros e roupas leves.",
             "en": "Bring sunscreen, sunglasses and light clothing.",
             "es": "Usa protector solar, gafas de sol y ropa ligera."},

# ---------- Rodapé ----------
"foot.text": {"pt": "Passeios de buggy em Cumbuco com bugueiro credenciado desde 2016. Atendimento exclusivo pelo WhatsApp.",
              "en": "Buggy tours in Cumbuco with a licensed driver since 2016. Bookings exclusively via WhatsApp.",
              "es": "Paseos en buggy en Cumbuco con bugueiro acreditado desde 2016. Atención exclusiva por WhatsApp."},
"foot.rights": {"pt": "Todos os direitos reservados.", "en": "All rights reserved.", "es": "Todos los derechos reservados."},
"foot.wa": {"pt": "Fale com Igor", "en": "Talk to Igor", "es": "Habla con Igor"},
"foot.dev": {"pt": "Desenvolvido pela", "en": "Developed by", "es": "Desarrollado por"},

# ---------- Mensagens WhatsApp ----------
"wa.default": {"pt": "Olá, Igor! Conheci seu site de passeios de buggy em Cumbuco e gostaria de saber mais informações sobre os passeios e disponibilidade.",
               "en": "Hello, Igor! I found your Cumbuco buggy tour website and I would like more information about your tours and availability.",
               "es": "¡Hola, Igor! Conocí tu sitio de paseos en buggy en Cumbuco y me gustaría recibir más información sobre los paseos y la disponibilidad."},
"wa.info": {"pt": "Olá, Igor! Gostaria de informações sobre os passeios de buggy em Cumbuco.",
            "en": "Hello, Igor! I would like more information about your buggy tours in Cumbuco.",
            "es": "¡Hola, Igor! Me gustaría recibir más información sobre los paseos en buggy en Cumbuco."},
"wa.prices": {"pt": "Olá, Igor! Gostaria de consultar os valores e a disponibilidade do passeio de buggy em Cumbuco.",
              "en": "Hello, Igor! I would like to check the rates and availability for the buggy tour in Cumbuco.",
              "es": "¡Hola, Igor! Me gustaría consultar las tarifas y la disponibilidad del paseo en buggy en Cumbuco."},
"wa.t1": {"pt": "Olá, Igor! Tenho interesse no Passeio Completo de buggy em Cumbuco. Poderia me informar valores e disponibilidade?",
          "en": "Hello, Igor! I'm interested in the Complete Buggy Tour in Cumbuco. Could you tell me the rates and availability?",
          "es": "¡Hola, Igor! Me interesa el Paseo Completo en buggy por Cumbuco. ¿Podrías informarme tarifas y disponibilidad?"},
"wa.t2": {"pt": "Olá, Igor! Tenho interesse no Passeio Tradicional de buggy em Cumbuco. Poderia me passar os detalhes, valores e disponibilidade?",
          "en": "Hello, Igor! I'm interested in the Traditional Buggy Tour in Cumbuco. Could you send me the details, rates and availability?",
          "es": "¡Hola, Igor! Me interesa el Paseo Tradicional en buggy por Cumbuco. ¿Podrías enviarme detalles, tarifas y disponibilidad?"},
"wa.pick": {"pt": "Olá, Igor! Gostaria de reservar um passeio de buggy em Cumbuco.",
            "en": "Hello, Igor! I would like to book a buggy tour in Cumbuco.",
            "es": "¡Hola, Igor! Me gustaría reservar un paseo en buggy en Cumbuco."},
}

GALLERY = [  # arquivo, categorias, legenda pt/en/es
 ("dunas-mirante", "dunas", "Pose no alto do buggy nas dunas", "Posing on top of the buggy on the dunes", "Posando sobre el buggy en las dunas"),
 ("coqueiros-por-do-sol-buggy", "sunset", "Buggy entre coqueiros ao entardecer", "Buggy among palm trees at dusk", "Buggy entre cocoteros al atardecer"),
 ("familia-por-do-sol", "sunset groups", "Família no buggy ao pôr do sol", "Family on the buggy at sunset", "Familia en el buggy al atardecer"),
 ("dunas-buggy-casal", "dunas couples", "Casal no topo do buggy nas dunas", "Couple on top of the buggy on the dunes", "Pareja sobre el buggy en las dunas"),
 ("por-do-sol-grupo", "sunset groups", "Amigos ao pôr do sol", "Friends at sunset", "Amigos al atardecer"),
 ("dunas-buggy-diversao", "dunas", "Diversão nas dunas de Cumbuco", "Fun on the Cumbuco dunes", "Diversión en las dunas de Cumbuco"),
 ("casal-por-do-sol", "sunset couples", "Casal ao entardecer na praia", "Couple at dusk on the beach", "Pareja al atardecer en la playa"),
 ("casal-dunas-olhar", "dunas couples", "Casal apaixonado no buggy", "Couple in love on the buggy", "Pareja enamorada en el buggy"),
 ("dunas-pose", "dunas", "Alegria no alto do buggy", "Pure joy on top of the buggy", "Alegría sobre el buggy"),
 ("por-do-sol-dunas", "sunset couples", "Contemplando o pôr do sol nas dunas", "Watching the sunset on the dunes", "Contemplando el atardecer en las dunas"),
 ("casal-buggy-dunas", "dunas couples", "Casal curtindo o passeio", "Couple enjoying the tour", "Pareja disfrutando el paseo"),
 ("grupo-familia-dunas", "groups dunas", "Grupo reunido nas dunas", "Group together on the dunes", "Grupo reunido en las dunas"),
 ("lagoa-por-do-sol", "sunset", "Pôr do sol na lagoa", "Sunset at the lagoon", "Atardecer en la laguna"),
 ("casal-buggy-relax", "dunas couples", "Casal relaxando no buggy", "Couple relaxing on the buggy", "Pareja relajándose en el buggy"),
 ("buggy-relax-chapeu", "dunas", "Relaxando no buggy à beira-mar", "Relaxing on the buggy by the sea", "Relajándose en el buggy junto al mar"),
 ("coqueiros-por-do-sol-grupo", "sunset groups", "Grupo entre coqueiros", "Group among palm trees", "Grupo entre cocoteros"),
 ("kitesurf-buggy", "couples groups", "Buggy na praia dos kitesurfistas", "Buggy on the kitesurf beach", "Buggy en la playa del kitesurf"),
 ("familia-coqueiros", "groups", "Família entre coqueiros nas dunas", "Family under the palm trees on the dunes", "Familia entre cocoteros en las dunas"),
 ("dunas-areia-branca", "dunas", "Areia branca de Cumbuco", "Cumbuco's white sand", "Arena blanca de Cumbuco"),
 ("familia-areia", "groups dunas", "Família curtindo as dunas", "Family enjoying the dunes", "Familia disfrutando las dunas"),
 ("passeio-jumento", "groups", "Criança passeando de jumento nas dunas", "Child on a donkey ride on the dunes", "Niña paseando en burro en las dunas"),
 ("buggy-frente", "dunas", "O buggy amarelo de Igor", "Igor's yellow buggy", "El buggy amarillo de Igor"),
 ("por-do-sol-kite", "sunset", "Kitesurf no pôr do sol", "Kitesurfing at sunset", "Kitesurf al atardecer"),
 ("buggy-som-relax", "dunas", "Relaxando no buggy com som", "Relaxing on the buggy with music", "Relajándose en el buggy con música"),
]
LI = {"pt": 2, "en": 3, "es": 4}

def wa(key, lang):
    return f"https://wa.me/{WHATSAPP}?text=" + urllib.parse.quote(T[key][lang], safe="")

def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def render(lang):
    tpl = open("template.html", encoding="utf-8").read()
    gal = []
    for f, cat, *cap in GALLERY:
        c = cap[LI[lang] - 2]
        gal.append(
            f'<figure class="g-item" data-cat="{cat}"><button type="button" data-full="../assets/img/{f}.jpg">'
            f'<img src="../assets/img/thumb/{f}.jpg" alt="{esc(c)}" data-gcap="{f}" loading="lazy" width="480" height="640"></button></figure>')
    tpl = tpl.replace("{{GALLERY}}", "\n".join(gal))
    revs = []
    cores = ["#0ea5e9", "#f59e0b", "#16a34a", "#8b5cf6", "#ef4444", "#0891b2", "#db2777"]
    for i, (nome, est, txt, quando) in enumerate(REVIEWS):
        data = f" · {esc(quando)}" if quando else ""
        revs.append(f'<figure class="rev"><div class="rev-top"><span class="rev-av" style="background:{cores[i % len(cores)]}">{esc(nome[0])}</span>'
                    f'<div><b>{esc(nome)}</b><span class="rev-stars" aria-label="{est}/5">{"★"*est}{"☆"*(5-est)}</span></div>'
                    f'<svg class="rev-g" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-google"/></svg></div>'
                    f'<blockquote>{esc(txt)}</blockquote><figcaption><span data-i18n="rev.src">{T["rev.src"][lang]}</span>{data}</figcaption></figure>')
    tpl = tpl.replace("{{REVIEWS}}", "\n".join(revs))
    tpl = tpl.replace("{{GURL}}", esc(GOOGLE_REVIEWS_URL)).replace("{{GRATING}}", GOOGLE_RATING).replace("{{GCOUNT}}", str(GOOGLE_COUNT))
    alt = "\n".join(
        f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{SITE}/{p}/">' for l, p in LANGS.items()
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/pt-br/">'
    rep = {"LANG": lang, "HTML_LANG": HTML_LANG[lang], "OG_LOCALE": OG_LOCALE[lang],
           "CANONICAL": f"{SITE}/{LANGS[lang]}/", "HREFLANG": alt, "SITE": SITE, "WA": WHATSAPP}
    tpl = re.sub(r"\{\{wa:([\w.]+)\}\}", lambda m: wa(m.group(1), lang), tpl)
    tpl = re.sub(r"\{\{attr:([\w.]+)\}\}", lambda m: esc(T[m.group(1)][lang]), tpl)
    tpl = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: rep[m.group(1)], tpl)
    tpl = re.sub(r"\{\{([\w.]+)\}\}", lambda m: T[m.group(1)][lang], tpl)
    for l in LANGS:
        tpl = tpl.replace(f'data-lang="{l}" aria-current="false"',
                          f'data-lang="{l}" aria-current="{"true" if l == lang else "false"}"')
    return tpl

for lang, path in LANGS.items():
    os.makedirs(path, exist_ok=True)
    open(f"{path}/index.html", "w", encoding="utf-8").write(render(lang))

caps = {f: {"pt": a, "en": b, "es": c} for f, _, a, b, c in GALLERY}
os.makedirs("assets/js", exist_ok=True)
open("assets/js/i18n.js", "w", encoding="utf-8").write(
    "/* gerado por build.py — não editar à mão */\nwindow.I18N=" +
    json.dumps({"t": T, "caps": caps, "paths": LANGS, "htmlLang": HTML_LANG, "site": SITE, "wa": WHATSAPP},
               ensure_ascii=False) + ";\n")

urls = []
for lang, path in LANGS.items():
    links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{HTML_LANG[l]}" href="{SITE}/{p}/"/>' for l, p in LANGS.items())
    links += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/pt-br/"/>'
    urls.append(f"  <url>\n    <loc>{SITE}/{path}/</loc>{links}\n    <changefreq>monthly</changefreq>\n    <priority>{'1.0' if lang == 'pt' else '0.9'}</priority>\n  </url>")
open("sitemap.xml", "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
open("robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("OK: pt-br/, en/, es/, assets/js/i18n.js, sitemap.xml, robots.txt")
